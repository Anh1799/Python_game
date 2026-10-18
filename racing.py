
import pygame
import random

# Initialize Pygame
pygame.init()

# Window settings
WIDTH = 500
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Racing Game")

# Colors
GREEN = (30, 150, 60)
GRAY = (60, 60, 60)
WHITE = (255, 255, 255)
YELLOW = (255, 220, 0)
BLUE = (0, 130, 255)
RED = (255, 50, 50)
BLACK = (0, 0, 0)

# Game settings
clock = pygame.time.Clock()
FPS = 60

# Road settings
ROAD_LEFT = 80
ROAD_RIGHT = 420
road_offset = 0

# Car settings
CAR_WIDTH = 45
CAR_HEIGHT = 80
PLAYER_SPEED = 6

player = pygame.Rect(
    WIDTH // 2 - CAR_WIDTH // 2,
    HEIGHT - 120,
    CAR_WIDTH,
    CAR_HEIGHT
)

# Enemy settings
enemies = []
enemy_speed = 5
spawn_delay = 900
last_spawn = pygame.time.get_ticks()

# Game state
score = 0
game_over = False
running = True

# Fonts
font = pygame.font.SysFont("Arial", 28)
big_font = pygame.font.SysFont("Arial", 50)

# Draw a car
def draw_car(rect, color):
    # Car body
    pygame.draw.rect(
        screen, color, rect,
        border_radius=8
    )

    # Windshield
    pygame.draw.rect(
        screen, (170, 220, 255),
        (rect.x + 8, rect.y + 15,
         rect.width - 16, 20),
        border_radius=4
    )

    # Rear window
    pygame.draw.rect(
        screen, (100, 170, 220),
        (rect.x + 8, rect.y + 50,
         rect.width - 16, 15),
        border_radius=4
    )

    # Wheels
    pygame.draw.rect(
        screen, BLACK,
        (rect.x - 6, rect.y + 12, 6, 20)
    )
    pygame.draw.rect(
        screen, BLACK,
        (rect.right, rect.y + 12, 6, 20)
    )
    pygame.draw.rect(
        screen, BLACK,
        (rect.x - 6, rect.y + 50, 6, 20)
    )
    pygame.draw.rect(
        screen, BLACK,
        (rect.right, rect.y + 50, 6, 20)
    )

# Draw scrolling road
def draw_road():
    global road_offset

    screen.fill(GREEN)

    # Road surface
    pygame.draw.rect(
        screen, GRAY,
        (ROAD_LEFT, 0,
         ROAD_RIGHT - ROAD_LEFT, HEIGHT)
    )

    # Road edges
    pygame.draw.line(
        screen, WHITE,
        (ROAD_LEFT, 0), (ROAD_LEFT, HEIGHT), 5
    )
    pygame.draw.line(
        screen, WHITE,
        (ROAD_RIGHT, 0), (ROAD_RIGHT, HEIGHT), 5
    )

    # Moving lane lines
    for y in range(-100, HEIGHT, 100):
        line_y = y + road_offset

        for x in [193, 307]:
            pygame.draw.rect(
                screen, YELLOW,
                (x, line_y, 6, 50)
            )

    road_offset = (road_offset + enemy_speed) % 100

# Create enemy car
def spawn_enemy():
    lane_centers = [136, 250, 364]
    x = random.choice(lane_centers) - CAR_WIDTH // 2

    enemy = pygame.Rect(
        x, -CAR_HEIGHT,
        CAR_WIDTH, CAR_HEIGHT
    )

    enemies.append(enemy)

# Reset game
def reset_game():
    global score, enemy_speed
    global spawn_delay, game_over, last_spawn
    global road_offset

    score = 0
    enemy_speed = 5
    spawn_delay = 900
    game_over = False
    road_offset = 0

    enemies.clear()

    player.centerx = WIDTH // 2
    last_spawn = pygame.time.get_ticks()

# Main game loop
while running:
    clock.tick(FPS)
    current_time = pygame.time.get_ticks()

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if game_over and event.key == pygame.K_r:
                reset_game()

    if not running:
        break

    # Game logic
    if not game_over:

        keys = pygame.key.get_pressed()

        # Move player left
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.x -= PLAYER_SPEED

        # Move player right
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.x += PLAYER_SPEED

        # Keep car inside road
        player.left = max(
            player.left, ROAD_LEFT + 10
        )
        player.right = min(
            player.right, ROAD_RIGHT - 10
        )

        # Spawn enemy cars
        if current_time - last_spawn >= spawn_delay:
            spawn_enemy()
            last_spawn = current_time

        # Move enemy cars
        for enemy in enemies[:]:
            enemy.y += enemy_speed

            # Enemy passes bottom of screen
            if enemy.top > HEIGHT:
                enemies.remove(enemy)
                score += 10

                # Increase difficulty
                enemy_speed = min(
                    12, 5 + score // 50
                )

                spawn_delay = max(
                    350, 900 - score * 2
                )

            # Detect collision
            elif player.colliderect(enemy):
                game_over = True

    # Draw everything
    draw_road()
    draw_car(player, BLUE)

    for enemy in enemies:
        draw_car(enemy, RED)

    # Display score
    score_text = font.render(
        f"Score: {score}", True, WHITE
    )
    screen.blit(score_text, (15, 15))

    # Game Over screen
    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(190)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        text = big_font.render(
            "GAME OVER", True, RED
        )
        screen.blit(
            text,
            text.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 - 60)
            )
        )

        final_score = font.render(
            f"Final Score: {score}", True, WHITE
        )
        screen.blit(
            final_score,
            final_score.get_rect(
                center=(WIDTH // 2, HEIGHT // 2)
            )
        )

        restart = font.render(
            "Press R to Restart", True, WHITE
        )
        screen.blit(
            restart,
            restart.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 + 50)
            )
        )

    pygame.display.flip()

pygame.quit()
