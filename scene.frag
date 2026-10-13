#version 330 core

in vec3 worldPosition;
in vec3 normal;
in vec2 uv;
out vec4 fragColor;

uniform vec3 baseColor;
uniform vec3 cameraPosition;
uniform vec3 lightPosition;
uniform float emission;
uniform bool textured;
uniform sampler2D floorTexture;

void main() {
    vec3 surface = baseColor;
    if (textured)
        surface *= texture(floorTexture, uv * vec2(9.0, 7.0)).rgb;

    vec3 N = normalize(normal);
    vec3 L = normalize(lightPosition - worldPosition);
    vec3 V = normalize(cameraPosition - worldPosition);
    vec3 H = normalize(L + V);
    float diffuse = max(dot(N, L), 0.0);
    float specular = diffuse > 0.0 ? pow(max(dot(N, H), 0.0), 48.0) : 0.0;
    vec3 color = surface * (0.23 + 0.77 * diffuse) + vec3(0.55) * specular;
    color += surface * emission;

    if (textured) {
        // Anti-aliased grid lines, computed from world coordinates.
        vec2 grid = abs(fract(worldPosition.xz - 0.5) - 0.5);
        vec2 line = 1.0 - smoothstep(vec2(0.0), fwidth(worldPosition.xz) * 1.2, grid);
        color += vec3(0.05, 0.22, 0.25) * max(line.x, line.y);
    }

    // A small distance fade makes the far side of the arena easier to read.
    float fog = smoothstep(22.0, 45.0, length(cameraPosition - worldPosition));
    color = mix(color, vec3(0.025, 0.035, 0.055), fog * 0.5);
    fragColor = vec4(color, 1.0);
}
