#pragma once

#include <glm/glm.hpp>
#include <vector>

constexpr float ARENA_X = 9.0f;
constexpr float ARENA_Z = 7.0f;
constexpr float PLAYER_RADIUS = 0.30f;
constexpr float BULLET_RADIUS = 0.16f;
constexpr float ROUND_SECONDS = 60.0f;
constexpr float FIXED_STEP = 1.0f / 120.0f;
constexpr float DASH_SPEED = 15.0f;
constexpr float DASH_DURATION = 0.18f;
constexpr float DASH_COOLDOWN = 2.5f;
constexpr int MAX_HEALTH = 5;

struct Input {
    float x = 0.0f;
    float z = 0.0f;
    bool slow = false;
    bool dash = false;
};

struct Bullet {
    glm::vec3 position;
    glm::vec3 velocity;
    bool aimed = false;
};

// Gameplay uses X/Z for the floor; Y is the height above it.
struct Game {
    glm::vec3 player{0.0f, 0.45f, 4.5f};
    glm::vec3 enemy{0.0f, 0.45f, -4.5f};
    std::vector<Bullet> bullets;
    int health = MAX_HEALTH;
    int wave = 1;
    float elapsed = 0.0f;
    float invulnerable = 1.0f;
    float aimTimer = 1.4f;
    float ringTimer = 2.5f;
    float dashCooldown = 0.0f;
    float dashTime = 0.0f;
    glm::vec3 dashDirection{0.0f};
    bool paused = false;
    bool won = false;

    void reset();
    void update(float dt, const Input& input);
    int score() const;
    bool finished() const { return health <= 0 || won; }
};
