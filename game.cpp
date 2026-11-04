#include "game.h"

#include <algorithm>
#include <cmath>

namespace {
constexpr float PI = 3.14159265359f;

void fire(Game& game, float angle, float speed, bool aimed) {
    glm::vec3 direction(std::cos(angle), 0.0f, std::sin(angle));
    game.bullets.push_back({game.enemy, direction * speed, aimed});
}
}

void Game::reset() {
    *this = Game{};
}

int Game::score() const {
    return static_cast<int>(elapsed * 100.0f) + grazes * GRAZE_BONUS;
}

void Game::update(float dt, const Input& input) {
    if (paused || finished() || dt <= 0.0f)
        return;

    // A fixed 120 Hz step keeps movement and collision independent of frame rate.
    elapsed = std::min(elapsed + dt, ROUND_SECONDS);
    invulnerable = std::max(0.0f, invulnerable - dt);
    grazeFlash = std::max(0.0f, grazeFlash - dt);
    dashCooldown = std::max(0.0f, dashCooldown - dt);
    wave = std::min(3, 1 + static_cast<int>(elapsed / 20.0f));

    glm::vec3 movement(input.x, 0.0f, input.z);
    if (glm::dot(movement, movement) > 1.0f)
        movement = glm::normalize(movement);
    if (input.dash && dashCooldown <= 0.0f && glm::dot(movement, movement) > 0.0f) {
        dashDirection = glm::normalize(movement);
        dashTime = DASH_DURATION;
        dashCooldown = DASH_COOLDOWN;
    }
    const bool dashing = dashTime > 0.0f;
    player += (dashing ? dashDirection * DASH_SPEED : movement * (input.slow ? 2.4f : 5.2f)) * dt;
    dashTime = std::max(0.0f, dashTime - dt);
    player.x = glm::clamp(player.x, -ARENA_X + PLAYER_RADIUS, ARENA_X - PLAYER_RADIUS);
    player.z = glm::clamp(player.z, -ARENA_Z + PLAYER_RADIUS, ARENA_Z - PLAYER_RADIUS);
    enemy.x = 2.8f * std::sin(elapsed * 0.55f);
    enemy.z = -4.5f + 0.5f * std::sin(elapsed * 0.8f);

    aimTimer -= dt;
    if (aimTimer <= 0.0f) {
        glm::vec3 toPlayer = player - enemy;
        float angle = std::atan2(toPlayer.z, toPlayer.x);
        // A three-shot fan aimed at the player's position when it was fired.
        for (int i = -1; i <= 1; ++i)
            fire(*this, angle + i * 0.20f, 4.0f + wave * 0.6f, true);
        aimTimer += 1.05f - wave * 0.12f;
    }

    ringTimer -= dt;
    if (ringTimer <= 0.0f) {
        int count = 14 + wave * 4;
        float rotation = elapsed * 0.33f;
        for (int i = 0; i < count; ++i)
            fire(*this, rotation + 2.0f * PI * i / count, 2.5f + wave * 0.35f, false);
        ringTimer += 2.1f - wave * 0.15f;
    }

    const float hitDistance = PLAYER_RADIUS + BULLET_RADIUS;
    for (auto it = bullets.begin(); it != bullets.end();) {
        it->position += it->velocity * dt;
        glm::vec3 difference = player - it->position;
        float distanceSquared = glm::dot(difference, difference);
        bool hit = distanceSquared <= hitDistance * hitDistance;
        bool outside = std::abs(it->position.x) > ARENA_X + 2.0f ||
                       std::abs(it->position.z) > ARENA_Z + 2.0f;
        if (hit) {
            if (invulnerable <= 0.0f && !dashing) {
                --health;
                invulnerable = 1.2f;
            }
            // Remove overlapping shots even during the brief damage grace period.
            it = bullets.erase(it);
        } else if (outside) {
            it = bullets.erase(it);
        } else {
            if (!it->grazed && !dashing && invulnerable <= 0.0f &&
                distanceSquared <= GRAZE_RADIUS * GRAZE_RADIUS) {
                it->grazed = true;
                ++grazes;
                grazeFlash = 0.7f;
            }
            ++it;
        }
    }
    if (elapsed >= ROUND_SECONDS && health > 0)
        won = true;
}
