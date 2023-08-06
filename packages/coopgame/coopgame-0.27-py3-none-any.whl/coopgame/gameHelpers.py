from typing import List
from coopstructs.vectors import Vector2, IVector
from coopstructs.geometry import Rectangle
import numpy as np

def calculate_fps(frame_times: List, ticks_last_frame: int):
    if len(frame_times) > 20:
        frame_times.pop(0)

    frame_times.append(ticks_last_frame)

    avg_sec_per_frame = sum(frame_times) / len(frame_times) / 1000.0
    fps = 1 / avg_sec_per_frame if avg_sec_per_frame > 0 else 0
    return fps

def game_area_coords_from_parent_coords(parent_coords: Vector2, game_area_surface_rectangle: Rectangle) -> Vector2:
    """Converts Global Coords into coords on the game area"""
    return Vector2(parent_coords.x - game_area_surface_rectangle.x, parent_coords.y - game_area_surface_rectangle.y)

def scaled_points_of_a_rect(rect, grid_pos: Vector2, draw_scale_matrix=None, margin: int = 1):
    if draw_scale_matrix is None:
        draw_scale_matrix = np.identity(4)

    ''' get the rectangle object representing the grid position that was input'''
    rect = Rectangle(x=(margin + rect.width) * grid_pos.x + margin
                     , y=(margin + rect.height) * grid_pos.y + margin
                     , height=rect.height
                     , width=rect.width)

    '''Convert the rectangle to a list of points at the 4 corners'''
    points = [(x[0], x[1], 0, 1) for x in rect.points_tuple()]

    '''Multiply the points by the transform matrix for drawing'''
    transformed_points = draw_scale_matrix.dot(np.transpose(points))  # Transpose the points to appropriately mutiply

    '''return the x and y position for all points on the rectangle'''
    return np.transpose(transformed_points)[:,
           :3]  # Re-Transpose the points back to remain in a "list of points" format


def scaled_points_of_points(points: List[Vector2], draw_scale_matrix=None):
    if draw_scale_matrix is None:
        draw_scale_matrix = np.identity(4)

    if len(points) == 0:
        return np.array([])
    '''Convert the point to a 4-dim point for multiplication'''
    normal_points = [(point.x, point.y, 0, 1) for point in points]

    '''Multiply the points by the transform matrix for drawing'''
    transformed_points = draw_scale_matrix.dot(
        np.transpose(normal_points))  # Transpose the points to appropriately mutiply

    return np.transpose(transformed_points)[:,
           :3]  # Re-Transpose the points back to remain in a "list of points" format


def viewport_point_on_plane(viewport_point: Vector2, game_area_rect, draw_scale_matrix=None, margin: int = 1):
    points_on_plane = scaled_points_of_a_rect(game_area_rect, Vector2(0, 0), draw_scale_matrix, margin=margin)
    point0 = points_on_plane[0]
    point1 = points_on_plane[1]
    point2 = points_on_plane[2]

    vec1 = point0 - point1
    vec2 = point2 - point1

    normal = np.cross(vec1, vec2)
    a = normal[0]
    b = normal[1]
    c = normal[2]
    d = a * point0[0] + b * point0[1] + c * point0[2]

    z_val = (d - a * viewport_point.x - b * viewport_point.y) / c

    return [viewport_point.x, viewport_point.y, z_val]


def scaled_points_to_normal_points(points: List[IVector], draw_scale_matrix=None):
    translated_points = [(point.x, point.y, 0, 1) for point in points]
    normal_array = scaled_array_to_normal_array(scaled_array=translated_points, draw_scale_matrix=draw_scale_matrix)
    normal_points = [Vector2(point[0], point[1]) for point in normal_array]

    return normal_points


def scaled_array_to_normal_array(scaled_array, draw_scale_matrix=None):
    if draw_scale_matrix is None:
        draw_scale_matrix = np.identity(4)

    draw_scale_matrix_inv = np.linalg.inv(draw_scale_matrix)
    normal_points = draw_scale_matrix_inv.dot(np.transpose(scaled_array))

    normal_points = np.reshape(normal_points, (-1, 2))

    return normal_points


def normal_points_to_scaled_points(points: List[Vector2], draw_scale_matrix=None):
    return scaled_points_of_points(points, draw_scale_matrix)


def mouse_in_plane_point(game_area_rect: Rectangle, draw_scale_matrix=None):
    # test = draw_scale_matrix_inv.dot(draw_scale_matrix)
    """Gets the mouse position and converts it to a grid position"""
    mouse_game_area_coord = game_area_coords_from_parent_coords(parent_coords=mouse_pos_as_vector(),
                                                                game_area_surface_rectangle=game_area_rect)
    mouse_plane_point = viewport_point_on_plane(mouse_game_area_coord, game_area_rect, draw_scale_matrix, margin=1)

    return mouse_plane_point


def normal_mouse_position(game_area_rect: Rectangle, draw_scale_matrix=None) -> Vector2:
    # test = draw_scale_matrix_inv.dot(draw_scale_matrix)
    """Gets the mouse position and converts it to a grid position"""
    # mouse_game_area_coord = game_area_coords_from_parent_coords(parent_coords=mouse_pos_as_vector(), game_area_surface_rectangle=game_area_rect)
    mouse_plane_point = mouse_in_plane_point(game_area_rect, draw_scale_matrix)
    points = np.array([mouse_plane_point[0], mouse_plane_point[1], mouse_plane_point[2], 1])

    normal_array = scaled_array_to_normal_array(points, draw_scale_matrix)

    return Vector2(normal_array[0][0], normal_array[0][1])