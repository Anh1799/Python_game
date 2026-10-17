
import pygame
import random

# Initialize Pygame
pygame.init()

# Window settings
WIDTH = 600
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter 🚀")

# Colors
BLACK = (5, 5, 25)
WHITE = (255, 255, 255)
BLUE = (0, 180, 255)
RED = (255, 60, 80)
YELLOW = (255, 230, 0)
GREEN = (0, 255, 120)

# Game clock
clock = pygame.time.Clock()
FPS = 60

# Fonts
font = pygame.font.SysFont("Arial", 28)
big_font = pygame.font.SysFont("Arial", 55)

# Player settings
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 40
PLAYER_SPEED = 6

player = pygame.Rect(
    WIDTH // 2 - PLAYER_WIDTH // 2,
    HEIGHT - 80,
    PLAYER_WIDTH,
    PLAYER_HEIGHT
)

# Bullet settings
BULLET_SPEED = 9
bullets = []
last_shot = 0
SHOOT_DELAY = 250

# Enemy settings
ENEMY_WIDTH = 45
ENEMY_HEIGHT = 40
ENEMY_SPEED = 3
enemies = []
last_spawn = 0
SPAWN_DELAY = 800

# Game state
score = 0
lives = 3
game_over = False

# Create background stars
stars = [
    (random.randint(0, WIDTH),
     random.randint(0, HEIGHT))
    for _ in range(70)
]

# Draw text
def draw_text(text, font, color, x, y):
    image = font.render(text, True, color)
    screen.blit(image, (x, y))

# Draw player's spaceship
def draw_player():
    x = player.centerx
    y = player.y

    points = [
        (x, y),
        (player.left, player.bottom),
        (player.right, player.bottom)
    ]

    pygame.draw.polygon(screen, BLUE, points)
    pygame.draw.rect(
        screen, GREEN,
        (x - 7, y + 20, 14, 15)
    )

# Draw enemies
def draw_enemies():
    for enemy in enemies:
        pygame.draw.ellipse(screen, RED, enemy)
        pygame.draw.circle(
            screen, YELLOW,
            enemy.center, 8
        )

# Draw bullets
def draw_bullets():
    for bullet in bullets:
        pygame.draw.rect(screen, YELLOW, bullet)

# Draw background
def draw_background():
    screen.fill(BLACK)

    for x, y in stars:
        pygame.draw.circle(
            screen, WHITE, (x, y), 2
        )

# Create an enemy
def spawn_enemy():
    x = random.randint(0, WIDTH - ENEMY_WIDTH)

    enemy = pygame.Rect(
        x, -ENEMY_HEIGHT,
        ENEMY_WIDTH, ENEMY_HEIGHT
    )

    enemies.append(enemy)

# Reset game
def reset_game():
    global score, lives, game_over
    global last_shot, last_spawn

    score = 0
    lives = 3
    game_over = False

    bullets.clear()
    enemies.clear()

    player.centerx = WIDTH // 2

    last_shot = pygame.time.get_ticks()
    last_spawn = pygame.time.get_ticks()

# Main game loop
running = True

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

        # Move left
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.x -= PLAYER_SPEED

        # Move right
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.x += PLAYER_SPEED

        # Keep player inside window
        player.x = max(
            0, min(player.x, WIDTH - PLAYER_WIDTH)
        )

        # Shoot bullets
        if keys[pygame.K_SPACE]:
            if current_time - last_shot >= SHOOT_DELAY:
                bullet = pygame.Rect(
                    player.centerx - 3,
                    player.top,
                    6, 15
                )

                bullets.append(bullet)
                last_shot = current_time

        # Move bullets upward
        for bullet in bullets[:]:
            bullet.y -= BULLET_SPEED

            if bullet.bottom < 0:
                bullets.remove(bullet)

        # Spawn enemies
        if current_time - last_spawn >= SPAWN_DELAY:
            spawn_enemy()
            last_spawn = current_time

        # Move enemies downward
        for enemy in enemies[:]:
            enemy.y += ENEMY_SPEED

            # Enemy reaches bottom
            if enemy.top > HEIGHT:
                enemies.remove(enemy)
                lives -= 1

            # Enemy hits player
            elif enemy.colliderect(player):
                enemies.remove(enemy)
                lives -= 1

        # Bullet-enemy collisions
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if bullet.colliderect(enemy):
                    if bullet in bullets:
                        bullets.remove(bullet)

                    enemies.remove(enemy)
                    score += 10
                    break

        # Check game over
        if lives <= 0:
            game_over = True

    # Draw everything
    draw_background()
    draw_player()
    draw_bullets()
    draw_enemies()

    # Show score and lives
    draw_text(f"Score: {score}", font, WHITE, 15, 15)
    draw_text(f"Lives: {max(0, lives)}",
              font, GREEN, WIDTH - 120, 15)

    # Game Over screen
    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(190)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        draw_text(
            "GAME OVER",
            big_font, RED,
            WIDTH // 2 - 170,
            HEIGHT // 2 - 80
        )

        draw_text(
            f"Final Score: {score}",
            font, WHITE,
            WIDTH // 2 - 95,
            HEIGHT // 2
        )

        draw_text(
            "Press R to Restart",
            font, GREEN,
            WIDTH // 2 - 115,
            HEIGHT // 2 + 50
        )

    # Update display
    pygame.display.flip()

pygame.quit()
