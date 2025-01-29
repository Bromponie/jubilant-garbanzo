import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle dimensions
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100

# Ball dimensions
BALL_SIZE = 20

# Initialize font for scoring
font = pygame.font.SysFont('Arial', 74)

# Score variables
left_score = 0
right_score = 0

# Paddle positions
left_paddle_y = (HEIGHT - PADDLE_HEIGHT) // 2
right_paddle_y = (HEIGHT - PADDLE_HEIGHT) // 2

# Ball position and speed
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_speed_x, ball_speed_y = 7, 7

# Paddle speed
paddle_speed = 10

# Clock
clock = pygame.time.Clock()

def draw_objects():
    screen.fill(BLACK)
    # Draw paddles
    pygame.draw.rect(screen, WHITE, (50, left_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, WHITE, (WIDTH - 50 - PADDLE_WIDTH, right_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    # Draw ball
    pygame.draw.ellipse(screen, WHITE, (ball_x - BALL_SIZE // 2, ball_y - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE))
    # Draw scores
    left_score_text = font.render(str(left_score), True, WHITE)
    right_score_text = font.render(str(right_score), True, WHITE)
    screen.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    screen.blit(right_score_text, (3*WIDTH//4 - right_score_text.get_width()//2, 20))
    pygame.display.flip()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle_y > 0:
        left_paddle_y -= paddle_speed
    if keys[pygame.K_s] and left_paddle_y < HEIGHT - PADDLE_HEIGHT:
        left_paddle_y += paddle_speed
    if keys[pygame.K_UP] and right_paddle_y > 0:
        right_paddle_y -= paddle_speed
    if keys[pygame.K_DOWN] and right_paddle_y < HEIGHT - PADDLE_HEIGHT:
        right_paddle_y += paddle_speed
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit(0)



    # Ball movement
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Ball collision with top and bottom walls
    if ball_y - BALL_SIZE // 2 <= 0 or ball_y + BALL_SIZE // 2 >= HEIGHT:
        ball_speed_y *= -1

    # Ball collision with paddles
    if (ball_x - BALL_SIZE // 2 <= 50 + PADDLE_WIDTH and
        left_paddle_y <= ball_y <= left_paddle_y + PADDLE_HEIGHT):
        ball_speed_x *= -1

    if (ball_x + BALL_SIZE // 2 >= WIDTH - 50 - PADDLE_WIDTH and
        right_paddle_y <= ball_y <= right_paddle_y + PADDLE_HEIGHT):
        ball_speed_x *= -1

    # Scoring and ball reset
    if ball_x < 0:
        right_score += 1
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2
        ball_speed_x = 7  # Reset direction to the right
    elif ball_x > WIDTH:
        left_score += 1
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2
        ball_speed_x = -7  # Reset direction to the left

    # Draw objects
    draw_objects()

    # Cap the frame rate
    clock.tick(60)
    
    
    