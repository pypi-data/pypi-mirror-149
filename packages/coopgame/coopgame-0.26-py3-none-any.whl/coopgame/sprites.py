import pygame
from coopstructs.vectors import Vector2
from coopgame.colors import Color
from typing import Dict, Tuple, Any
from enum import Enum


class SpriteOriginPosition(Enum):
    CENTER = 1
    BOTTOM_MIDDLE = 2
    BOTTOM_RIGHT = 3
    TOP_LEFT = 4


class MySprite(pygame.sprite.Sprite):
    def __init__(self,
                 id: str,
                 init_pos: Vector2,
                 width: int,
                 height: int,
                 sprite_origin_position: SpriteOriginPosition = None
                 ):
        super().__init__()

        self.id = id

        # Pass in the color of the car, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.surf = pygame.Surface([width, height]).convert()
        self.surf.fill(Color.PINK.value)
        self.surf.set_colorkey(Color.PINK.value)

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.surf.get_rect()
        self.set_pos(init_pos, sprite_origin_position)

    @property
    def bottom_center_pos(self) -> Vector2:
        x = self.rect.x + self.rect.width / 2
        y = self.rect.y + self.rect.height

        return Vector2(x, y)

    def _center_from_sprite_origin(self, pos: Vector2, sprite_origin_position: SpriteOriginPosition):
        if sprite_origin_position == SpriteOriginPosition.CENTER:
            ret = (pos.x, pos.y)
        elif sprite_origin_position == SpriteOriginPosition.BOTTOM_MIDDLE:
            ret = (pos.x, pos.y - self.surf.get_height() / 2)
        elif sprite_origin_position == SpriteOriginPosition.BOTTOM_RIGHT:
            ret = (pos.x - self.surf.get_width() / 2, pos.y - self.surf.get_height() / 2)
        elif sprite_origin_position == SpriteOriginPosition.TOP_LEFT:
            ret = (pos.x + self.surf.get_width() / 2, pos.y + self.surf.get_height() / 2)
        else:
            raise NotImplementedError(f"origin pos: {sprite_origin_position} not handled for finding center")
        return ret

    def set_pos(self, pos: Vector2, sprite_origin_position: SpriteOriginPosition = None):
        if sprite_origin_position is None:
            sprite_origin_position = SpriteOriginPosition.CENTER

        center = self._center_from_sprite_origin(pos, sprite_origin_position)

        self.rect = self.surf.get_rect(center=center)

    def blit(self, surface: pygame.Surface, display_handle: bool = False, display_rect: bool = False):

        surface.blit(self.surf, (self.rect.x, self.rect.y))
        if display_handle:
            pygame.draw.rect(surface, Color.RED.value, [self.rect.x, self.rect.y, 1, 1])
        if display_rect:
            pygame.draw.rect(surface, Color.RED.value, [self.rect.x, self.rect.y, self.rect.width, self.rect.height], 1)

    def __repr__(self):
        return f"{self.id} {super().__repr__()}"


class RectangleSprite(MySprite):
    def __init__(self, id: str, init_pos: Vector2, color: Color, width: int, height: int):
        # Call the parent class (Sprite) constructor
        MySprite.__init__(self, id, init_pos, width, height)

        pygame.draw.rect(self.surf, color.value, [0, 0, width, height])


class ImageSprite(MySprite):
    def __init__(self,
                 id: str,
                 init_pos: Vector2,
                 width: int,
                 height: int):
        # Call the parent class (Sprite) constructor
        MySprite.__init__(self, id, init_pos, width, height)


class AnimatedSprite(MySprite):
    def __init__(self,
                 id: str,
                 init_pos: Vector2,
                 animation_dict: Dict[Any, Tuple],
                 default_animation_key=None,
                 animation_cycle_ms: int = None,
                 width: int = None,
                 height: int = None,
                 sprite_origin_position: SpriteOriginPosition = None,
                 loop: bool = False):
        self._animation_dict = animation_dict

        self._animation_key = default_animation_key
        self._animation_index = 0

        # Call the parent class (Sprite) constructor
        first_image = next(iter(self._animation_dict.values()))[0]
        width = first_image.get_width() if not width else width
        height = first_image.get_height() if not height else height
        self.size = (width, height)
        MySprite.__init__(self, id, init_pos, width, height, sprite_origin_position)

        self.loop = loop
        self.animate_timer = 0
        self.animate_cycle = animation_cycle_ms if animation_cycle_ms else 100

        self.image = None
        self._set_image()

    def set_animation(self, animation: str):
        if animation in self._animation_dict.keys() and animation != self.current_animation:
            self._animation_key = animation
            self._animation_index = 0

    def increment_animation_phase(self, loop: bool = True):
        ''':return True if animation cycle has completed, False if still in cycle
        :param loop allows caller to specify whether or not to loop the aniimation (default True)'''
        ret = False
        self._animation_index += 1
        if self._animation_index >= len(self._animation_dict[self._animation_key]):
            self._animation_index = 0 if loop else len(self._animation_dict[self._animation_key]) - 1
            ret = True

        self._set_image()
        return ret

    def _set_image(self):
        self.surf.fill(Color.PINK.value)
        self.image = self._animation_dict[self._animation_key][self._animation_index]
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.surf.blit(self.image, (0, 0))

    @property
    def current_animation(self):
        return self._animation_key

    def animate(self,
                delta_time_ms: int):
        self.animate_timer += delta_time_ms
        if self.animate_timer > self.animate_cycle:
            self.increment_animation_phase(self.loop)
            self.animate_timer = 0

