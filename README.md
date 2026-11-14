# Orbit Bullet Hell

A small C++17 and OpenGL 3.3 survival game. Move around the arena, dodge the boss's aimed fans and radial volleys, and survive for 60 seconds. Wave two adds a rotating projectile stream; wave three fires opposite streams with a faster rhythm.

The boss is a hierarchical model: its core, orbiting satellites, and small beacon children inherit a parent transform. The arena and HUD change from amber to blue to magenta across the waves. Cyan shots mark the rotating stream.
The player and projectiles share a low-detail sphere mesh with smooth normals, keeping the projectile-heavy final wave responsive.

## Build and run

Install a C++17 compiler, CMake 3.16 or newer, OpenGL development files, GLFW 3.3 or newer, GLEW, and GLM. On Arch Linux, the library packages are `glfw`, `glew`, and `glm`.

```sh
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
./build/bullethell
```

On Windows, run `build/bullethell.exe` after building with an installed GLFW, GLEW, GLM, and OpenGL toolchain. CMake copies the shaders beside the executable.

## Controls

| Key | Action |
| --- | --- |
| W A S D | Move |
| Shift | Move slowly for precise dodging |
| Space | Dash in the held movement direction; briefly avoid damage, then wait for the cooldown |
| P | Pause or resume |
| R | Restart |
| Esc | Quit |

The HUD shows health, score, round progress, dash readiness, and near misses. A dash requires a movement direction. Passing close to a bullet without touching it earns 50 bonus points once per bullet. A dash or damage grace period cannot earn near miss points. Getting hit removes one health point and gives a brief grace period. The round ends when health reaches zero or the timer reaches 60 seconds.

## Checks

```sh
ctest --test-dir build --output-on-failure
```

`bullethell --smoke-test` runs a short rendering check when an OpenGL display is available. Use `--smoke-wave 1`, `2`, or `3` to start that check at a wave boundary; this does not change normal play. Add `--screenshot output.ppm` to save its final frame.

On a headless Linux machine with Xvfb installed, run the rendering check on a virtual display:

```sh
env -u WAYLAND_DISPLAY LIBGL_ALWAYS_SOFTWARE=1 xvfb-run -a -s '-screen 0 1280x800x24 -nolisten tcp' \
  ./build/bullethell --smoke-test --screenshot smoke.ppm
```

## Contributors

Mukhammed Sailau developed the gameplay, tests, integration, and project documents. Ali Turlas developed the hierarchical boss, wave visuals, and sphere-mesh optimization. This repository preserves their original commit history from [`at254135/our-game`](https://github.com/at254135/our-game).

## AI use

Both students used Codex during development for planning, code, testing, and documentation. They are responsible for reviewing, testing, and explaining the submitted work. The report and presentation also disclose this assistance.
