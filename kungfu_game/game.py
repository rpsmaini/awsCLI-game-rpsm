import pygame
import sys
import random
from player import Player
from enemy import Enemy

class KungFuGame:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        
        # Game constants
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.FPS = 60
        self.GROUND_HEIGHT = self.SCREEN_HEIGHT - 50
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BACKGROUND_COLOR = (135, 206, 235)  # Sky blue
        self.GROUND_COLOR = (139, 69, 19)  # Brown
        
        # Set up the display
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Kung Fu Master")
        self.clock = pygame.time.Clock()
        
        # Game state
        self.running = True
        self.game_over = False
        self.score = 0
        self.level = 1
        self.enemy_spawn_timer = 0
        
        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        
        # Create player
        self.player = Player(self.SCREEN_WIDTH // 4, self.GROUND_HEIGHT - 80)
        self.all_sprites.add(self.player)
        
        # Create initial enemies
        self._spawn_enemies(3)
        
        # Load font
        self.font = pygame.font.SysFont(None, 36)
    
    def _spawn_enemies(self, count):
        for _ in range(count):
            x = random.randint(self.SCREEN_WIDTH // 2, self.SCREEN_WIDTH - 100)
            y = self.GROUND_HEIGHT - 80
            enemy = Enemy(x, y, self.SCREEN_WIDTH)
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)
    
    def run(self):
        # Main game loop
        while self.running:
            # Keep the game running at the right speed
            self.clock.tick(self.FPS)
            
            # Handle events
            self._process_events()
            
            # Update game state
            if not self.game_over:
                self._update()
            
            # Draw everything
            self._render()
        
        # Quit the game
        pygame.quit()
        sys.exit()
    
    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.punch()
                elif event.key == pygame.K_UP:
                    self.player.jump(self.GROUND_HEIGHT)
                elif event.key == pygame.K_DOWN:
                    self.player.dodge(self.GROUND_HEIGHT)
                elif event.key == pygame.K_r and self.game_over:
                    self._reset_game()
        
        # Get keys pressed for continuous movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move_left()
        if keys[pygame.K_RIGHT]:
            self.player.move_right()
    
    def _update(self):
        # Update player
        self.player.update(self.GROUND_HEIGHT)
        
        # Keep player within screen bounds
        if self.player.rect.left < 0:
            self.player.rect.left = 0
        if self.player.rect.right > self.SCREEN_WIDTH:
            self.player.rect.right = self.SCREEN_WIDTH
        
        # Update enemies
        for enemy in self.enemies:
            enemy.update(self.player.rect)
            
            # Check if enemy is attacking player
            if enemy.state == "attack" and enemy.attack_cooldown == 59:  # Just started attack
                if not self.player.is_dodging:  # Player gets hit if not dodging
                    self.player.take_damage(10)
        
        # Check for player punch collisions
        punch_rect = self.player.get_punch_rect()
        if punch_rect:
            for enemy in self.enemies:
                if punch_rect.colliderect(enemy.rect):
                    if enemy.take_damage(20):  # Enemy defeated
                        self.score += enemy.get_points()
                        enemy.kill()
        
        # Spawn new enemies periodically
        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer >= 180:  # Every 3 seconds (at 60 FPS)
            self._spawn_enemies(1)
            self.enemy_spawn_timer = 0
        
        # Check for game over
        if self.player.health <= 0:
            self.game_over = True
    
    def _render(self):
        # Draw background
        self.screen.fill(self.BACKGROUND_COLOR)
        
        # Draw ground
        pygame.draw.rect(self.screen, self.GROUND_COLOR, 
                        (0, self.GROUND_HEIGHT, self.SCREEN_WIDTH, self.SCREEN_HEIGHT - self.GROUND_HEIGHT))
        
        # Draw all sprites
        self.all_sprites.draw(self.screen)
        
        # Draw UI
        self._draw_ui()
        
        # Flip the display
        pygame.display.flip()
    
    def _draw_ui(self):
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, self.BLACK)
        self.screen.blit(score_text, (20, 20))
        
        # Draw health bar
        health_width = 200 * (self.player.health / 100)
        pygame.draw.rect(self.screen, (255, 0, 0), (20, 60, 200, 20))  # Red background
        pygame.draw.rect(self.screen, (0, 255, 0), (20, 60, health_width, 20))  # Green health
        
        # Draw controls reminder
        if not self.game_over:
            controls = self.font.render("Arrows to move, Space to punch", True, self.BLACK)
            self.screen.blit(controls, (self.SCREEN_WIDTH - 350, 20))
        
        # Draw game over screen
        if self.game_over:
            game_over_text = self.font.render("GAME OVER", True, (255, 0, 0))
            restart_text = self.font.render("Press R to restart", True, self.BLACK)
            self.screen.blit(game_over_text, 
                           (self.SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                            self.SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(restart_text, 
                           (self.SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                            self.SCREEN_HEIGHT // 2 + 10))
    
    def _reset_game(self):
        # Reset game state
        self.game_over = False
        self.score = 0
        self.level = 1
        self.enemy_spawn_timer = 0
        
        # Clear all sprites
        self.all_sprites.empty()
        self.enemies.empty()
        
        # Create new player
        self.player = Player(self.SCREEN_WIDTH // 4, self.GROUND_HEIGHT - 80)
        self.all_sprites.add(self.player)
        
        # Create initial enemies
        self._spawn_enemies(3)
