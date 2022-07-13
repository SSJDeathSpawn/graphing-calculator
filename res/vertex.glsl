#version 330

in vec2 vert;
in vec3 colour;
out vec4 Colour;

void main() {
    gl_Position = vec4(vert, 0.0, 1.0);
    Colour = vec4(colour, 1.0);
}