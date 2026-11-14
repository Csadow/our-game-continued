# Orbit Bullet Hell: development plan

## Design and core

**Goal:** a small, understandable C++17/OpenGL 3.3 game for Computer Graphics Fundamentals (OKG 2214). The player survives a 60-second boss encounter in a 3D arena. Keyboard movement, slow movement, dash, collision, health, and near-miss scoring make the rendered scene interactive. Three 20-second waves increase pressure. The visual style uses simple meshes and a limited palette so the graphics techniques remain easy to explain in a code walkthrough.

**Implementation:** GLFW window and input; GLEW and GLSL shaders; GLM model/view/projection matrices; VAO/VBO meshes; perspective camera; depth testing; a textured checkerboard floor; ambient/diffuse/specular shading; animated boss; aimed, radial, and rotating shots; health, score, pause, restart, win/lose; fixed-step gameplay checks. The project uses no game engine or external asset pack.

## Course alignment

| Syllabus / lecture topic | Evidence in this project |
| --- | --- |
| Modern OpenGL pipeline, shaders (L1–L2) | VAO/VBO meshes and vertex/fragment shaders; CPU-to-GPU flow explained in the report |
| Input and animation (L3) | GLFW keyboard events, fixed-step movement, pause, and start/end states |
| Geometry and transforms (L3–L4) | Cube/sphere/floor vertices and model matrices for the boss and projectiles |
| Viewing and projection (L5-1) | `lookAt` view and perspective projection with window aspect handling |
| Shading (L5-2) | Ambient, diffuse, specular, and emission terms in the fragment shader |
| Pixels, buffers, blending (L7) | Depth buffer, blended HUD, and screenshot readback |
| Texture mapping (L8) | UV-mapped checkerboard texture and a world-space grid |
| Hierarchical models (L9) | Boss parent, orbit pivots, satellites, and beacon children inherit transforms |
| Procedural methods (L10) | Generated checkerboard, grid effect, and time-based attack patterns |

The syllabus requires a buildable repository, a 3–6 minute demo, a report using the course template, and a slide deck. Its grading emphasizes technical correctness, visual quality/performance, interaction, documentation, report, and presentation. The submission instruction requires **three separate files**: presentation, PDF report containing a public YouTube demonstration link, and source ZIP. The supplied report template requires Introduction, Literature Review, Project Description, Technical Implementation, Graphics and Rendering, Testing and Evaluation, Conclusion and Future Work, References, and an optional Appendix. It explicitly asks for at least **15 sources from credible Q1/Q2 journals** in the literature review, performance evaluation, and a figure citation in the surrounding text.

## Development milestones

1. **Core game:** a playable round, movement, collision, health, score, pause, restart, and win/loss states.
2. **Gameplay extensions:** dash, near-miss scoring, and three distinct 20-second attack waves.
3. **Graphics:** a hierarchical boss, wave colors, a textured floor, lighting, HUD, and a smaller sphere mesh for projectile-heavy scenes.
4. **Integration and checks:** CMake build, rules tests, three OpenGL wave smoke checks, screenshots, and a documented software-rendering measurement.
5. **Submission:** separate presentation, PDF report, and source ZIP have been prepared as drafts. The team still needs to publish the 4:23 demonstration publicly, insert its real YouTube URL, regenerate the PDF and slides, and personally review the final files before submitting.

## Scope and acceptance checks

- Gameplay remains a complete, playable 60-second round with three visibly distinct waves, clear controls, HUD, restart, and success/failure screens.
- The code builds with CMake and common OpenGL/GLFW/GLEW/GLM packages. Gameplay checks and a 360-frame OpenGL smoke test pass.
- Any new mechanic is simple enough to teach from the source, and its behavior is checked by a meaningful test.
- Presentation and report show screenshots of the actual build, explain the graphics pipeline and design choices, state limitations honestly, cite the supplied lectures and any external sources, and include AI-use disclosure.
- The ZIP contains source, shaders, README, and CMake files; generated build outputs and local dependencies stay out.

## Contributions

Mukhammed developed the gameplay and tests and integrated the release documents. Ali developed the boss hierarchy, wave visuals, and sphere-mesh optimization. The repository preserves the original commit history and each contributor's authored changes.
