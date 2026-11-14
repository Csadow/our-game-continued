# Demonstration video plan

The local draft is `../../our-game-submission-editable/Orbit_Bullet_Hell_Demo_Draft.mp4`. It is 4 minutes 23 seconds long and contains a genuine OpenGL gameplay capture, two labeled wave-check frames, and actual C++ and GLSL source excerpts. The recording shows movement, projectile patterns, pause, game over, and restart. The wave 2/3 frames use a test shortcut that starts at their wave boundaries; they are clearly labeled, and no full player survival is claimed. The team should review the final rendering version, add spoken explanation if desired, and upload the video to YouTube with **Public** visibility. To insert its URL in both the report and presentation, rerun `tools/make_submission.py` with `OUR_GAME_YOUTUBE_URL=https://youtu.be/YOUR_REAL_ID` set. Alternatively edit the DOCX and PPTX, then export the PDF again. The three files in the submission folder are drafts until this is done.

| Time | On screen | Suggested explanation |
| --- | --- | --- |
| 0:00–0:12 | Title and controls | State the goal: survive 60 seconds in three waves. |
| 0:12–1:25 | Actual game capture | Point out player, boss, aimed/red shots, radial/gold shots, HUD, pause, and restart. |
| 1:25–1:39 | Wave 2 smoke frame | Explain blue palette and cyan stream; state this starts at the 20-second boundary. |
| 1:39–1:53 | Wave 3 smoke frame | Explain magenta palette and opposite streams; state this starts at the 40-second boundary. |
| 1:53–2:16 | Fixed update | Explain `Game::update`, fixed 1/120-second step, and normalized movement. |
| 2:16–2:39 | Collision | Explain squared-distance hit check and why it is simple enough here. |
| 2:39–3:02 | Vertex shader | Explain model, view, and projection matrices. |
| 3:02–3:25 | Hierarchical boss | Show Ali's parent, orbit pivot, satellite, and beacon matrices. |
| 3:25–3:48 | Fragment shader | Explain ambient, diffuse, specular, and emission. |
| 3:48–4:11 | Game tests | Explain checks for wave 2 and wave 3. |
| 4:11–4:23 | Closing | Mention the report's performance measurement, sources, and AI-use disclosure. |

The capture is silent so students can narrate in their own words. It is a local draft until the integrated rendering pass is recorded and the final YouTube link is inserted. A plain screen recording is enough if the team prefers to record a live explanation instead.

To reproduce on a Linux virtual display, build the game, install `python-xlib`, Pillow, ffmpeg, and Xvfb, then run `tools/record_gameplay.py` inside `xvfb-run` followed by `tools/make_demo_video.py`. The recording script intentionally resumes play after Xvfb's initial focus event. The code cards are generated from the current source so the walkthrough matches the build.
