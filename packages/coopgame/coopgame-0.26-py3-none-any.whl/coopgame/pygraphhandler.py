from coopgame.colors import Color
import pygame
from coopgraph.graphs import Graph
from coopstructs.vectors import Vector2
from coopstructs.geometry import Rectangle
import coopgame.pygamehelpers as help
from typing import Callable, Tuple


class PyGraphHandler:
    def _draw_graph_edges(self,
                          surface: pygame.Surface,
                          graph: Graph,
                          coordinate_converter: Callable[[Vector2], Vector2] = None,
                          enabled_color: Color = None,
                          disabled_color: Color = None,
                          draw_scale_matrix=None,
                          draw_label_color: Color = None,
                          draw_label_font: pygame.font.Font = None,
                          label_offset: Tuple[int, int] = None
                          ):

        if not coordinate_converter:
            coordinate_converter = lambda x: x

        if not enabled_color:
            enabled_color = Color.BLUE

        if not disabled_color:
            disabled_color = Color.GREY

        if draw_label_color:
            draw_label_font = draw_label_font if draw_label_font is not None else pygame.font.Font(None, 25)
            label_offset = label_offset if label_offset is not None else (10, 10)

        for edge in graph.edges:
            start = coordinate_converter(edge.start.pos)
            end = coordinate_converter(edge.end.pos)

            width = 3 if graph.edge_between(edge.end, edge.start) is not None else 1

            scaled_pos = help.scaled_points_of_points([start, end], draw_scale_matrix=draw_scale_matrix)
            color = enabled_color if edge.enabled() else disabled_color
            pygame.draw.line(surface, color.value, (scaled_pos[0][0], scaled_pos[0][1]),
                             (scaled_pos[1][0], scaled_pos[1][1]), width)

            if draw_label_color is not None:
                mid = ((scaled_pos[0][0] + scaled_pos[1][0]) / 2, (scaled_pos[0][1] + scaled_pos[1][1]) / 2)
                help.draw_text(edge.id, surface, draw_label_font,
                               offset_rect=Rectangle(mid[0] + label_offset[0], mid[1] + label_offset[1], 100, 100),
                               color=draw_label_color)

    def _draw_graph_nodes(self,
                          surface: pygame.Surface,
                          graph: Graph,
                          coordinate_converter: Callable[[Vector2], Vector2] = None,
                          color: Color = None,
                          radius: int = 1,
                          width: int = 0,
                          draw_scale_matrix=None,
                          draw_label_color: Color = None,
                          draw_label_font: pygame.font.Font = None,
                          label_offset: Tuple[int, int] = None):
        if not coordinate_converter:
            coordinate_converter = lambda x: x

        if not color:
            color = Color.ORANGE

        txt_dict = {}
        for node in graph.nodes:
            position = coordinate_converter(node.pos)
            scaled_pos = help.scaled_points([position], draw_scale_matrix=draw_scale_matrix)
            position = (int(scaled_pos[0].x), int(scaled_pos[0].y))

            pygame.draw.circle(surface, color.value, position, radius, width)

            txt_dict.setdefault(scaled_pos[0], []).append(node.name)

        if draw_label_color is not None:
            draw_label_font = draw_label_font if draw_label_font is not None else pygame.font.Font(None, 25)
            label_offset = label_offset if label_offset is not None else (10, 10)

            for pos, labels in txt_dict.items():
                help.draw_text(",".join(labels), surface, draw_label_font,
                               offset_rect=Rectangle(pos.x + label_offset[0], pos.y + label_offset[1], 100, 100),
                               color=draw_label_color)

    @staticmethod
    def draw_articulation_points(surface: pygame.Surface,
                                 graph: Graph,
                                 color: Color = None,
                                 draw_scale_matrix=None
                                 ):
        if graph is None:
            return

        articulation_points = graph.AP()

        if color is None:
            color = Color.ORANGE

        scaled_pos = help.scaled_points([node.pos for node in articulation_points.keys()],
                                        draw_scale_matrix=draw_scale_matrix)

        for point in scaled_pos:
            pygame.draw.circle(surface, color.value, (int(point.x), int(point.y)), 10, 1)

    def draw_to_surface(self, surface: pygame.Surface,
                        graph: Graph,
                        coordinate_converter: Callable[[Vector2], Vector2] = None,
                        node_color: Color = None,
                        enabled_edge_color: Color = None,
                        disabled_edge_color: Color = None,
                        draw_scale_matrix=None,
                        node_label_color: Color = None,
                        edge_label_color: Color = None,
                        draw_label_font: pygame.font.Font = None,
                        draw_articulation_points: bool = True):
        if not coordinate_converter:
            coordinate_converter = lambda x: x

        self._draw_graph_edges(surface,
                               graph=graph,
                               coordinate_converter=coordinate_converter,
                               enabled_color=enabled_edge_color,
                               disabled_color=disabled_edge_color,
                               draw_scale_matrix=draw_scale_matrix,
                               draw_label_color=edge_label_color,
                               draw_label_font=draw_label_font)
        self._draw_graph_nodes(surface,
                               graph=graph,
                               coordinate_converter=coordinate_converter,
                               color=node_color,
                               draw_scale_matrix=draw_scale_matrix,
                               draw_label_color=node_label_color,
                               draw_label_font=draw_label_font)

        if draw_articulation_points:
            self.draw_articulation_points(surface,
                                          graph,
                                          Color.ORANGE,
                                          draw_scale_matrix=draw_scale_matrix)