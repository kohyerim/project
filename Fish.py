import pygame


class Fish(pygame.Rect):
    def __init__(self, screen, fish, x, y, frame):
        self.screen = screen
        self.frame = frame
        self.fish = fish
        self.x = x
        self.y = y
        self.last_update = 0
        self.current_frame = 0

    def move(self):
        self.x += 1
        rect = self.screen.blit(self.food_animate(self.frame), (self.x, self.y))
        return rect

    def food_animate(self, frame):
        now = pygame.time.get_ticks()
        if now - self.last_update > 100:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frame)
        return frame[self.current_frame]
