from math import sin
import moderngl_window as mglw
import numpy as np
from pathlib import Path

from graph import Graph
from constants import GL_VERSION, WINDOW_RESOLUTION

class CustomWindow(mglw.WindowConfig):
    gl_version = GL_VERSION
    window_size = WINDOW_RESOLUTION
    resource_dir = (Path(__file__).parent / 'res').resolve()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Do initialization here

        self.vert = self.load_program(vertex_shader='vertex.glsl', fragment_shader='fragment.glsl')

        func = lambda x, y: (x**2 + y**2)**2 - 32*(x**2 - y**2)
        circle_func = lambda x, y: x**2 + y**2 - 4
        sin_func = lambda x,y: y - sin(x)
        
        self.graph = Graph(self.ctx, self.vert, ['vert', 'colour'], func)

    def render(self, time, frametime):
        self.ctx.clear(1.0, 1.0, 1.0, 1.0)
        self.graph.render(self.ctx)
