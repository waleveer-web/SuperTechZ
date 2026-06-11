import pygame
import random
import sys

pygame.init()

# Window
WIDTH, HEIGHT = 400, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Game")

# Colors
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
SKIN = (255, 220, 177)
RED = (139, 0 ,0)
# GREEN = (30, 200, 30)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)


# Player car
CAR_WIDTH, CAR_HEIGHT = 40, 70
player_x = WIDTH // 2 - CAR_WIDTH // 2
player_y = HEIGHT - CAR_HEIGHT - 20
player_speed = 9  # faster, more responsive

# Enemy cars
ENEMY_WIDTH, ENEMY_HEIGHT = 50, 70
enemy_speed = 20  # faster enemies
enemies = []

# Score
score = 0
font = pygame.font.SysFont("Arial", 28)

clock = pygame.time.Clock()


def spawn_enemy():
    lane_positions = [100, 180, 260]  # 3 lanes
    x = random.choice(lane_positions)
    y = -ENEMY_HEIGHT
    enemies.append(pygame.Rect(x, y, ENEMY_WIDTH, ENEMY_HEIGHT))


def draw_window():
    WIN.fill(GRAY)

    # Center road line
    pygame.draw.rect(WIN, WHITE, (WIDTH // 2 - 5, 0, 10, HEIGHT))

    # Player car
    pygame.draw.rect(WIN, BLACK, (player_x, player_y, CAR_WIDTH, CAR_HEIGHT))

    # Enemy cars
    for e in enemies:
        pygame.draw.rect(WIN, SKIN, e)

    # Score
    score_text = font.render(f"Score: {score}", True, YELLOW)
    WIN.blit(score_text, (10, 10))

    pygame.display.update()


def game_over():
    text = font.render("YOU FAILED ME", True, RED)
    WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
    pygame.display.update()
    pygame.time.delay(2000)
    pygame.quit()
    sys.exit()


def main():
    global player_x, score, enemy_speed

    spawn_timer = 0

    running = True
    while running:
        clock.tick(60)
        spawn_timer += 1

        # Events (quit)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Spawn enemy every 45 frames
        if spawn_timer > 45:
            spawn_enemy()
            spawn_timer = 0

        # Input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 60:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - CAR_WIDTH - 60:
            player_x += player_speed

        # Move enemies
        for e in enemies:
            e.y += enemy_speed

        # Remove off-screen enemies + increase score
        for e in enemies[:]:
            if e.y > HEIGHT:
                enemies.remove(e)
                score += 1
                enemy_speed += 0.25  # difficulty ramp

        # Collision detection
        player_rect = pygame.Rect(player_x, player_y, CAR_WIDTH, CAR_HEIGHT)
        for e in enemies:
            if player_rect.colliderect(e):
                game_over()

        draw_window()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
