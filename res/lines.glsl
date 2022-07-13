#version 330

layout (lines) in;

in float w[];

layout (triangle_strip, max_vertices=4) out;

void main() {
    float offset;
    if (gl_in[0].gl_Position.y == gl_in[1].gl_Position.y || gl_in[0].gl_Position.x == gl_in[1].gl_Position.x) {
        offset = w[0]/2 ;
    } else {
        float m = (gl_in[1].gl_Position.y - gl_in[0].gl_Position.y)/(gl_in[1].gl_Position.x - gl_in[0].gl_Position.x);
         offset = sqrt((w[0]*w[0]*m*m)/(4+4*m*m));
    }

    gl_Position = vec4(gl_in[0].gl_Position.x - int(gl_in[0].gl_Position.x != gl_in[1].gl_Position.x) * offset, gl_in[0].gl_Position.y + ((gl_in[0].gl_Position.y != gl_in[1].gl_Position.y) ? offset : 0.0), 0.0, 1.0);
    EmitVertex();
    gl_Position = vec4(gl_in[1].gl_Position.x - int(gl_in[0].gl_Position.x != gl_in[1].gl_Position.x) * offset, gl_in[1].gl_Position.y + int(gl_in[0].gl_Position.y != gl_in[1].gl_Position.y) * offset, 0.0, 1.0);
    EmitVertex();
    gl_Position = vec4(gl_in[1].gl_Position.x + int(gl_in[0].gl_Position.x != gl_in[1].gl_Position.x) * offset, gl_in[1].gl_Position.y - int(gl_in[0].gl_Position.y != gl_in[1].gl_Position.y) * offset, 0.0, 1.0);
    EmitVertex();
    gl_Position = vec4(gl_in[0].gl_Position.x + int(gl_in[0].gl_Position.x != gl_in[1].gl_Position.x) * offset, gl_in[0].gl_Position.y - int(gl_in[0].gl_Position.y != gl_in[1].gl_Position.y) * offset, 0.0, 1.0);
    EmitVertex();
    EndPrimitive();
}