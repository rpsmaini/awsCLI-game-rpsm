import pygame
import sys
import os

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 1
JUMP_STRENGTH = 15
PLAYER_SPEED = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BACKGROUND_COLOR = (135, 206, 235)  # Sky blue

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Kung Fu Master")
clock = pygame.time.Clock()

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Placeholder rectangle for the player
        self.image = pygame.Surface((50, 80))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        
        # Movement variables
        self.velocity_y = 0
        self.is_jumping = False
        self.is_punching = False
        self.punch_timer = 0
        self.facing_right = True
        self.is_dodging = False
        self.dodge_timer = 0
        
    def update(self):
        # Apply gravity
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y
        
        # Check if player is on the ground
        if self.rect.bottom >= SCREEN_HEIGHT - 50:  # Ground level
            self.rect.bottom = SCREEN_HEIGHT - 50
            self.velocity_y = 0
            self.is_jumping = False
        
        # Handle punch animation timing
        if self.is_punching:
            self.punch_timer += 1
            if self.punch_timer > 20:  # Punch animation lasts 20 frames
                self.is_punching = False
                self.punch_timer = 0
                # Return to normal appearance
                self.image = pygame.Surface((50, 80))
                self.image.fill(RED)
        
        # Handle dodge animation timing
        if self.is_dodging:
            self.dodge_timer += 1
            if self.dodge_timer > 30:  # Dodge animation lasts 30 frames
                self.is_dodging = False
                self.dodge_timer = 0
                # Return to normal appearance
                self.image = pygame.Surface((50, 80))
                self.image.fill(RED)
    
    def jump(self):
        if not self.is_jumping and not self.is_dodging:
            self.velocity_y = -JUMP_STRENGTH
            self.is_jumping = True
    
    def move_left(self):
        if not self.is_dodging:
            self.rect.x -= PLAYER_SPEED
            self.facing_right = False
    
    def move_right(self):
        if not self.is_dodging:
            self.rect.x += PLAYER_SPEED
            self.facing_right = True
    
    def punch(self):
        if not self.is_punching and not self.is_dodging:
            self.is_punching = True
            self.punch_timer = 0
            # Change appearance for punch
            self.image = pygame.Surface((70, 80))
            self.image.fill(GREEN)
    
    def dodge(self):
        if not self.is_jumping and not self.is_dodging:
            self.is_dodging = True
            self.dodge_timer = 0
            # Change appearance for dodge
            self.image = pygame.Surface((50, 40))
            self.image.fill(BLUE)
            self.rect.y += 40  # Move down to simulate crouching

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x_pos):
        super().__init__()
        self.image = pygame.Surface((50, 80))
        self.image.fill((100, 100, 100))  # Gray color
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x_pos, SCREEN_HEIGHT - 50)
        self.speed = 2
        self.direction = -1  # Moving left initially
    
    def update(self):
        self.rect.x += self.speed * self.direction
        
        # Change direction if reaching screen edges
        if self.rect.left <= 0:
            self.direction = 1
        elif self.rect.right >= SCREEN_WIDTH:
            self.direction = -1

# Create sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Create some enemies
for i in range(3):
    enemy = Enemy(SCREEN_WIDTH - 100 * (i + 1))
    all_sprites.add(enemy)
    enemies.add(enemy)

# Game loop
running = True
while running:
    # Keep the game running at the right speed
    clock.tick(FPS)
    
    # Process input/events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.punch()
            elif event.key == pygame.K_UP:
                player.jump()
            elif event.key == pygame.K_DOWN:
                player.dodge()
    
    # Get keys pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move_left()
    if keys[pygame.K_RIGHT]:
        player.move_right()
    
    # Update
    all_sprites.update()
    
    # Check for collisions between player punches and enemies
    if player.is_punching:
        # Create a temporary rect for the punch area
        punch_rect = player.rect.copy()
        if player.facing_right:
            punch_rect.width += 30
        else:
            punch_rect.left -= 30
            punch_rect.width += 30
        
        # Check for collisions with enemies
        for enemy in enemies:
            if punch_rect.colliderect(enemy.rect):
                enemy.kill()  # Remove the enemy
    
    # Draw / render
    screen.fill(BACKGROUND_COLOR)
    
    # Draw ground
    pygame.draw.rect(screen, (139, 69, 19), (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
    
    # Draw all sprites
    all_sprites.draw(screen)
    
    # Display score and instructions
    font = pygame.font.SysFont(None, 36)
    instructions = font.render("Arrow keys to move, Space to punch", True, BLACK)
    screen.blit(instructions, (10, 10))
    
    # Flip the display
    pygame.display.flip()

# Quit the game
pygame.quit()
sys.exit()
