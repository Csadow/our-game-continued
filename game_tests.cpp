#include "game.h"

#include <cmath>
#include <iostream>
#include <stdexcept>

void check(bool condition, const char* message) {
    if (!condition)
        throw std::runtime_error(message);
}

void advance(Game& game, float seconds, Input input = {}) {
    int steps = static_cast<int>(std::round(seconds / FIXED_STEP));
    for (int i = 0; i < steps; ++i)
        game.update(FIXED_STEP, input);
}

int main() {
    try {
        Game straight, diagonal, slow;
        glm::vec3 start = straight.player;
        advance(straight, 0.5f, {1,0,false});
        advance(diagonal, 0.5f, {1,1,false});
        advance(slow, 0.5f, {1,0,true});
        check(std::abs(glm::length(straight.player - start) -
                       glm::length(diagonal.player - start)) < 0.001f,
              "Diagonal movement must not be faster.");
        check(slow.player.x < straight.player.x, "Shift must reduce speed.");

        Game bounded;
        bounded.aimTimer = bounded.ringTimer = 1000;
        advance(bounded, 5, {1,1,false});
        check(bounded.player.x <= ARENA_X - PLAYER_RADIUS &&
              bounded.player.z <= ARENA_Z - PLAYER_RADIUS, "Positive arena bounds failed.");
        advance(bounded, 10, {-1,-1,false});
        check(bounded.player.x >= -ARENA_X + PLAYER_RADIUS &&
              bounded.player.z >= -ARENA_Z + PLAYER_RADIUS, "Negative arena bounds failed.");

        Game hit;
        hit.invulnerable = 0;
        hit.bullets.push_back({hit.player, {0,0,0}, true});
        hit.bullets.push_back({hit.player, {0,0,0}, true});
        hit.update(FIXED_STEP, {});
        check(hit.health == MAX_HEALTH - 1 && hit.bullets.empty(),
              "Overlapping bullets must cause one hit during the grace period.");
        hit.bullets.push_back({hit.player, {0,0,0}, false});
        hit.update(FIXED_STEP, {});
        check(hit.health == MAX_HEALTH - 1, "Damage grace period failed.");

        Game miss;
        miss.invulnerable = 0;
        miss.bullets.push_back({miss.player + glm::vec3(0.6f,0,0), {0,0,0}, true});
        miss.update(FIXED_STEP, {});
        check(miss.health == MAX_HEALTH && miss.bullets.size() == 1, "A nearby miss must not damage.");
        miss.bullets.push_back({{ARENA_X + 3,0.45f,0},{1,0,0},false});
        miss.update(FIXED_STEP, {});
        check(miss.bullets.size() == 1, "Off-arena bullets must be removed.");

        Game paused;
        paused.paused = true;
        advance(paused, 1, {1,0,false});
        check(paused.elapsed == 0 && paused.player == start && paused.bullets.empty(),
              "Pause must freeze gameplay.");

        Game patterns;
        patterns.invulnerable = 1000;
        advance(patterns, 3);
        bool aimed = false, ring = false;
        for (const auto& bullet : patterns.bullets) {
            aimed = aimed || bullet.aimed;
            ring = ring || !bullet.aimed;
            check(std::isfinite(bullet.velocity.x) && std::isfinite(bullet.velocity.z),
                  "Bullet velocity must be finite.");
        }
        check(aimed && ring, "Both bullet patterns must spawn.");

        Game lost;
        lost.health = 1;
        lost.invulnerable = 0;
        lost.bullets.push_back({lost.player,{0,0,0},false});
        lost.update(FIXED_STEP, {});
        check(lost.finished() && !lost.won && lost.health == 0, "Game-over transition failed.");
        float stopped = lost.elapsed;
        advance(lost, 1, {1,0,false});
        check(lost.elapsed == stopped, "Game over must freeze gameplay.");

        Game winner;
        winner.invulnerable = 1000;
        advance(winner, 61);
        check(winner.won && winner.wave == 3 && winner.score() == 6000,
              "Full survival round must reach all waves and stop at 6000 points.");
        check(winner.bullets.size() < 250, "Bullet lifetime should bound the active count.");
        winner.reset();
        check(winner.health == MAX_HEALTH && winner.elapsed == 0 && winner.bullets.empty() &&
              !winner.won && !winner.paused && winner.player == start, "Restart must reset the round.");

        std::cout << "All gameplay checks passed.\n";
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "FAILED: " << error.what() << '\n';
        return 1;
    }
}
