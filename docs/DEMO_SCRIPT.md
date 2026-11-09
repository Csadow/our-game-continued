# Demonstration video plan

The local draft is `../our-game-submission-editable/Orbit_Bullet_Hell_Demo_Draft.mp4`. It is about 3 minutes 30 seconds and contains a genuine OpenGL gameplay capture followed by actual C++ and GLSL source excerpts. The recording shows movement, projectile patterns, pause, game over, and restart. The team should review the final rendering version, add spoken explanation if desired, and upload the video to YouTube with **Public** visibility. Put its exact URL in both the editable report and the presentation before exporting the final PDF.

| Time | On screen | Suggested explanation |
| --- | --- | --- |
| 0:00–0:12 | Title and controls | State the goal: survive 60 seconds in three waves. |
| 0:12–1:25 | Actual game capture | Point out player, boss, aimed/red shots, radial/gold shots, HUD, pause, and restart. |
| 1:25–1:48 | Fixed update | Explain `Game::update`, fixed 1/120-second step, and normalized movement. |
| 1:48–2:11 | Collision | Explain squared-distance hit check and why it is simple enough here. |
| 2:11–2:34 | Vertex shader | Explain model, view, and projection matrices. |
| 2:34–2:57 | Fragment shader | Explain ambient, diffuse, specular, and emission. |
| 2:57–3:20 | Game tests | Explain checks for wave 2 and wave 3. |
| 3:20–3:32 | Closing | Mention the report's performance measurement, sources, and AI-use disclosure. |

The capture is silent so students can narrate in their own words. It is a local draft until the integrated rendering pass is recorded and the final YouTube link is inserted. A plain screen recording is enough if the team prefers to record a live explanation instead.

To reproduce on a Linux virtual display, build the game, install `python-xlib`, Pillow, ffmpeg, and Xvfb, then run `tools/record_gameplay.py` inside `xvfb-run` followed by `tools/make_demo_video.py`. The recording script intentionally resumes play after Xvfb's initial focus event. The code cards are generated from the current source so the walkthrough matches the build.
