#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include <algorithm>
#include <iostream>
#include <string>
#include "game.h"

int main(int argc, char** argv) {
    bool test = argc > 1 && std::string(argv[1]) == "--smoke-test";
    if (!glfwInit()) return 1;
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
    glfwWindowHint(GLFW_VISIBLE, test ? GLFW_FALSE : GLFW_TRUE);
    GLFWwindow* window = glfwCreateWindow(1280, 800, "Orbit prototype", nullptr, nullptr);
    if (!window) { glfwTerminate(); return 1; }
    glfwMakeContextCurrent(window);
    glewExperimental = GL_TRUE;
    if (glewInit() != GLEW_OK) { glfwDestroyWindow(window); glfwTerminate(); return 1; }
    while (glGetError() != GL_NO_ERROR) {}
    glfwSwapInterval(test ? 0 : 1);
    double previous = glfwGetTime();
    int frames = 0;
    Game game;
    double accumulator = 0;
    while (!glfwWindowShouldClose(window)) {
        glfwPollEvents();
        if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS)
            glfwSetWindowShouldClose(window, GLFW_TRUE);
        double now = glfwGetTime();
        float dt = static_cast<float>(std::min(now - previous, 0.1));
        previous = now;
        Input input;
        auto down = [&](int key) { return glfwGetKey(window, key) == GLFW_PRESS; };
        input.x = float(down(GLFW_KEY_D)) - float(down(GLFW_KEY_A));
        input.z = float(down(GLFW_KEY_S)) - float(down(GLFW_KEY_W));
        input.slow = down(GLFW_KEY_LEFT_SHIFT) || down(GLFW_KEY_RIGHT_SHIFT);
        accumulator += test ? 1.0 / 60.0 : dt;
        while (accumulator >= FIXED_STEP) {
            game.update(FIXED_STEP, input);
            accumulator -= FIXED_STEP;
        }
        (void)dt;
        int width, height;
        glfwGetFramebufferSize(window, &width, &height);
        glViewport(0, 0, width, height);
        glClearColor(.025f, .035f, .055f, 1);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        glfwSwapBuffers(window);
        if (test && ++frames >= 10) break;
    }
    glfwDestroyWindow(window);
    glfwTerminate();
    std::cout << "Window prototype finished.\n";
    return 0;
}
