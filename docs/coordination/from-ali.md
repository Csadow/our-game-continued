# From Ali and his AI agent — 2026-11-09

## Rendering handoff

Implemented against Muhammad's gameplay update `c1d2cbb`. The only gameplay dependency added by this pass is reading the existing `Bullet::spiral` flag. No gameplay API changes are requested. `game.h`, `game.cpp`, and `game_tests.cpp` are unchanged by Ali's work.

Files touched: `main.cpp`, this note, and three actual-build PNG screenshots under `docs/coordination/screenshots/`. The existing GLSL 330 shaders, cube/sphere meshes, and CMake dependencies remain compatible without shader changes.

- The boss has one translated, bobbing, rotating parent matrix. Core and heart are children; four orbit pivots inherit the parent; arms and satellites inherit their pivots; each satellite has a sphere beacon child that also inherits its local spin. Composition is `parent * local * vertex`, with mesh scaling at leaves so it cannot distort sibling orbits.
- Animation uses `game.elapsed`, so pause, restart, and round completion keep the visual assembly in sync with gameplay. Decorative arms are visual only and do not add collision geometry.
- Waves 1/2/3 use amber/blue/magenta for the boss, corner lights, HUD wave label, and progress bar. Orbit speed and radius increase with wave number. Progress marks show the two wave boundaries.
- Aimed bullets remain red and radial bullets amber. The new spiral stream is cyan. Dash and near-miss cues brighten the player while preserving existing invulnerability blinking.
- `--smoke-wave 1|2|3` selects a deterministic 360-frame rendering check starting at the chosen wave boundary. This is a test shortcut, not evidence that a player survived the earlier waves. Normal play still starts at wave 1.

## Validation

On CachyOS Linux, GCC 16.2.1, Release build:

```sh
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j2
ctest --test-dir build --output-on-failure
glslangValidator scene.vert scene.frag hud.vert hud.frag
```

Build completed without compiler warnings; the `game_rules` CTest passed, all four shaders validated, and `git diff --check` passed. Invalid `--smoke-wave 4` exits with a validation message before GLFW initialization.

All three integrated OpenGL checks passed with no reported GL errors, using Xvfb at 1280x800 and Mesa 26.2.5 llvmpipe (LLVM 23.1.3, 256 bits), software rendering. Host CPU: Intel Core i5-12450HX; kernel 7.3.1-1-cachyos. Xvfb was extracted into `/tmp` for this session, without installing system packages. Equivalent commands on a machine with `xvfb-run` installed:

```sh
env -u WAYLAND_DISPLAY LIBGL_ALWAYS_SOFTWARE=1 xvfb-run -a -s '-screen 0 1280x800x24 -nolisten tcp' ./build/bullethell --smoke-wave 1 --screenshot build/wave-1.ppm
env -u WAYLAND_DISPLAY LIBGL_ALWAYS_SOFTWARE=1 xvfb-run -a -s '-screen 0 1280x800x24 -nolisten tcp' ./build/bullethell --smoke-wave 2 --screenshot build/wave-2.ppm
env -u WAYLAND_DISPLAY LIBGL_ALWAYS_SOFTWARE=1 xvfb-run -a -s '-screen 0 1280x800x24 -nolisten tcp' ./build/bullethell --smoke-wave 3 --screenshot build/wave-3.ppm
```

| Start wave | Frames | Final bullets | Final health | Final simulated time | Process wall time | Frames / wall second |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 360 | 35 | 4 | 5.99166 s | 2.666 s | 135.0 |
| 2 | 360 | 56 | 3 | 25.9916 s | 3.419 s | 105.3 |
| 3 | 360 | 105 | 3 | 45.9929 s | 4.789 s | 75.2 |

These are single-run process measurements using Python `time.perf_counter()` around each executable invocation, with vsync disabled by smoke mode. They include startup and screenshot writing, and are **not** GPU frame timings, a controlled performance comparison, or evidence of interactive hardware FPS. Measure real play separately for the report. No human playtest is claimed.

Actual-build screenshots (lossless PPM-to-PNG conversion): [wave 1](screenshots/wave-1.png), [wave 2](screenshots/wave-2.png), [wave 3](screenshots/wave-3.png). Waves 1 and 3 were visually inspected for HUD placement, hierarchy appearance, and projectile visibility.

## Demo and submission support

I can help prepare a recording script and capture footage where a usable display is available. No YouTube account/channel has been connected, and no upload or public demo URL is claimed. Please arrange the public upload and add its exact URL to the report.

A roughly four-minute recording can show: 0:00–0:30 project aim and controls; 0:30–1:40 a real round/restart demonstrating movement, dash, hit/grace period and grazing; 1:40–2:20 distinct wave attack patterns (label any test-mode footage); 2:20–3:20 a code walkthrough of parent/child matrices, normal matrix, lighting and depth/HUD order; 3:20–4:00 test results, performance method, limitations, contributions and AI disclosure.

Muhammad retains ownership of the report, slide deck and release packaging. Still required for final submission: human playtest/code review, the supplied report template and lecture references, complete verified 15-source literature review, public 3–6 minute YouTube demo, report PDF, presentation, and source ZIP. This rendering handoff does not mark those deliverables complete.

## Journal literature leads

The following five real journal articles have bibliographic/paper links checked on 2026-11-09. Relevance sentences are suggestions for the literature review, not claims that the corresponding algorithms are implemented. **Quartiles are not independently verified here**: record the required ranking system, category and year from an authoritative ranking record before counting any toward the 15 Q1/Q2 sources. Old conference versions must not replace the journal versions below.

| Journal reference | DOI and verification link | Relevance |
| --- | --- | --- |
| Bui Tuong Phong (1975), “Illumination for Computer Generated Pictures,” *Communications of the ACM* 18(6), 311–317. | [DOI](https://doi.org/10.1145/360825.360839); [paper](https://users.cs.northwestern.edu/~ago820/cs395/Papers/Phong_1975.pdf) | Provides context for smooth shading and specular illumination; explain that our shader uses the half-vector variant rather than claiming it implements Phong's original reflection formula exactly. |
| R. L. Cook and K. E. Torrance (1982), “A Reflectance Model for Computer Graphics,” *ACM Transactions on Graphics* 1(1), 7–24. | [DOI](https://doi.org/10.1145/357290.357293); [Cornell paper listing](https://www.graphics.cornell.edu/~westin/consortium-home/index.html) | Offers a physically motivated reference against which to discuss the limitations of our inexpensive empirical shader; Cook–Torrance is not implemented. |
| Christophe Schlick (1994), “A Survey of Shading and Reflectance Models,” *Computer Graphics Forum* 13(2), 121–131. | [Publisher/DOI](https://onlinelibrary.wiley.com/doi/abs/10.1111/1467-8659.1320121) | Helps organize the report's comparison of local shading models and the choice of a simple real-time lighting model. |
| Christophe Schlick (1994), “An Inexpensive BRDF Model for Physically-based Rendering,” *Computer Graphics Forum* 13(3), 233–246. | [Publisher/DOI](https://onlinelibrary.wiley.com/doi/10.1111/1467-8659.1330233) | Supplies a reference for the efficiency-versus-physical-accuracy tradeoff and a possible future material model, not the current implementation. |
| M. Teschner et al. (2005), “Collision Detection for Deformable Objects,” *Computer Graphics Forum* 24(1), 61–81. | [Publisher/DOI](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1467-8659.2005.00829.x); [author paper](https://cg.informatik.uni-freiburg.de/publications/2005_CGF_collisionDetection.pdf) | Provides background on spatial partitioning and bounding volumes for future scaling; our current rigid sphere checks are much simpler and do not implement deformable collision. |

## Authorship and publication

Ali supplied the repository-local Git author `ali <254135@astanait.edu.kz>`. This rendering implementation, validation and handoff were prepared with Codex AI assistance; Ali should review and understand the submitted code. Personal GitHub credentials and global Git configuration were not used for this work. The GitHub connector was verified as university account `at254135`, with university email `254135@astanait.edu.kz`, before publication. This pass is submitted on `ali/hierarchical-boss` for Muhammad's integration review; please read this reply from that branch until it is merged.

## Review of report and slides source at `8223123`

I reviewed `docs/REPORT_DRAFT.md`, `docs/RESEARCH_NOTES.md`, and the relevant presentation-generation text in `tools/make_submission.py`. I have not reviewed the generated PDF/PPTX or the supplied template itself in this workspace. Please make these integration edits in your owned documents:

1. Add the hierarchy explanation above to report sections 4.3/5.3 and the graphics slides. Include the leaf-only scales and inverse-transpose normal matrix. The code now has 3 levels of inherited transforms (boss, satellite, beacon), with explicit orbit pivots between boss and satellite.
2. Replace the old Figure 1 with an integrated screenshot from this branch; wave 3 shows all three projectile types. Name the wave-color cues and cyan spiral bullets in its caption and surrounding text.
3. Section 4.2 currently discloses Codex assistance only for Mukhammed. Include Ali's AI-assisted rendering implementation, validation, and handoff too. Ali did not change shader source in this pass, so do not list new shader code as a contribution.
4. The old 88.2 frames/s / 205 MiB result is from Mukhammed's earlier build and different CPU. Retain it only if labeled as that baseline, or remeasure the final build on the presentation machine. Our new table is a separate, single-run software-rendering measurement; it does not measure RSS and cannot establish a before/after speedup. Update the hardcoded slide measurement consistently if replacing it.
5. The slide source still says Ali's hierarchy is “in progress”; change that after merging and reviewing this pass.
6. Report section 2 describes all sources as selected for Q1/Q2 standing, while the research notes still request a final index check. Before submission, record each venue's ranking system, year, subject category and actual Q1/Q2 evidence; do not represent pending checks as complete.
7. Replace every `VIDEO_URL_PENDING_PUBLIC_UPLOAD` occurrence with the actual public YouTube URL, regenerate all deliverables, inspect the exported pages/slides, and rebuild the source ZIP from the merged commit. Complete a real 60-second playtest and code explanation before submission.

Publication update: the connector could read the repository but rejected file-object creation (HTTP 403). The newly created university SSH key was then explicitly tested and GitHub replied `Hi at254135!`. Only this key is configured in this repository, with the SSH agent and personal SSH configuration disabled for its Git operations.

## Sphere performance follow-up — 2026-11-09

Completed the integration-review request from `to-ali.md`, based on integrated main `0e46b8e`. The shared sphere now uses **12 rows by 16 columns**, retaining the same analytic positions, smooth normals, UVs, radius and draw path. Storage is reserved once before filling the mesh. Generated triangles per sphere fall from 1,120 to 384, a 65.7% reduction; vertices fall from 3,360 to 1,152. No gameplay code, hit radii, shaders or dependencies changed.

Both versions were configured and built in Release mode on the same Intel Core i5-12450HX/CachyOS machine. Comparison used a dedicated Xvfb display at 1280×800, Mesa 26.2.5 llvmpipe (LLVM 23.1.3, 256 bits), vsync disabled, and the same command arguments: `--smoke-wave 3 --screenshot wave-3.ppm`. One warm-up per version was excluded, then three runs per version were interleaved, alternating which version ran first. Process wall time includes initialization and screenshot writing. Linux `wait4` measured peak resident memory for each child; this is process RSS, not GPU memory. All eight runs passed 360 rendered frames and ended at 105 projectiles, HP 3, and the same simulated time.

| Mesh | Measured wall times | Median wall time | Median frames / wall second | Median peak process RSS |
| --- | --- | --- | --- | --- |
| 20 × 28 | 4.947, 4.960, 4.905 s | 4.947 s | 72.8 | 141.8 MiB |
| 12 × 16 | 2.122, 2.179, 2.233 s | 2.179 s | 165.2 | 121.3 MiB |

This comparison shows about 56% lower median process wall time for this software-rendered smoke workload on this machine. It is not a claim about dedicated-GPU FPS, other CPUs, or a full human-played round. Please remeasure your same Ryzen/Mesa wave-3 command for a local comparison rather than mixing these results with your 35.8 frames/s baseline. The raw observations, including warm-ups, CPU time and KiB RSS, are in [sphere-benchmark.json](sphere-benchmark.json).

The Release build and `game_rules` test passed. The full-size before/after wave-3 screenshots were visually inspected: the player and tiny projectiles remain round enough at the fixed camera scale, the HUD and hierarchy are unchanged, and the three projectile types remain readable. [Optimized wave-3 screenshot](screenshots/wave-3-optimized.png). The rendering PR can be reviewed independently of document changes.

Additional submission review: all 15 report DOIs were independently queried through Crossref on 2026-11-09 and returned matching journal-article titles and venues. The updated JCR table in your research notes agrees with the dated JCR entries I checked. Ali's supplied course template was found and rendered read-only; it has the expected sections, the 15 Q1/Q2-source requirement and the figure/in-text-reference requirement. No duplicate edits to your report or slide generator are included in this follow-up; please continue your existing document/video work. I am available for the next integration check via this folder.

## Generated report review

I ran only `make_report()` from your current generator against Ali's copy of the supplied template, directing all output to a private QA directory. I then rendered the generated DOCX with the packaged document renderer and visually inspected **all 11 pages**, alongside all 4 pages of the untouched template. The logo, current names/instructor, figure and in-text reference, hierarchy explanation, both students' AI disclosure, and complete bibliography are present. I did not see clipped/overlapping content. The public video placeholder and old sphere-performance measurement remain expected pending integration items; this is not a final submission sign-off.

Please consider these small final-export improvements in your owned generator:

- `paragraph.text = value` removes the cover labels' bold formatting. Edit the value runs while preserving the bold labels if you want the cover to retain the template treatment.
- `add_heading()` inherits blue, larger built-in headings, whereas the supplied body template has black Times New Roman bold headings. Set the heading styles explicitly or clone the template's heading formatting. The contents-page title is also much larger than the template's.
- The contents list has only top-level headings and no page numbers. This is readable, but adding the final section/subsection page numbers would help navigation in the 11-page report.
- The direct LibreOffice subprocess exited unsuccessfully in Ali's sandbox even though the packaged `render_docx.py --emit_pdf` path generated a readable PDF. Retain stderr and raise on conversion failure; do not treat printed success for the other files as proof that a PDF was exported. The hardcoded template path also needs overriding on a second machine.
- Re-render after inserting the real public video URL and updating performance; inspect the reference wraps and the Figure 1 caption again because those edits can change pagination.
- The current video card sequence in `make_demo_video.py` covers fixed update, collision, shaders and wave tests, but has no hierarchical-boss code card. Add a short `main.cpp` parent/orbit/satellite/beacon walkthrough, and ensure the final video uses the optimized renderer. Label scripted captures honestly, as your notes already do.

The optimized renderer also passed the wave-1 and wave-2 360-frame OpenGL checks, in addition to the repeated wave-3 checks documented above.

## Source archive and final-file checks

The current ten-file source archive was independently CRC-checked, compared byte-for-byte with the optimized checkout, extracted into a clean directory, configured/built in Release mode, and passed CTest there. All four shader files are present; no repository credentials or build outputs are included.

While awaiting integration, Ali added the optional read-only `tools/check_submission.py` helper. Run `python tools/check_submission.py /path/to/exported/files` with `pypdf` installed. It checks the named PDF, ten-slide PPTX and source ZIP, rejects unresolved template/video placeholders, checks that the PDF and slides share a recognizable YouTube video ID, and verifies the ZIP's required source/shaders and CRCs. It reads PPTX XML without requiring python-pptx. It does not verify public YouTube visibility, document layout, source behavior or a human playtest. On the actual incomplete local report draft, it correctly rejected the public-video placeholder and missing presentation while accepting the intact source ZIP. Please use it after final export as an additional file check, not as a final-submission sign-off.

## Availability handoff — 2026-11-09

Ali reports that this helper AI is running out of credits and therefore cannot continue working. Please continue integration and the remaining submission work without waiting for further replies from this helper.

The completed work is pushed on `ali/sphere-performance` in [PR #2](https://github.com/Csadow/our-game-continued/pull/2), including the sphere optimization, measured before/after results, optimized screenshot, report-layout review, source-archive validation and optional final-file checker. Please review the latest branch contents and integrate what you accept. The initial hierarchical rendering work was already merged through PR #1.

Outstanding items include reviewing/merging PR #2, remeasuring the optimized build on the integration machine, regenerating/reviewing the final report, slides and demo, completing the human playtest, and publishing the 3–6 minute YouTube demo with Public visibility. Ali does not know of an existing public demo URL. Insert the real URL in the PDF and slides after upload, then verify the three separate submission files. The project is not being marked complete by this handoff.
