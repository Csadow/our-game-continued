# Coordination through GitHub

This folder is the handoff between Muhammad's and Ali's AI agents. Pull `main` before work; read the plan and latest notes. Use real author identity and preserve the original commit history.

## Working agreement

1. Muhammad leads integration and submission. He owns `game.h`, `game.cpp`, `game_tests.cpp`, and the release documents.
2. Ali owns `main.cpp`, `scene.vert`, and `scene.frag` for the rendering pass. The first task is in [to-ali.md](to-ali.md).
3. Ali replies in `from-ali.md` with his agent's understanding, decisions, and test result, then pushes his own commits. If he needs a gameplay API change, request it there before editing Muhammad's files.
4. Each agent pulls before pushing. Prefer a feature branch and a pull request for larger changes. Never force-push `main`.
5. AI assistance must be disclosed in the report/README; students review and understand the submitted work. Do not fabricate authorship, performance numbers, screenshots, or a YouTube URL.

## Current integration status

- Starting base: `aa9f10c` on `main`, preserving Ali's and Muhammad's original work.
- Build and unit checks passed in the earlier session. A 360-frame OpenGL smoke test passed on an isolated Xvfb display with Mesa software rendering.
- Next: Ali's hierarchy/visual pass and Muhammad's wave mechanics, then a joint review and submission artifacts.
