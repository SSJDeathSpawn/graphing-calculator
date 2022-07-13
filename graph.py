from __future__ import annotations
import itertools
from typing import TYPE_CHECKING, Callable
import numpy as np

from constants import CLARITY, GRAPH_BOUNDS, WINDOW_RESOLUTION, GRAPH_LIMIT, CELL_VALUES
from march_sq import MarchingSquareHelper

if TYPE_CHECKING:
    import moderngl

class Graph(object):

    def __init__(self, ctx: moderngl.Context, prog: moderngl.Program, prog_attribs: list[str], func: Callable[[float, float], float]) -> Graph:
        x_line: list[list[float]] = [
            [-GRAPH_BOUNDS[0]/WINDOW_RESOLUTION[0], 0, 0.2, 0.2, 0.2],
            [GRAPH_BOUNDS[0]/WINDOW_RESOLUTION[0], 0, 0.2, 0.2, 0.2]
        ]
        y_line: list[list[float]] = [
            [0.0, -GRAPH_BOUNDS[1]/WINDOW_RESOLUTION[1], 0.2, 0.2, 0.2],
            [0.0, GRAPH_BOUNDS[1]/WINDOW_RESOLUTION[1], 0.2, 0.2, 0.2]
        ]

        guide_linesH: list[list[list[float]]] = [
            [[-GRAPH_BOUNDS[0]/WINDOW_RESOLUTION[0], i*GRAPH_BOUNDS[1]/(WINDOW_RESOLUTION[1]*GRAPH_LIMIT[1]), 0.5, 0.5, 0.5],
            [GRAPH_BOUNDS[0]/WINDOW_RESOLUTION[0], i*GRAPH_BOUNDS[1]/(WINDOW_RESOLUTION[1]*GRAPH_LIMIT[1]), 0.5, 0.5, 0.5]]
            for i in range(-GRAPH_LIMIT[1], GRAPH_LIMIT[1]+1) if i != 0
        ]
        guide_lines_hori: list[list[float]] = []
        for item in guide_linesH:
            guide_lines_hori.extend(item)
        
        guide_linesV: list[list[list[float]]] = [
            [[i*GRAPH_BOUNDS[0]/(WINDOW_RESOLUTION[0]*GRAPH_LIMIT[0]), -GRAPH_BOUNDS[1]/WINDOW_RESOLUTION[1], 0.5, 0.5, 0.5],
            [i*GRAPH_BOUNDS[0]/(WINDOW_RESOLUTION[0]*GRAPH_LIMIT[0]), GRAPH_BOUNDS[1]/WINDOW_RESOLUTION[1], 0.5, 0.5, 0.5]]
            for i in range(-GRAPH_LIMIT[0], GRAPH_LIMIT[0]+1) if i != 0
        ]
        guide_lines_vert: list[list[float]] = []
        for item in guide_linesV:
            guide_lines_vert.extend(item)

        lines: list[list[float]] = x_line + y_line + guide_lines_hori + guide_lines_vert
        xs: list[float] = [ i[0] for i in lines ] 
        ys: list[float] = [ i[1] for i in lines ]
        rs: list[float] = [ i[2] for i in lines ]
        gs: list[float] = [ i[3] for i in lines ]
        bs: list[float] = [ i[4] for i in lines ]
        self.axes_vbo: moderngl.Buffer = ctx.buffer(np.dstack([xs, ys, rs, gs, bs]).astype('f4').tobytes())
        self.axes_vao: moderngl.VertexArray = ctx.simple_vertex_array(prog, self.axes_vbo, *prog_attribs)

        self.calculate_points(func)
        self.calculate_line_points(func)
        xs,ys,rs,gs,bs = [],[],[],[],[]
        for point in self.line_points:
            on_screen = Graph.get_point_on_screen(point)
            xs.append(on_screen[0])
            ys.append(on_screen[1])
            rs.append(0.8) 
            gs.append(0.0) 
            bs.append(0.0)

        # xs,ys,rs,gs,bs = [],[],[],[],[]
        # for key, value in self.result.items():
        #     on_screen = Graph.get_point_on_screen(key)
        #     xs.append(on_screen[0])
        #     ys.append(on_screen[1])
        #     if value < 0:
        #         rs.append(0.0)
        #         gs.append(0.0) 
        #         bs.append(1.0)
        #     elif value == 0:
        #         rs.append(0.0) 
        #         gs.append(1.0) 
        #         bs.append(1.0)
        #     elif value > 0:
        #         rs.append(0.0) 
        #         gs.append(1.0) 
        #         bs.append(0.0)

        temp = np.dstack([xs, ys, rs, gs, bs])
        self.result_vbo = ctx.buffer(np.dstack([xs,ys,rs,gs,bs]).astype('f4').tobytes())
        self.result_vao = ctx.simple_vertex_array(prog, self.result_vbo, *prog_attribs)

    def calculate_line_points(self, func: Callable[[float, float], float]) -> None:
        self.line_points = []
        for i in range(-GRAPH_LIMIT[0]*CLARITY, GRAPH_LIMIT[0]*CLARITY):
            for j in range(GRAPH_LIMIT[1]*CLARITY, -GRAPH_LIMIT[1]*CLARITY,-1):
                #Points of interest
                psoi = [(i/CLARITY,j/CLARITY), ((i+1)/CLARITY, j/CLARITY), ((i+1)/CLARITY, (j-1)/CLARITY), (i/CLARITY, (j-1)/CLARITY)]
                point_value = {poi:self.result[poi] for poi in psoi}
                temp_lines = MarchingSquareHelper.get_lines_from_cell(point_value, func)
                if temp_lines: 
                    self.line_points.extend(temp_lines)
    
    def calculate_points(self, func: Callable[[float, float], float]):
        all_points = itertools.product([i/CLARITY for i in range(-GRAPH_LIMIT[0]*CLARITY, GRAPH_LIMIT[0]*CLARITY+1)], [i/CLARITY for i in range(-GRAPH_LIMIT[1]*CLARITY, GRAPH_LIMIT[1]*CLARITY+1)])
        self.result = {}
        for point in all_points:
            self.result[point] = func(*point)

    @staticmethod
    def get_point_on_screen(point: tuple[int | float, int | float]) -> tuple[float, float]:
        return (point[0] * GRAPH_BOUNDS[0]/(WINDOW_RESOLUTION[0]*GRAPH_LIMIT[0]), point[1] * GRAPH_BOUNDS[1]/(WINDOW_RESOLUTION[1]*GRAPH_LIMIT[1]))

    def render_axes(self, ctx: moderngl.Context):
        self.axes_vao.render(ctx.LINES)
        # ctx.point_size = 7.0
        self.result_vao.render(ctx.LINES)

    def render(self, ctx: moderngl.Context):
        self.render_axes(ctx)