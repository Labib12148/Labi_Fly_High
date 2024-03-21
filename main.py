import asyncio
import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game variables
GRAVITY = 0.25
BIRD_WIDTH = 100
BIRD_HEIGHT = 60
PIPE_WIDTH = 80
GAP_HEIGHT = 250

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Game states
INTRO = 0
PLAYING = 1
GAME_OVER = 2

# Bird class
class Bird:
    def __init__(self):
        self.width = BIRD_WIDTH
        self.height = BIRD_HEIGHT
        self.x = 150
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.image = pygame.image.load("assets/Labi_Fly.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def flap(self):
        self.velocity = -6

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.y = self.y

    def draw(self):
        screen.blit(self.image, self.rect)

# Pipe class
class Pipe:
    def __init__(self, x):
        self.width = PIPE_WIDTH
        self.x = x
        self.height = random.randint(100, SCREEN_HEIGHT - GAP_HEIGHT - 100)
        self.passed = False
        self.pipe_down = pygame.image.load("assets/Pipe_Green_Down.png").convert_alpha()
        self.pipe_up = pygame.image.load("assets/Pipe_Green_Up.png").convert_alpha()
        self.pipe_down = pygame.transform.scale(self.pipe_down, (self.width, self.height))
        self.pipe_up = pygame.transform.scale(self.pipe_up, (self.width, SCREEN_HEIGHT - self.height - GAP_HEIGHT))
        self.rect_down = self.pipe_down.get_rect(topleft=(self.x, 0))
        self.rect_up = self.pipe_up.get_rect(topleft=(self.x, self.height + GAP_HEIGHT))

    def move(self):
        self.x -= 2
        self.rect_down.x = self.x
        self.rect_up.x = self.x

    def draw(self):
        screen.blit(self.pipe_down, self.rect_down)
        screen.blit(self.pipe_up, self.rect_up)

# Intro screen function
def intro_screen():
    screen.fill(WHITE)
    font = pygame.font.SysFont(None, 36)
    title_text = font.render("Labi Bird", True, BLACK)
    start_text = font.render("Press Space To Start", True, BLACK)

    # Positioning the text
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 3))

    # Calculate the position for the bird image
    bird_image = pygame.image.load("assets/Labi_Fly.png").convert_alpha()
    bird_image = pygame.transform.scale(bird_image, (139, 83))
    bird_rect = bird_image.get_rect(center=(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 3) + (SCREEN_HEIGHT // 6)))

    screen.blit(bird_image, (140, 250 ))

    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, bird_rect.bottom + 20))
    

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

async def main():
    bird = Bird()
    pipes = [Pipe(SCREEN_WIDTH + i * 320) for i in range(3)]
    clock = pygame.time.Clock()
    score = 0
    state = INTRO

    # Load background image
    background_image = pygame.image.load("assets/sky.jpg").convert()
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    while True:
        if state == INTRO:
            intro_screen()
            state = PLAYING

        elif state == PLAYING:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bird.flap()

            # Move pipes
            for pipe in pipes:
                pipe.move()

            # Update bird
            bird.update()

            # Check for collisions and update score
            for pipe in pipes:
                if bird.rect.colliderect(pipe.rect_down) or bird.rect.colliderect(pipe.rect_up) \
                        or bird.rect.top <= 0 or bird.rect.bottom >= SCREEN_HEIGHT:
                    state = GAME_OVER
                elif not pipe.passed and bird.rect.x > pipe.rect_down.x + PIPE_WIDTH:
                    pipe.passed = True
                    score += 1

            # Add new pipes
            if pipes[-1].x < SCREEN_WIDTH - 300:
                pipes.append(Pipe(SCREEN_WIDTH))

            # Remove off-screen pipes
            if pipes[0].x < -PIPE_WIDTH:
                pipes.pop(0)

            # Draw background
            screen.blit(background_image, (0, 0))

            # Draw everything
            for pipe in pipes:
                pipe.draw()
            bird.draw()

            # Display score
            font = pygame.font.SysFont(None, 36)
            text = font.render(f'Score: {score}', True, BLACK)
            screen.blit(text, (10, 10))

        elif state == GAME_OVER:
            screen.fill(WHITE)
            font = pygame.font.SysFont(None, 36)
            title_text = font.render("Labi Bird", True, BLACK)
            game_over_text = font.render("Game Over", True, BLACK)
            final_score_text = font.render(f'Final Score: {score}', True, BLACK)
            resume_text = font.render("Press Enter to continue", True, BLACK)

            # Positioning the text
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
            screen.blit(title_text, (150, 10))  # Absolute position for title text
            screen.blit(resume_text, (SCREEN_WIDTH // 2 - resume_text.get_width() // 2, SCREEN_HEIGHT - 50))

            # Calculate the position for the bird image
            bird_image_sad = pygame.image.load("assets/Labi_Fly_Sad.png").convert_alpha()
            bird_image_sad = pygame.transform.scale(bird_image_sad, (139, 83))
            bird_rect = bird_image_sad.get_rect(center=(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 3) + (SCREEN_HEIGHT // 6)))

            screen.blit(bird_image_sad, (140, 250 ))

            screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, bird_rect.bottom + 20))


            pygame.display.update()
            await asyncio.sleep(0)

            # Wait for spacebar to restart the game
            wait_for_enter = True
            while wait_for_enter:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            # Reset game variables
                            bird = Bird()
                            pipes = [Pipe(SCREEN_WIDTH + i * 200) for i in range(3)]
                            score = 0
                            state = PLAYING
                            wait_for_enter = False  # Exit the loop to resume playing

        pygame.display.update()
        clock.tick(60)
        
        asyncio.run(main())