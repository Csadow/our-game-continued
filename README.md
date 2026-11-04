# Orbit Bullet Hell

A small C++17 and OpenGL 3.3 survival game. Move around the arena, dodge the boss's aimed fans and radial volleys, and survive for 60 seconds. The round has three waves, with faster and denser attacks in later waves.

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

The HUD shows health, score, round progress, and dash readiness. A dash requires a movement direction. Getting hit removes one health point and gives a brief grace period. The round ends when health reaches zero or the timer reaches 60 seconds.

## Checks

```sh
ctest --test-dir build --output-on-failure
```

`bullethell --smoke-test` runs a short rendering check when an OpenGL display is available. Add `--screenshot output.ppm` to save its final frame.

## Contributors

This repository keeps the original commit history from [`at254135/our-game`](https://github.com/at254135/our-game), including work by Ali and Muhammad. Keep each new commit under the identity of the person who actually made the change so both contributors receive accurate credit.
