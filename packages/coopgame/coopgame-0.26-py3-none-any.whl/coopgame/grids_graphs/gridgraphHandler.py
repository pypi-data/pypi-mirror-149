from coopgraph.gridSelectPolicies import TogglePolicy
from coopgraph.grids import RectGrid
from coopgame.grids_graphs.pygridhandler import PyGridHandler
from coopgame.grids_graphs.pygraphhandler import PyGraphHandler
from coopstructs.toggles import BooleanToggleable
import numpy as np
from coopgame.colors import Color
from coopstructs.vectors import Vector2
from coopstructs.geometry import Rectangle
from typing import Callable, Any
import logging

class GridGraphHandler:

    def __init__(self):
        self.toggle_key = 'toggle'
        self.toggle_bool_policy = TogglePolicy(key=self.toggle_key, toggle=BooleanToggleable(default=False))
        self.grid = None
        self.init_grid(200, 200)
        self.grid_handler = PyGridHandler()
        self.graph_handler = PyGraphHandler()
        self.graph = None

    def init_grid(self, rows, cols, init_condition: np.ndarray = None):
        self.grid = RectGrid(rows, cols, grid_select_policies=[self.toggle_bool_policy])

        if init_condition is not None:
            for ii, row in enumerate(init_condition):
                for jj, col in enumerate(row):
                    self.grid.at(ii, jj).state[self.toggle_key].set_value(True if init_condition[ii][jj] == 1 else False)

    def define_highlighted_grids(self, hover:Vector2, highlight_toggled:bool = False):
        highlights = {}
        grid_point = hover

        if self.grid.nColumns > grid_point.x >= 0 and self.grid.nRows > grid_point.y >= 0:
            highlights[grid_point] = Color.PURPLE

        if highlight_toggled:
            grid_value_array = self.grid.state_value_as_array(key=self.toggle_key)
            for x in range(0, self.grid.nColumns):
                for y in range(0,  self.grid.nRows):
                    if grid_value_array[y][x].value:
                        highlights[Vector2(x, y)] = Color.ORANGE

        return highlights

    def mouse_grid_pos(self, window_rect: Rectangle, mouse_pos: Vector2, draw_scale_matrix: np.array = None):
        return self.grid_handler.get_mouse_grid_pos(window_rect, mouse_pos,
                                             coord_to_grid_converter=self.grid.grid_from_coord,
                                             draw_scale_matrix=draw_scale_matrix)

    def redefine_grid(self, rows: int, cols: int, grid_update_callback: Callable[[Any], Any] = None):
        if rows is None or cols is None:
            return

        logging.info(f"Creating grid...")
        self.init_grid(rows, cols)
        logging.info(f"Done creating grid...")

        if grid_update_callback is not None:
            grid_update_callback(...)



