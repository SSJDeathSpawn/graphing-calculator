#version 330

in vec4 Colour;
out vec4 Frag_Colour;

void main() {
    Frag_Colour = Colour;
}