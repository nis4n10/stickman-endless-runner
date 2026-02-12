import pygame
import random
import sys

# -----------------------------
# Initialize Pygame
# -----------------------------
pygame.init()
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stickman Endless Runner")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24, bold=True)

# -----------------------------
# Colors
# -----------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 100, 255)

# -----------------------------
# Game Variables
# -----------------------------
gravity = 1
ground_y = HEIGHT - 80

# -----------------------------
# Button Class
# -----------------------------
class Button:
    def __init__(self, x, y, w, h, text, color=GRAY, hover_color=BLUE):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color

    def draw(self, surf):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(surf, self.hover_color, self.rect)
        else:
            pygame.draw.rect(surf, self.color, self.rect)
        text_surf = font.render(self.text, True, WHITE)
        surf.blit(text_surf, (self.rect.centerx - text_surf.get_width()//2,
                              self.rect.centery - text_surf.get_height()//2))

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

# -----------------------------
# Stickman Class
# -----------------------------
class Stickman:
    def __init__(self):
        self.x = 150
        self.y = ground_y
        self.vy = 0
        self.width = 20
        self.height = 50
        self.on_ground = True

    def jump(self):
        if self.on_ground:
            self.vy = -15
            self.on_ground = False

    def update(self):
        self.vy += gravity
        self.y += self.vy
        if self.y >= ground_y:
            self.y = ground_y
            self.vy = 0
            self.on_ground = True

    def draw(self, surf):
        # Head
        pygame.draw.circle(surf, BLACK, (int(self.x), int(self.y- self.height)), 10)
        # Body
        pygame.draw.line(surf, BLACK, (self.x, self.y - self.height + 10), (self.x, self.y - 10), 4)
        # Arms
        pygame.draw.line(surf, BLACK, (self.x, self.y - self.height + 20), (self.x - 15, self.y - self.height + 35), 3)
        pygame.draw.line(surf, BLACK, (self.x, self.y - self.height + 20), (self.x + 15, self.y - self.height + 35), 3)
        # Legs
        pygame.draw.line(surf, BLACK, (self.x, self.y - 10), (self.x - 10, self.y + 15), 3)
        pygame.draw.line(surf, BLACK, (self.x, self.y - 10), (self.x + 10, self.y + 15), 3)

# -----------------------------
# Obstacle Class
# -----------------------------
class Obstacle:
    def __init__(self):
        self.width = random.randint(20, 40)
        self.height = random.randint(30, 50)
        self.x = WIDTH
        self.y = ground_y
        self.color = RED

    def update(self, speed):
        self.x -= speed

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, (self.x, self.y - self.height, self.width, self.height))

    def collides_with(self, stickman):
        stick_rect = pygame.Rect(stickman.x - 10, stickman.y - stickman.height, 20, stickman.height)
        obs_rect = pygame.Rect(self.x, self.y - self.height, self.width, self.height)
        return stick_rect.colliderect(obs_rect)

# -----------------------------
# Buttons
# -----------------------------
start_button = Button(WIDTH//2 - 75, HEIGHT//2 - 25, 150, 50, "START")
restart_button = Button(WIDTH//2 - 75, HEIGHT//2 + 20, 150, 50, "RESTART")
quit_button = Button(WIDTH//2 - 75, HEIGHT//2 + 90, 150, 50, "QUIT")

# -----------------------------
# Game Loop
# -----------------------------
def game_loop():
    stickman = Stickman()
    obstacles = []
    obstacle_timer = 0
    speed = 8
    score = 0
    game_over = False

    while True:
        screen.fill(WHITE)
        pygame.draw.rect(screen, GREEN, (0, ground_y, WIDTH, HEIGHT - ground_y))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if not game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        stickman.jump()
            else:
                if restart_button.is_clicked(event):
                    return  # Restart game
                if quit_button.is_clicked(event):
                    pygame.quit()
                    sys.exit()

        # Update stickman
        if not game_over:
            stickman.update()

        # Spawn obstacles
        obstacle_timer += 1
        if obstacle_timer > 60:
            obstacles.append(Obstacle())
            obstacle_timer = 0

        # Update and draw obstacles
        for obs in obstacles[:]:
            if not game_over:
                obs.update(speed)
            obs.draw(screen)
            if obs.collides_with(stickman):
                game_over = True
            if obs.x + obs.width < 0:
                obstacles.remove(obs)

        # Draw stickman
        stickman.draw(screen)

        # Update score
        if not game_over:
            score += 1

        # Display score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10,10))

        # Game over screen
        if game_over:
            over_text = font.render("Game Over!", True, BLACK)
            screen.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2 - 60))
            restart_button.draw(screen)
            quit_button.draw(screen)

        pygame.display.update()
        clock.tick(60)

# -----------------------------
# Main Menu Loop
# -----------------------------
while True:
    screen.fill(WHITE)
    title = font.render("Stickman Endless Runner", True, BLACK)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 100))
    start_button.draw(screen)
    quit_button.draw(screen)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if start_button.is_clicked(event):
            game_loop()
        if quit_button.is_clicked(event):
            pygame.quit()
            sys.exit()
