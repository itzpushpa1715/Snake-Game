import pygame
import random
import time

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game with Obstacles")

# Clock for controlling game speed
clock = pygame.time.Clock()

# Snake and food parameters
BLOCK_SIZE = 20
snake_speed = 6  # Reduced speed (slower snake)

# Font for displaying score
font = pygame.font.SysFont("comicsansms", 25)

# Function to display the scoregi
def show_score(score):
    value = font.render(f"Score: {score}", True, WHITE)
    screen.blit(value, [10, 10])

# Main game function
def game():
    game_over = False
    game_close = False

    # Initial position of the snake
    x = WIDTH // 2
    y = HEIGHT // 2

    # Initial movement
    x_change = 0
    y_change = 0

    # Snake's body
    snake_list = []
    snake_length = 1

    # Food position
    food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE

    # Obstacles
    obstacles = [(random.randint(1, WIDTH // BLOCK_SIZE - 1) * BLOCK_SIZE,
                  random.randint(1, HEIGHT // BLOCK_SIZE - 1) * BLOCK_SIZE) for _ in range(5)]

    while not game_over:
        while game_close:
            screen.fill(BLACK)
            message = font.render("Game Over! Press C to Play Again or Q to Quit", True, RED)
            screen.blit(message, [WIDTH // 6, HEIGHT // 3])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change = -BLOCK_SIZE
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change = BLOCK_SIZE
                    x_change = 0

        # Check for boundaries
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True

        x += x_change
        y += y_change
        screen.fill(BLACK)

        # Draw food
        pygame.draw.rect(screen, GREEN, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE])

        # Draw obstacles
        for obs in obstacles:
            pygame.draw.rect(screen, RED, [obs[0], obs[1], BLOCK_SIZE, BLOCK_SIZE])

        # Update snake's body
        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Check for collision with itself
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        # Check for collision with obstacles
        for obs in obstacles:
            if x == obs[0] and y == obs[1]:
                game_close = True

        # Draw the snake
        for segment in snake_list:
            pygame.draw.rect(screen, BLUE, [segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE])

        # Check if snake eats food
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            snake_length += 1

        show_score(snake_length - 1)
        pygame.display.update()

        clock.tick(snake_speed)  # Controls snake speed

    pygame.quit()
    quit()

# Start the game
game()
