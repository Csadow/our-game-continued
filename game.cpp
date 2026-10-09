#include "game.h"
#include <algorithm>

void Game::reset() { *this = Game{}; }
int Game::score() const { return static_cast<int>(elapsed * 100); }

void Game::update(float dt, const Input& input) {
    if (paused || finished() || dt <= 0) return;
    elapsed += dt;
    glm::vec3 movement(input.x, 0, input.z);
    if (glm::dot(movement, movement) > 1)
        movement = glm::normalize(movement);
    player += movement * (input.slow ? 2.4f : 5.2f) * dt;
    player.x = glm::clamp(player.x, -ARENA_X + PLAYER_RADIUS, ARENA_X - PLAYER_RADIUS);
    player.z = glm::clamp(player.z, -ARENA_Z + PLAYER_RADIUS, ARENA_Z - PLAYER_RADIUS);
}
