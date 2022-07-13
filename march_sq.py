from __future__ import annotations
from typing import TYPE_CHECKING, Callable


from utils import sign, lerp, invlerp

if TYPE_CHECKING:
    pass

class MarchingSquareHelper(object):
    
    @staticmethod
    def get_needed_sides(values: dict[tuple[int, int], float]) -> list[int]:
        side_list = []
        clear_values = {i:sign(values[i]) for i in values}
        en = list(zip(range(len(clear_values)), list(clear_values.values())))
        for i, v in en: 
            #If there is a 1, then add that side to the list if the other end's value is -1
            if ((v in (1,-1)) and (en[(i+1)%4][1]==-v or en[(i+1)%4][1]==0)):
                #and 
                side_list.append(i)
        
        return side_list

    @staticmethod
    def get_pair_list(values: dict[tuple[int, int], float], sides: list[int]) -> dict[tuple[tuple[int, int], tuple[int, int]], tuple[float, float]]:
        easier = list(values.items())
        pair = {(easier[i][0], easier[(i+1)%4][0]):(easier[i][1], easier[(i+1)%4][1]) for i in sides}
        return pair

    @staticmethod
    def get_lines_from_cell(values: dict[tuple[int, int], float], func: Callable[[float, float], float]) -> list[list[float]]:
        """Returns the approximate ends of the line segments that form the contour."""

        line_points = []
        sides: list[int] = MarchingSquareHelper.get_needed_sides(values)
        pairs: dict[tuple[tuple[int, int], tuple[int, int]], tuple[float, float]] = MarchingSquareHelper.get_pair_list(values, sides)
        for side in pairs.items():
            #If x is constant, evaluate the y value using lerp
            if side[0][0][0] == side[0][1][0]:
                line_points.append([side[0][0][0], lerp(side[0][0][1], side[0][1][1], invlerp(side[1][0], side[1][1], 0))])
            #If y is constant, evaluate the x value using lerp
            else:
                line_points.append([lerp(side[0][0][0], side[0][1][0], invlerp(side[1][0], side[1][1], 0)), side[0][0][1]])
        if len(line_points) & 1 == 0:
            return line_points