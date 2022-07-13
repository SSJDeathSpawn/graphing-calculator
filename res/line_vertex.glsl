
#version 330

in vec2 vert;
in float thickness;
out float w;

void main() {
    gl_Position = vec4(vert, 0.0, 1.0);
    w = thickness;
}