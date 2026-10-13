#ifdef _WIN32
#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif
#endif

#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>

#include "game.h"

#include <algorithm>
#include <array>
#include <cmath>
#include <cstddef>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <iterator>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>

#ifdef _WIN32
#include <windows.h>
#endif

namespace fs = std::filesystem;

struct Vertex {
    glm::vec3 position;
    glm::vec3 normal;
    glm::vec2 uv;
};

struct Mesh {
    GLuint vao = 0;
    GLuint vbo = 0;
    GLsizei count = 0;

    void create(const std::vector<Vertex>& vertices) {
        count = static_cast<GLsizei>(vertices.size());
        glGenVertexArrays(1, &vao);
        glGenBuffers(1, &vbo);
        glBindVertexArray(vao);
        glBindBuffer(GL_ARRAY_BUFFER, vbo);
        glBufferData(GL_ARRAY_BUFFER, vertices.size() * sizeof(Vertex), vertices.data(), GL_STATIC_DRAW);
        glEnableVertexAttribArray(0);
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, sizeof(Vertex),
                              reinterpret_cast<void*>(offsetof(Vertex, position)));
        glEnableVertexAttribArray(1);
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, sizeof(Vertex),
                              reinterpret_cast<void*>(offsetof(Vertex, normal)));
        glEnableVertexAttribArray(2);
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, sizeof(Vertex),
                              reinterpret_cast<void*>(offsetof(Vertex, uv)));
    }

    void destroy() {
        glDeleteBuffers(1, &vbo);
        glDeleteVertexArrays(1, &vao);
    }
};

std::string readFile(const fs::path& path) {
    std::ifstream file(path);
    if (!file)
        throw std::runtime_error("Cannot open shader: " + path.string());
    return std::string(std::istreambuf_iterator<char>(file), std::istreambuf_iterator<char>());
}

GLuint compileShader(GLenum type, const fs::path& path) {
    std::string source = readFile(path);
    const char* text = source.c_str();
    GLuint shader = glCreateShader(type);
    glShaderSource(shader, 1, &text, nullptr);
    glCompileShader(shader);
    GLint ok = GL_FALSE;
    glGetShaderiv(shader, GL_COMPILE_STATUS, &ok);
    if (!ok) {
        GLint length = 0;
        glGetShaderiv(shader, GL_INFO_LOG_LENGTH, &length);
        std::string log(static_cast<std::size_t>(std::max(1, length)), '\0');
        glGetShaderInfoLog(shader, length, nullptr, log.data());
        glDeleteShader(shader);
        throw std::runtime_error(path.filename().string() + ":\n" + log);
    }
    return shader;
}

GLuint makeProgram(const fs::path& vertexPath, const fs::path& fragmentPath) {
    GLuint vertex = compileShader(GL_VERTEX_SHADER, vertexPath);
    GLuint fragment = 0;
    try {
        fragment = compileShader(GL_FRAGMENT_SHADER, fragmentPath);
    } catch (...) {
        glDeleteShader(vertex);
        throw;
    }
    GLuint program = glCreateProgram();
    glAttachShader(program, vertex);
    glAttachShader(program, fragment);
    glLinkProgram(program);
    glDeleteShader(vertex);
    glDeleteShader(fragment);
    GLint ok = GL_FALSE;
    glGetProgramiv(program, GL_LINK_STATUS, &ok);
    if (!ok) {
        GLint length = 0;
        glGetProgramiv(program, GL_INFO_LOG_LENGTH, &length);
        std::string log(static_cast<std::size_t>(std::max(1, length)), '\0');
        glGetProgramInfoLog(program, length, nullptr, log.data());
        glDeleteProgram(program);
        throw std::runtime_error("Shader link error:\n" + log);
    }
    return program;
}

std::vector<Vertex> cubeVertices() {
    std::vector<Vertex> vertices;
    auto face = [&](glm::vec3 a, glm::vec3 b, glm::vec3 c, glm::vec3 d, glm::vec3 normal) {
        vertices.insert(vertices.end(), {
            {a, normal, {0, 0}}, {b, normal, {1, 0}}, {c, normal, {1, 1}},
            {a, normal, {0, 0}}, {c, normal, {1, 1}}, {d, normal, {0, 1}}
        });
    };
    face({-.5f,-.5f,.5f}, {.5f,-.5f,.5f}, {.5f,.5f,.5f}, {-.5f,.5f,.5f}, {0,0,1});
    face({.5f,-.5f,-.5f}, {-.5f,-.5f,-.5f}, {-.5f,.5f,-.5f}, {.5f,.5f,-.5f}, {0,0,-1});
    face({.5f,-.5f,.5f}, {.5f,-.5f,-.5f}, {.5f,.5f,-.5f}, {.5f,.5f,.5f}, {1,0,0});
    face({-.5f,-.5f,-.5f}, {-.5f,-.5f,.5f}, {-.5f,.5f,.5f}, {-.5f,.5f,-.5f}, {-1,0,0});
    face({-.5f,.5f,.5f}, {.5f,.5f,.5f}, {.5f,.5f,-.5f}, {-.5f,.5f,-.5f}, {0,1,0});
    face({-.5f,-.5f,-.5f}, {.5f,-.5f,-.5f}, {.5f,-.5f,.5f}, {-.5f,-.5f,.5f}, {0,-1,0});
    return vertices;
}

std::vector<Vertex> sphereVertices() {
    const int rows = 20;
    const int columns = 28;
    std::vector<Vertex> vertices;
    auto point = [](float u, float v) -> Vertex {
        float a = u * 6.2831853f;
        float b = v * 3.1415927f;
        glm::vec3 p(std::sin(b) * std::cos(a), std::cos(b), std::sin(b) * std::sin(a));
        return {p, p, {u, v}};
    };
    for (int y = 0; y < rows; ++y) {
        for (int x = 0; x < columns; ++x) {
            float u = static_cast<float>(x) / columns;
            float v = static_cast<float>(y) / rows;
            float du = 1.0f / columns;
            float dv = 1.0f / rows;
            vertices.insert(vertices.end(), {
                point(u,v), point(u+du,v), point(u+du,v+dv),
                point(u,v), point(u+du,v+dv), point(u,v+dv)
            });
        }
    }
    return vertices;
}

GLuint makeFloorTexture() {
    constexpr int size = 64;
    std::vector<unsigned char> pixels(size * size * 3);
    for (int y = 0; y < size; ++y) {
        for (int x = 0; x < size; ++x) {
            bool checker = ((x / 32) + (y / 32)) % 2 == 0;
            int i = (y * size + x) * 3;
            pixels[i] = checker ? 34 : 24;
            pixels[i + 1] = checker ? 47 : 35;
            pixels[i + 2] = checker ? 58 : 45;
        }
    }
    GLuint texture = 0;
    glGenTextures(1, &texture);
    glBindTexture(GL_TEXTURE_2D, texture);
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB8, size, size, 0, GL_RGB, GL_UNSIGNED_BYTE, pixels.data());
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
    return texture;
}

void saveScreenshot(const fs::path& path, int width, int height) {
    std::vector<unsigned char> pixels(static_cast<std::size_t>(width) * height * 3);
    glPixelStorei(GL_PACK_ALIGNMENT, 1);
    glReadBuffer(GL_BACK);
    glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE, pixels.data());
    std::ofstream file(path, std::ios::binary);
    if (!file)
        throw std::runtime_error("Cannot write screenshot: " + path.string());
    file << "P6\n" << width << " " << height << "\n255\n";
    for (int row = height - 1; row >= 0; --row)
        file.write(reinterpret_cast<const char*>(pixels.data() + row * width * 3), width * 3);
    if (!file)
        throw std::runtime_error("Screenshot write failed: " + path.string());
}

fs::path executableDirectory(const char* argument) {
#ifdef _WIN32
    std::wstring path(32768, L'\0');
    DWORD length = GetModuleFileNameW(nullptr, path.data(), static_cast<DWORD>(path.size()));
    if (length == 0 || length >= path.size())
        throw std::runtime_error("Cannot locate executable directory.");
    path.resize(length);
    (void)argument;
    return fs::path(path).parent_path();
#else
    return fs::absolute(argument).parent_path();
#endif
}

int run(GLFWwindow* window, const fs::path& directory, bool smokeTest, const fs::path& screenshot) {
    glewExperimental = GL_TRUE;
    GLenum result = glewInit();
    if (result != GLEW_OK)
        throw std::runtime_error(reinterpret_cast<const char*>(glewGetErrorString(result)));
    // GLEW may probe a removed extension enum while initializing a core context.
    while (glGetError() != GL_NO_ERROR) {}
    std::cout << "OpenGL " << glGetString(GL_VERSION) << "\nGPU: " << glGetString(GL_RENDERER)
              << "\nWASD move | Shift slow | P pause | R restart | Esc quit\n";

    GLuint program = makeProgram(directory / "scene.vert", directory / "scene.frag");
    GLint modelLocation = glGetUniformLocation(program, "model");
    GLint viewLocation = glGetUniformLocation(program, "view");
    GLint projectionLocation = glGetUniformLocation(program, "projection");
    GLint colorLocation = glGetUniformLocation(program, "baseColor");
    GLint emissionLocation = glGetUniformLocation(program, "emission");
    GLint texturedLocation = glGetUniformLocation(program, "textured");
    Mesh cube, sphere, floor;
    cube.create(cubeVertices());
    sphere.create(sphereVertices());
    floor.create({
        {{-1,0,-1},{0,1,0},{0,0}}, {{1,0,1},{0,1,0},{1,1}}, {{1,0,-1},{0,1,0},{1,0}},
        {{-1,0,-1},{0,1,0},{0,0}}, {{-1,0,1},{0,1,0},{0,1}}, {{1,0,1},{0,1,0},{1,1}}
    });
    GLuint texture = makeFloorTexture();

    Game game;
    glfwSetWindowUserPointer(window, &game);
    glfwSetWindowFocusCallback(window, [](GLFWwindow* w, int focused) {
        auto* state = static_cast<Game*>(glfwGetWindowUserPointer(w));
        if (!focused && !state->finished())
            state->paused = true;
    });
    glEnable(GL_DEPTH_TEST);
    glClearColor(0.025f, 0.035f, 0.055f, 1.0f);
    bool previousPause = false;
    bool previousRestart = false;
    double lastTime = glfwGetTime();
    double accumulator = 0.0;
    int frames = 0;

    while (!glfwWindowShouldClose(window)) {
        glfwPollEvents();
        auto down = [&](int key) { return glfwGetKey(window, key) == GLFW_PRESS; };
        if (down(GLFW_KEY_ESCAPE))
            glfwSetWindowShouldClose(window, GLFW_TRUE);
        bool pause = down(GLFW_KEY_P);
        bool restart = down(GLFW_KEY_R);
        if (pause && !previousPause && !game.finished())
            game.paused = !game.paused;
        if (restart && !previousRestart) {
            game.reset();
            accumulator = 0.0;
        }
        previousPause = pause;
        previousRestart = restart;
        Input input;
        input.x = static_cast<float>(down(GLFW_KEY_D)) - static_cast<float>(down(GLFW_KEY_A));
        input.z = static_cast<float>(down(GLFW_KEY_S)) - static_cast<float>(down(GLFW_KEY_W));
        input.slow = down(GLFW_KEY_LEFT_SHIFT) || down(GLFW_KEY_RIGHT_SHIFT);

        int width = 0, height = 0;
        glfwGetFramebufferSize(window, &width, &height);
        if (width == 0 || height == 0) {
            glfwWaitEventsTimeout(0.1);
            lastTime = glfwGetTime();
            accumulator = 0.0;
            continue;
        }
        double now = glfwGetTime();
        double dt = smokeTest ? 1.0 / 60.0 : std::min(now - lastTime, 0.1);
        lastTime = now;
        if (smokeTest) {
            input.x = frames % 240 < 120 ? 0.45f : -0.45f;
            input.slow = true;
        }
        accumulator += dt;
        while (accumulator >= FIXED_STEP) {
            game.update(FIXED_STEP, input);
            accumulator -= FIXED_STEP;
        }

        glViewport(0, 0, width, height);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        glUseProgram(program);
        float aspect = static_cast<float>(width) / height;
        // Widen the vertical field at narrow aspect ratios to keep the whole floor visible.
        float fieldOfView = aspect < 1.5f ? 55.0f : 48.0f;
        glm::vec3 camera(0.0f, 17.0f, 18.5f);
        glm::mat4 projection = glm::perspective(glm::radians(fieldOfView), aspect, 0.1f, 100.0f);
        glm::mat4 view = glm::lookAt(camera, glm::vec3(0,-0.1f,-0.4f), glm::vec3(0,1,0));
        glUniformMatrix4fv(viewLocation, 1, GL_FALSE, glm::value_ptr(view));
        glUniformMatrix4fv(projectionLocation, 1, GL_FALSE, glm::value_ptr(projection));
        glUniform3fv(glGetUniformLocation(program, "cameraPosition"), 1, glm::value_ptr(camera));
        glUniform3f(glGetUniformLocation(program, "lightPosition"), -3.0f, 10.0f, 3.0f);
        glActiveTexture(GL_TEXTURE0);
        glBindTexture(GL_TEXTURE_2D, texture);
        glUniform1i(glGetUniformLocation(program, "floorTexture"), 0);

        auto draw = [&](const Mesh& mesh, glm::vec3 position, glm::vec3 size,
                        glm::vec3 color, float emission = 0.0f, float rotation = 0.0f,
                        float tilt = 0.0f, bool textured = false) {
            glm::mat4 model = glm::translate(glm::mat4(1.0f), position);
            model = glm::rotate(model, rotation, glm::vec3(0,1,0));
            model = glm::rotate(model, tilt, glm::vec3(1,0,0));
            model = glm::scale(model, size);
            glUniformMatrix4fv(modelLocation, 1, GL_FALSE, glm::value_ptr(model));
            glUniform3fv(colorLocation, 1, glm::value_ptr(color));
            glUniform1f(emissionLocation, emission);
            glUniform1i(texturedLocation, textured ? 1 : 0);
            glBindVertexArray(mesh.vao);
            glDrawArrays(GL_TRIANGLES, 0, mesh.count);
        };

        draw(cube, {0,-.18f,0}, {18.3f,.32f,14.3f}, {.18f,.17f,.15f});
        draw(floor, {0,.005f,0}, {ARENA_X,1,ARENA_Z}, {1,1,1}, 0, 0, 0, true);
        glm::vec3 border(.08f,.40f,.46f);
        for (float side : {-1.0f, 1.0f}) {
            draw(cube, {side * ARENA_X,.08f,0}, {.10f,.16f,14.1f}, border);
            draw(cube, {0,.08f,side * ARENA_Z}, {18.1f,.16f,.10f}, border);
            for (float z : {-ARENA_Z, ARENA_Z}) {
                draw(cube, {side * ARENA_X,.35f,z}, {.20f,.70f,.20f}, {.25f,.24f,.22f});
                draw(sphere, {side * ARENA_X,.76f,z}, {.10f,.10f,.10f}, {.65f,.58f,.40f}, .15f);
            }
        }

        draw(cube, game.enemy + glm::vec3(0,.85f,0), {.85f,.85f,.85f}, {.7f,.1f,.2f});
        for (const Bullet& bullet : game.bullets) {
            glm::vec3 color = bullet.aimed ? glm::vec3(1.0f,.32f,.08f) : glm::vec3(.88f,.12f,.45f);
            draw(sphere, bullet.position, glm::vec3(BULLET_RADIUS), color, .75f);
            glm::vec3 tail = bullet.position - glm::normalize(bullet.velocity) * .23f;
            draw(sphere, tail, glm::vec3(BULLET_RADIUS * .5f), color * .6f, .4f);
        }

        bool blink = game.invulnerable > 0.0f && static_cast<int>(game.invulnerable * 12) % 2 == 0;
        glm::vec3 playerColor = blink ? glm::vec3(.65f,.68f,.73f) : glm::vec3(.12f,.8f,.95f);
        draw(sphere, {game.player.x,.04f,game.player.z}, {.42f,.025f,.42f}, {.03f,.30f,.37f}, .4f);
        draw(sphere, game.player, glm::vec3(PLAYER_RADIUS), playerColor, .25f);
        draw(cube, game.player + glm::vec3(0,.30f,0), {.15f,.15f,.15f}, {.8f,1,1}, .6f, game.elapsed);

        if (smokeTest) {
            GLenum error = glGetError();
            if (error != GL_NO_ERROR)
                throw std::runtime_error("OpenGL error during smoke test: " + std::to_string(error));
            if (frames == 359 && !screenshot.empty())
                saveScreenshot(screenshot, width, height);
        }
        glfwSwapBuffers(window);
        ++frames;
        if (smokeTest && frames >= 360)
            glfwSetWindowShouldClose(window, GLFW_TRUE);
    }

    if (smokeTest)
        std::cout << "Smoke test passed: " << frames << " frames, " << game.bullets.size()
                  << " active projectiles, HP " << game.health << ", time " << game.elapsed << "\n";
    floor.destroy();
    sphere.destroy();
    cube.destroy();
    glDeleteTextures(1, &texture);
    glDeleteProgram(program);
    return 0;
}

int main(int argc, char** argv) {
    bool smokeTest = false;
    fs::path screenshot;
    for (int i = 1; i < argc; ++i) {
        std::string argument = argv[i];
        if (argument == "--smoke-test")
            smokeTest = true;
        else if (argument == "--screenshot" && i + 1 < argc)
            screenshot = argv[++i];
        else {
            std::cerr << "Usage: bullethell [--smoke-test] [--screenshot output.ppm]\n";
            return 1;
        }
    }
    if (!screenshot.empty() && !smokeTest) {
        std::cerr << "Use --screenshot together with --smoke-test.\n";
        return 1;
    }
    glfwSetErrorCallback([](int code, const char* description) {
        std::cerr << "GLFW error " << code << ": " << description << '\n';
    });
    if (!glfwInit())
        return 1;
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
    glfwWindowHint(GLFW_VISIBLE, smokeTest ? GLFW_FALSE : GLFW_TRUE);
    GLFWwindow* window = glfwCreateWindow(1280, 800, "Orbit - Computer Graphics Week 7", nullptr, nullptr);
    if (!window) {
        std::cerr << "An OpenGL 3.3 core profile driver is required.\n";
        glfwTerminate();
        return 1;
    }
    glfwSetWindowSizeLimits(window, 960, 600, GLFW_DONT_CARE, GLFW_DONT_CARE);
    glfwMakeContextCurrent(window);
    glfwSwapInterval(smokeTest ? 0 : 1);
    int status = 0;
    try {
        status = run(window, executableDirectory(argv[0]), smokeTest, screenshot);
    } catch (const std::exception& error) {
        std::cerr << "Error: " << error.what() << '\n';
        status = 1;
    }
    glfwDestroyWindow(window);
    glfwTerminate();
    return status;
}
