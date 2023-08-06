import time

import pygame


class FpsTracker:
    def __init__(self, max_fps):
        self.ticks = 0
        self.frame_times = []
        self.fps = None
        self.max_fps = max_fps

        self.clock = pygame.time.Clock()
        self.game_start = None

    def calculate_fps(self, ticks_last_frame: int):
        if len(self.frame_times) > 20:
            self.frame_times.pop(0)

        self.frame_times.append(ticks_last_frame)

        avg_sec_per_frame = sum(self.frame_times) / len(self.frame_times) / 1000.0
        self.fps = 1 / avg_sec_per_frame if avg_sec_per_frame > 0 else 0

    def clock_tick(self):
        self.clock.tick(self.max_fps)

    def set_start(self):
        self.game_start = time.perf_counter()

    @property
    def run_time(self):
        return (time.perf_counter() - self.game_start) if self.game_start else None

    def update(self) -> int:
        t = pygame.time.get_ticks()
        delta_time_ms = (t - self.ticks)
        self.ticks = t
        self.calculate_fps(delta_time_ms)

        return delta_time_ms
