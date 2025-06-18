import math
import time

import pygame

STACK_ROTATION = False
ROTATION_SPEED = 0.01

class Circle:
    def __init__(self, r, omega, x = 0, y = 0, child = None, angle = 0):
        self.r = r
        self.omega = omega
        self.x = x
        self.y = y
        self.angle = angle
        self.child = child
        self.child_x, self.child_y = 0, 0
        self.path = []

    def update(self, x = None, y = None, angle_offset = 0):
        # update angle and postion, and calculate child position

        if not STACK_ROTATION:
            angle_offset = 0

        if x is not None: # used for root circle
            self.x, self.y = x, y
        self.angle -= self.omega * ROTATION_SPEED
        self.child_x = self.x + self.r * math.cos(self.angle + angle_offset)
        self.child_y = self.y + self.r * math.sin(self.angle + angle_offset)

        if self.child is not None:
            # upadte child
            self.child.update(self.child_x, self.child_y, self.angle + angle_offset)
        else:
            # no child, so this is the circle that draws the path
            self.path.append((self.child_x, self.child_y))

    def draw(self, screen):
        if self.child is not None:
            self.child.draw(screen)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x), int(self.y)), self.r, width=1)
        pygame.draw.circle(screen, (255, 0, 0) if self.child is None else (0, 0, 0), (int(self.child_x), int(self.child_y)), 5)
        pygame.draw.line(screen, (0, 0, 0), (int(self.x), int(self.y)), (int(self.child_x), int(self.child_y)), width=1)

    def get_path(self):
        if self.child is None:
            return self.path
        else:
            return self.child.get_path()

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()
    c = Circle(100, 0)
    c = Circle(100, 5, child=c, angle=math.pi)
    c = Circle(100, -5, x = 400, y = 400, child=c)

    time.sleep(5)

    running = True
    while running:
        screen.fill((255, 255, 255))
        
        c.update()

        path = c.get_path()
        if len(path) > 1:
            pygame.draw.lines(screen, (128, 0, 0), False, [(int(x), int(y)) for x, y in path], 2)

        c.draw(screen)

        pygame.display.flip()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()