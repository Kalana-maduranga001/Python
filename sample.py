# bouncing_ball.py
# Requires: pip install pygame
import pygame
import random
import sys

pygame.init()
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball")

clock = pygame.time.Clock()

class Ball:
    def __init__(self, x, y, r=20):
        self.x = x
        self.y = y
        self.r = r
        self.vx = random.choice([-200, 200])  # pixels/sec
        self.vy = -300
        self.color = (random.randint(50,255), random.randint(50,255), random.randint(50,255))

    def update(self, dt):
        # gravity
        g = 800  # pixels/sec^2
        self.vy += g * dt
        self.x += self.vx * dt
        self.y += self.vy * dt

        # collisions with walls
        if self.x - self.r < 0:
            self.x = self.r
            self.vx *= -1
        if self.x + self.r > WIDTH:
            self.x = WIDTH - self.r
            self.vx *= -1
        # floor and ceiling
        if self.y + self.r > HEIGHT:
            self.y = HEIGHT - self.r
            self.vy *= -0.8  # lose some energy
            # small threshold to stop jitter
            if abs(self.vy) < 50:
                self.vy = 0
        if self.y - self.r < 0:
            self.y = self.r
            self.vy *= -1

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.r)

balls = [Ball(WIDTH//2, HEIGHT//4, r=24)]

font = pygame.font.SysFont(None, 24)

running = True
while running:
    dt = clock.tick(60) / 1000.0  # seconds since last frame (cap 60 FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # spawn new ball at mouse
            mx, my = event.pos
            balls.append(Ball(mx, my, r=random.randint(12, 36)))
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # update
    for b in balls:
        b.update(dt)

    # draw
    screen.fill((30, 30, 40))
    for b in balls:
        b.draw(screen)

    info = font.render(f"Balls: {len(balls)}  (Click to add, Esc to quit)", True, (220,220,220))
    screen.blit(info, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
