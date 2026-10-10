#version 330 core
layout(location = 0) in vec2 aPosition;
layout(location = 1) in vec4 aColor;
uniform mat4 projection;
out vec4 color;
void main() {
    color = aColor;
    gl_Position = projection * vec4(aPosition, 0.0, 1.0);
}
