# Orbit Bullet Hell: development plan

## Design and core

**Goal:** a small, understandable C++17/OpenGL 3.3 game for Computer Graphics Fundamentals (OKG 2214). The player survives a 60-second boss encounter in a 3D arena. Keyboard movement, slow movement, dash, collision, health, and near-miss scoring make the rendered scene interactive. Three 20-second waves increase pressure. The visual style uses simple meshes and a limited palette so the graphics techniques remain easy to explain in a code walkthrough.

**Current core:** GLFW window and input; GLEW and GLSL shaders; GLM model/view/projection matrices; VAO/VBO meshes; perspective camera; depth testing; a textured checkerboard floor; ambient/diffuse/specular shading; animated boss; aimed and radial shots; health, score, pause, restart, win/lose; fixed-step gameplay checks. Do not replace this with a large engine or external asset pack.

## Course alignment

| Syllabus / lecture topic | Evidence in this project | Next work |
| --- | --- | --- |
| Modern OpenGL pipeline, shaders (L1–L2) | VAO/VBO meshes, vertex and fragment shaders | Explain CPU-to-GPU data flow in report and slides |
| Input and animation (L3) | GLFW keyboard events, fixed-step movement, pause | Make controls and start/end states clear |
| Geometry and transforms (L3–L4) | Cube/sphere/floor vertices, model matrices | Hierarchical boss assembly, with a parent transform and child parts |
| Viewing and projection (L5-1) | `lookAt` view and perspective projection | Document camera coordinates and aspect handling |
| Shading (L5-2) | Ambient, diffuse, specular, emission | Refine readable lighting and explain the equations |
| Pixels, buffers, blending (L7) | Depth buffer, blended HUD, screenshot readback | Document depth/blend order and screenshot path |
| Texture mapping (L8) | UV-mapped checkerboard texture and grid shader | Improve texture filtering if it benefits the scene |
| Hierarchical models (L9) | Boss parent, orbit pivots, satellites, and beacon children inherit transforms | Explain parent/local matrix composition in report and demo |
| Procedural methods (L10) | Procedural checkerboard and time-based attack patterns | Add one restrained time-based visual effect if performance allows |

The syllabus requires a buildable repository, a 3–6 minute demo, a report using the course template, and a slide deck. Its grading emphasizes technical correctness, visual quality/performance, interaction, documentation, report, and presentation. The submission instruction requires **three separate files**: presentation, PDF report containing a public YouTube demonstration link, and source ZIP. The supplied report template requires Introduction, Literature Review, Project Description, Technical Implementation, Graphics and Rendering, Testing and Evaluation, Conclusion and Future Work, References, and an optional Appendix. It explicitly asks for at least **15 sources from credible Q1/Q2 journals** in the literature review, performance evaluation, and a figure citation in the surrounding text.

## Milestones and ownership

1. **Plan and integration baseline (Muhammad):** keep original history, record this plan, build and test, coordinate file ownership. Done when the plan is committed and Ali can read it.
2. **Graphics and model (Ali):** own `main.cpp`, `scene.vert`, and `scene.frag`. Make the boss a clear hierarchical model; improve visual feedback and polish while keeping OpenGL 3.3 and simple readable code. Describe what changed in `docs/coordination/from-ali.md` and commit under Ali's real identity. The hierarchy, wave visual pass, and sphere-mesh optimization are merged and tested.
3. **Gameplay (Mukhammed):** own `game.h`, `game.cpp`, and `game_tests.cpp`. Make waves mechanically distinct and ensure win/loss, dash, grazing, bounds, and pause remain correct. Complete and tested.
4. **Integration (Mukhammed with Ali):** pull both sets of commits, resolve any conflicts, run CMake build, `ctest`, and the Xvfb OpenGL smoke test. Review the screenshot together. Measure a simple frame rate in the report, with hardware and method stated. Build, CTest, and all three wave smoke checks pass after the mesh optimization; the final-build software-rendering result is in the report.
5. **Submission (both):** record a 3–6 minute demonstration, publish it publicly on YouTube, and put its exact URL in the PDF report. Prepare a slide deck, PDF report following the supplied template, and source ZIP as separate files. Verify at least 15 relevant Q1/Q2 journal articles for the literature review; cite the supplied lectures where used. List actual contributions and include a truthful AI-use disclosure. The separate draft files and 4:23 local demo are prepared. Public upload, URL insertion, and each student's personal review remain before submission.

## Scope and acceptance checks

- Gameplay remains a complete, playable 60-second round with three visibly distinct waves, clear controls, HUD, restart, and success/failure screens.
- The code builds with CMake and common OpenGL/GLFW/GLEW/GLM packages. Gameplay checks and a 360-frame OpenGL smoke test pass.
- Any new mechanic is simple enough to teach from the source, and its behavior is checked by a meaningful test.
- Presentation and report show screenshots of the actual build, explain the graphics pipeline and design choices, state limitations honestly, cite the supplied lectures and any external sources, and include AI-use disclosure.
- The ZIP contains source, shaders, README, and CMake files; generated build outputs and local dependencies stay out.

## Repository coordination

Read [coordination/README.md](coordination/README.md). Do not amend or author commits for the other person. Equal contribution should come from actual work, not manufactured commits. Before starting a file shared with another owner, leave a note and pull the newest `main`.
