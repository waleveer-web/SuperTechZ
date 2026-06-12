import pygame
import random

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 200, 0)

clock = pygame.time.Clock()

bird_x = 80
bird_y = HEIGHT // 2
bird_radius = 15
bird_velocity = 2
gravity = 0.5
jump_strength = -8

pipes = []
pipe_width = 60
pipe_gap = 135
score = 0
game_over = False

def create_pipe():
    top_height = random.randint(50, 300)
    return {
        "x": WIDTH,
        "top": top_height,
        "bottom": top_height + pipe_gap
    }

pipe_timer = 0

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird_velocity = jump_strength

    if not game_over:
        bird_velocity += gravity
        bird_y += bird_velocity

        pipe_timer += 1
        if pipe_timer > 90:
            pipes.append(create_pipe())
            pipe_timer = 0

        for pipe in pipes:
            pipe["x"] -= 3

            if (bird_x + bird_radius > pipe["x"] and
                bird_x - bird_radius < pipe["x"] + pipe_width and
                (bird_y - bird_radius < pipe["top"] or
                 bird_y + bird_radius > pipe["bottom"])):
                game_over = True

            if pipe["x"] + pipe_width < bird_x and not pipe.get("scored", False):
             score += 1
             pipe["scored"] = True

        pipes = [p for p in pipes if p["x"] + pipe_width > 0]

        if bird_y < 0 or bird_y > HEIGHT:
            game_over = True

    screen.fill((135, 206, 235))

    pygame.draw.circle(screen, YELLOW, (int(bird_x), int(bird_y)), bird_radius)

    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, (pipe["x"], 0, pipe_width, pipe["top"]))
        pygame.draw.rect(
            screen,
            GREEN,
            (pipe["x"], pipe["bottom"], pipe_width, HEIGHT - pipe["bottom"])
        )

    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    if game_over:
        game_over_text = font.render("Game Over", True, WHITE)
        screen.blit(game_over_text, (130, HEIGHT // 2))

    pygame.display.flip()

pygame.quit()