import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game variables
GRAVITY = 0.22
BIRD_WIDTH = 100
BIRD_HEIGHT = 60
PIPE_WIDTH = 80
GAP_HEIGHT = 280

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Labi Fly High')

INTRO = 0
PLAYING = 1
GAME_OVER = 2
bg_music = pygame.mixer.Sound("assets/Audio/mii.mp3")
bg_music.play(loops=-1)

class Bird:
    def __init__(self):
        self.width = BIRD_WIDTH
        self.height = BIRD_HEIGHT
        self.x = 80
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.image = pygame.image.load("assets/imgs/Labi_Fly.png").convert_alpha()
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

class Pipe:
    def __init__(self, x):
        self.width = PIPE_WIDTH
        self.x = x
        self.height = random.randint(50, SCREEN_HEIGHT - GAP_HEIGHT - 50)
        self.passed = False
        self.pipe_down = pygame.image.load("assets/imgs/Pipe_Green_Down.png").convert_alpha()
        self.pipe_up = pygame.image.load("assets/imgs/Pipe_Green_Up.png").convert_alpha()
        self.pipe_down = pygame.transform.scale(self.pipe_down, (self.width, self.height))
        self.pipe_up = pygame.transform.scale(self.pipe_up, (self.width, SCREEN_HEIGHT - self.height - GAP_HEIGHT))
        self.rect_down = self.pipe_down.get_rect(topleft=(self.x, 0))
        self.rect_up = self.pipe_up.get_rect(topleft=(self.x, self.height + GAP_HEIGHT))
        self.points_sound = pygame.mixer.Sound("assets/Audio/points.mp3")


    def move(self):
        self.x -= 3
        self.rect_down.x = self.x
        self.rect_up.x = self.x

    def draw(self):
        screen.blit(self.pipe_down, self.rect_down)
        screen.blit(self.pipe_up, self.rect_up)

def intro_screen():
    screen.fill(WHITE)
    font = pygame.font.SysFont(None, 36)
    title_text = font.render("Labi Fly High", True, BLACK)
    start_text = font.render("Press Space To Start", True, BLACK)

    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 3))

    bird_image = pygame.image.load("assets/imgs/Labi_Fly.png").convert_alpha()
    bird_image = pygame.transform.scale(bird_image, (139, 83))
    bird_rect = bird_image.get_rect(center=(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 3) + (SCREEN_HEIGHT // 6)))

    screen.blit(bird_image, (175, 280 ))

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

def main():
    bird = Bird()
    pipes = [Pipe(SCREEN_WIDTH + i * 320) for i in range(5)]
    clock = pygame.time.Clock()
    score = 0
    state = INTRO

    background_image = pygame.image.load("assets/imgs/sky.jpg").convert()
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

            for pipe in pipes:
                pipe.move()

            bird.update()

            for pipe in pipes:
                if bird.rect.colliderect(pipe.rect_down) or bird.rect.colliderect(pipe.rect_up) \
                        or bird.rect.top <= 0 or bird.rect.bottom >= SCREEN_HEIGHT:
                    state = GAME_OVER
                elif not pipe.passed and bird.rect.x > pipe.rect_down.x + PIPE_WIDTH:
                    pipe.passed = True
                    score += 1
                    pipe.points_sound.play()

            if pipes[-1].x < SCREEN_WIDTH - 300:
                pipes.append(Pipe(SCREEN_WIDTH))

            if pipes[0].x < -PIPE_WIDTH:
                pipes.pop(0)

            screen.blit(background_image, (0, 0))

            for pipe in pipes:
                pipe.draw()
            bird.draw()

            font = pygame.font.SysFont(None, 36)
            text = font.render(f'Score: {score}', True, BLACK)
            screen.blit(text, (10, 10))

        elif state == GAME_OVER:
            screen.fill(WHITE)
            font = pygame.font.SysFont(None, 36)
            title_text = font.render("Labi Fly High", True, BLACK)
            game_over_text = font.render("Game Over", True, BLACK)
            final_score_text = font.render(f'Final Score: {score}', True, BLACK)
            resume_text = font.render("Press Enter to continue", True, BLACK)

            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
            screen.blit(title_text, (175, 10))
            screen.blit(resume_text, (SCREEN_WIDTH // 2 - resume_text.get_width() // 2, SCREEN_HEIGHT - 50))

            bird_image_sad = pygame.image.load("assets/imgs/Labi_Fly_Sad.png").convert_alpha()
            bird_image_sad = pygame.transform.scale(bird_image_sad, (139, 83))
            bird_rect = bird_image_sad.get_rect(center=(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 3) + (SCREEN_HEIGHT // 6)))

            screen.blit(bird_image_sad, (175, 280 ))

            screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, bird_rect.bottom + 20))


            pygame.display.update()

            wait_for_enter = True
            while wait_for_enter:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            bird = Bird()
                            pipes = [Pipe(SCREEN_WIDTH + i * 300) for i in range(5)]
                            score = 0
                            state = PLAYING
                            wait_for_enter = False

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()