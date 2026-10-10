#version 330 core
out vec4 fragColor;
uniform vec3 baseColor;
uniform bool textured;
void main() {
    fragColor = vec4(textured ? vec3(0.25) : baseColor, 1.0);
}
