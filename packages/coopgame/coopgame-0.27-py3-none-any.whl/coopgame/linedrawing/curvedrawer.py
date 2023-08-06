import pygame
from coopgame.colors import Color
from typing import List, Dict, Callable
from coopstructs.curves import Arc, CubicBezier, LineCurve, Curve, Orientation, CatmullRom, CircularArc
from coopstructs.geometry import Line, PolygonRegion
import numpy as np
from descartes import PolygonPatch
from shapely.geometry import LineString
import coopgame.pygamehelpers as help


class CurveDrawer:

    def __init__(self):
        pass

    @classmethod
    def draw_curves(cls,
                    curves: Dict[Curve, Color],
                    surface: pygame.Surface,
                    control_point_color: Color = Color.RED,
                    control_point_size: int = None,
                    control_line_color: Color = Color.GREY,
                    draw_scale_matrix=None,
                    buffer: int = None,
                    buffer_color: Color = None):
        for curve, color in curves.items():
            if type(curve) == CubicBezier:
                cls.draw_bezier(surface,
                                 curve,
                                 color,
                                 control_point_color=control_point_color,
                                 control_point_size=control_point_size,
                                 control_line_color=control_line_color,
                                 draw_scale_matrix=draw_scale_matrix,
                                 buffer=buffer,
                                 buffer_color=buffer_color)
            elif type(curve) == LineCurve:
                cls.draw_line(surface,
                               curve,
                               color,
                               control_point_color=control_point_color,
                               control_point_size=control_point_size,
                               draw_scale_matrix=draw_scale_matrix,
                               buffer=buffer,
                               buffer_color=buffer_color)
            elif type(curve) == Arc:
                cls.draw_arc(surface,
                              curve,
                              color,
                              control_point_color=control_point_color,
                              control_point_size=control_point_size,
                              draw_scale_matrix=draw_scale_matrix,
                              buffer=buffer,
                              buffer_color=buffer_color)
            elif type(curve) == CatmullRom:
                cls.draw_catmullrom(surface,
                                     curve,
                                     color,
                                     control_point_color=control_point_color,
                                     control_point_size=control_point_size,
                                     draw_scale_matrix=draw_scale_matrix,
                                     buffer=buffer,
                                     buffer_color=buffer_color)
            elif type(curve) == CircularArc:
                cls.draw_circulararc(surface,
                                      curve,
                                      color,
                                      control_point_color=control_point_color,
                                      control_point_size=control_point_size,
                                      draw_scale_matrix=draw_scale_matrix,
                                      buffer=buffer,
                                      buffer_color=buffer_color)
            else:
                raise NotImplementedError(f"Unahanlded curve type {curve}")

    @classmethod
    def draw_bezier(cls,
                    screen,
                    curve: CubicBezier,
                    curve_color: Color,
                    control_point_color: Color = Color.RED,
                    control_point_size: int = None,
                    control_line_color: Color = Color.GREY,
                    draw_scale_matrix=None,
                    buffer: int = None,
                    buffer_color: Color = None):

        if draw_scale_matrix is None:
            draw_scale_matrix = np.identity(4)

        # Convert control points into np.arrays
        arrays_of_points = []
        for point in curve.control_points:
            arrays_of_points.append(np.array([point.x, point.y, 0, 1]))

        # Translate the points via the scaling matrix
        translated_points = draw_scale_matrix.dot(np.transpose(np.array(arrays_of_points))).transpose()

        # Draw bezier curve
        b_points = curve.compute_bezier_points([(translated_points[ii][0], translated_points[ii][1])
                                                for ii in range(len(translated_points))])

        if buffer is not None:
            line = LineString(b_points)

            dilated = line.buffer(buffer)
            poly = PolygonRegion.from_shapely_polygon(dilated)
            buffer_color = Color.GREEN if buffer_color is None else buffer_color
            help.draw_polygon(screen, [x.as_tuple() for x in poly.boundary_points], buffer_color)

        # Draw control points
        if control_point_size is None:
            control_point_size = 4

        if control_point_color:
            for ii in range(len(translated_points)):
                pygame.draw.circle(screen, control_point_color.value,
                                   (int(translated_points[ii][0]), int(translated_points[ii][1])), control_point_size)
            # for p in curve.control_points:
            #     pygame.draw.circle(screen, control_point_color.value, (int(p.x), int(p.y)), 4)

        # Draw control "lines"
        if control_line_color:
            pygame.draw.lines(screen,
                              control_line_color.value,
                              False,
                              [(translated_points[ii][0], translated_points[ii][1])
                               for ii in range(len(translated_points))])
            # pygame.draw.lines(screen, control_line_color.value, False, [(x.x, x.y) for x in curve.control_points])

        # b_points = curve.compute_bezier_points([(x.x, x.y) for x in curve.control_points])
        if b_points is not None and len(b_points) > 1:
            pygame.draw.lines(screen, curve_color.value, False, b_points, 2)

    @classmethod
    def draw_line(cls,
                  surface: pygame.Surface,
                  line: Line,
                  color: Color,
                  control_point_color: Color = Color.RED,
                  control_point_size: int = None,
                  draw_scale_matrix=None,
                  buffer: int = None,
                  buffer_color: Color = None):
        if draw_scale_matrix is None:
            draw_scale_matrix = np.identity(4)

        # Convert Origin/Destination into np.arrays
        origin = np.array([line.origin.x, line.origin.y, 0, 1])
        destination = np.array([line.destination.x, line.destination.y, 0, 1])

        # Translate the points via the scaling matrix
        translated_points = draw_scale_matrix.dot(np.transpose(np.array([origin, destination]))).transpose()

        # Draw the lines
        pygame.draw.line(surface, color.value, (translated_points[0][0], translated_points[0][1]),
                         (translated_points[1][0], translated_points[1][1]))

        # Draw the points
        if control_point_size is None:
            control_point_size = 4

        if control_point_color:
            pygame.draw.circle(surface, control_point_color.value,
                               (int(translated_points[0][0]), int(translated_points[0][1])), control_point_size)
            pygame.draw.circle(surface, control_point_color.value,
                               (int(translated_points[1][0]), int(translated_points[1][1])), control_point_size)

    @classmethod
    def draw_arc(cls,
                 surface: pygame.Surface,
                 arc: Arc,
                 color: Color,
                 control_point_color: Color = Color.RED,
                 control_point_size: int = None,
                 draw_scale_matrix=None,
                 buffer: int = None,
                 buffer_color: Color = None):

        if draw_scale_matrix is None:
            draw_scale_matrix = np.identity(4)

        # Convert control points into np.arrays
        control_points = arc.compute_curve_points()
        arrays_of_points = []
        for point in control_points:
            arrays_of_points.append(np.array([point.x, point.y, 0, 1]))

        # Translate the points via the scaling matrix
        translated_points = draw_scale_matrix.dot(np.transpose(np.array(arrays_of_points))).transpose()

        # Draw Lines
        pygame.draw.lines(surface, color.value, False, [(translated_points[ii][0], translated_points[ii][1])
                                                        for ii in range(len(translated_points))], 2)

        # Draw the points
        if control_point_size is None:
            control_point_size = 4

        if control_point_color:
            pygame.draw.circle(surface, control_point_color.value,
                               (int(translated_points[0][0]), int(translated_points[0][1])), control_point_size)
            pygame.draw.circle(surface, control_point_color.value,
                               (int(translated_points[-1][0]), int(translated_points[-1][1])), control_point_size)

    @classmethod
    def draw_catmullrom(cls,
                        screen,
                        curve: CatmullRom,
                        curve_color: Color,
                        control_point_color: Color = Color.RED,
                        control_point_size: int = None,
                        control_line_color: Color = Color.GREY,
                        draw_scale_matrix=None,
                        buffer: int = None,
                        buffer_color: Color = None):

        if draw_scale_matrix is None:
            draw_scale_matrix = np.identity(4)

        # Convert control points into np.arrays
        arrays_of_points = []
        for point in curve.control_points:
            arrays_of_points.append(np.array([point.x, point.y, 0, 1]))

        # Translate the points via the scaling matrix
        translated_points = draw_scale_matrix.dot(np.transpose(np.array(arrays_of_points))).transpose()

        # Draw control points
        if control_point_size is None:
            control_point_size = 4

        if control_point_color:
            for ii in range(len(translated_points)):
                pygame.draw.circle(screen, control_point_color.value,
                                   (int(translated_points[ii][0]), int(translated_points[ii][1])), control_point_size)

        # Draw control "lines"
        if control_line_color:
            pygame.draw.lines(screen,
                              control_line_color.value,
                              False,
                              [(translated_points[ii][0], translated_points[ii][1])
                               for ii in range(len(translated_points))])

        # Draw CatmullRom curve
        b_points = curve.compute_catmull_points([(translated_points[ii][0], translated_points[ii][1])
                                                 for ii in range(len(translated_points))])
        # b_points = curve.compute_catmull_points(curve.control_points)

        if b_points is not None and len(b_points) > 1:
            pygame.draw.lines(screen, curve_color.value, False, [(point.x, point.y) for point in b_points], 2)

    @classmethod
    def draw_circulararc(cls,
                         screen,
                         curve: CircularArc,
                         curve_color: Color,
                         control_point_color: Color = Color.RED,
                         control_point_size: int = None,
                         control_line_color: Color = Color.GREY,
                         draw_scale_matrix=None,
                         buffer: int = None,
                         buffer_color: Color = None):
        if draw_scale_matrix is None:
            draw_scale_matrix = np.identity(4)

        # Convert control points into np.arrays
        arrays_of_points = []
        for point in curve.control_points:
            arrays_of_points.append(np.array([point.x, point.y, 0, 1]))

        # Translate the points via the scaling matrix
        translated_points = draw_scale_matrix.dot(np.transpose(np.array(arrays_of_points))).transpose()

        # Draw control points
        if control_point_size is None:
            control_point_size = 4

        if control_point_color:
            for ii in range(len(translated_points)):
                pygame.draw.circle(screen, control_point_color.value,
                                   (int(translated_points[ii][0]), int(translated_points[ii][1])), control_point_size)

        # Draw control "lines"
        if control_line_color:
            pygame.draw.lines(screen,
                              control_line_color.value,
                              False,
                              [(translated_points[ii][0], translated_points[ii][1])
                               for ii in range(len(translated_points))])

        # Draw circulararc_points
        b_points = curve.compute_circulararc_points()

        # Convert
        arrays_of_points = []
        for point in b_points:
            arrays_of_points.append(np.array([point.x, point.y, 0, 1]))

        # Translate the points via the scaling matrix
        translated_points = draw_scale_matrix.dot(np.transpose(np.array(arrays_of_points))).transpose()

        if translated_points is not None and len(translated_points) > 1:
            pygame.draw.lines(screen, curve_color.value, False, [(point[0], point[1]) for point in translated_points],
                              2)

    @classmethod
    def draw_curve_builder(self):
        pass