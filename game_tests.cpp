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

        Game dash;
        dash.aimTimer = dash.ringTimer = 1000;
        dash.invulnerable = 0;
        glm::vec3 dashStart = dash.player;
        dash.bullets.push_back({dash.player + glm::vec3(DASH_SPEED * FIXED_STEP, 0, 0),
                                {0,0,0}, true});
        dash.update(FIXED_STEP, {1,0,false,true});
        check(dash.player.x > dashStart.x + 0.1f && dash.health == MAX_HEALTH &&
              dash.bullets.empty(), "Dash must move quickly through a shot without damage.");
        check(dash.dashCooldown > 0 && dash.dashTime > 0, "Dash must start its timers.");
        advance(dash, 0.25f, {1,0,false});
        float afterDash = dash.player.x;
        dash.update(FIXED_STEP, {1,0,false,true});
        check(dash.player.x - afterDash < 0.1f, "Dash cannot repeat during cooldown.");
        advance(dash, DASH_COOLDOWN, {});
        check(dash.dashCooldown == 0, "Dash cooldown must expire.");
        dash.update(FIXED_STEP, {0,0,false,true});
        check(dash.dashTime == 0, "Dash needs a movement direction.");
        dash.update(FIXED_STEP, {-1,0,false,true});
        check(dash.dashTime > 0 && dash.dashDirection.x < 0,
              "Dash should be available again in the requested direction.");
        dash.paused = true;
        float pausedCooldown = dash.dashCooldown;
        advance(dash, 0.5f, {1,0,false,true});
        check(dash.dashCooldown == pausedCooldown, "Pause must freeze dash cooldown.");
        dash.reset();
        check(dash.dashCooldown == 0 && dash.dashTime == 0,
              "Restart must restore dash availability.");

        Game edgeDash;
        edgeDash.aimTimer = edgeDash.ringTimer = 1000;
        edgeDash.player.x = ARENA_X - PLAYER_RADIUS - 0.05f;
        advance(edgeDash, DASH_DURATION, {1,0,false,true});
        check(edgeDash.player.x == ARENA_X - PLAYER_RADIUS,
              "Dash must respect arena boundaries.");

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

        Game graze;
        graze.aimTimer = graze.ringTimer = 1000;
        graze.invulnerable = 0;
        graze.bullets.push_back({graze.player + glm::vec3(GRAZE_RADIUS - 0.05f,0,0),
                                 {0,0,0},true});
        graze.update(FIXED_STEP, {});
        check(graze.grazes == 1 && graze.health == MAX_HEALTH &&
              graze.score() == static_cast<int>(graze.elapsed * 100.0f) + GRAZE_BONUS,
              "A near miss must award bonus points without damage.");
        check(graze.grazeFlash > 0, "A near miss must show feedback.");
        advance(graze, 0.2f);
        check(graze.grazes == 1, "The same bullet can only be grazed once.");
        graze.reset();
        check(graze.grazes == 0 && graze.grazeFlash == 0,
              "Restart must clear near miss points and feedback.");

        Game safeGraze;
        safeGraze.aimTimer = safeGraze.ringTimer = 1000;
        safeGraze.bullets.push_back({safeGraze.player + glm::vec3(GRAZE_RADIUS - 0.05f,0,0),
                                     {0,0,0},true});
        safeGraze.update(FIXED_STEP, {});
        check(safeGraze.grazes == 0,
              "The opening damage grace period must not grant risk-free graze points.");

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
