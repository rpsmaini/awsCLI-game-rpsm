import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, screen_width):
        super().__init__()
        self.screen_width = screen_width
        
        # Enemy appearance
        self.image = pygame.Surface((50, 80))
        self.image.fill((100, 100, 100))  # Gray color
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Movement variables
        self.speed = random.randint(2, 4)
        self.direction = -1 if x > screen_width // 2 else 1  # Move toward center initially
        
        # Combat variables
        self.health = 30
        self.attack_cooldown = 0
        self.attack_range = 60
        self.points_value = 100
        
        # AI behavior state
        self.state = "patrol"  # patrol, chase, attack
        self.detection_range = 200
    
    def update(self, player_rect):
        # Update attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        # AI behavior based on state
        player_distance = abs(self.rect.centerx - player_rect.centerx)
        
        # Change state based on player distance
        if player_distance < self.attack_range:
            self.state = "attack"
        elif player_distance < self.detection_range:
            self.state = "chase"
        else:
            self.state = "patrol"
        
        # Act based on current state
        if self.state == "patrol":
            self._patrol()
        elif self.state == "chase":
            self._chase(player_rect)
        elif self.state == "attack":
            self._attack(player_rect)
    
    def _patrol(self):
        # Move back and forth
        self.rect.x += self.speed * self.direction
        
        # Change direction if reaching screen edges
        if self.rect.left <= 0:
            self.direction = 1
        elif self.rect.right >= self.screen_width:
            self.direction = -1
    
    def _chase(self, player_rect):
        # Move toward player
        if self.rect.centerx < player_rect.centerx:
            self.rect.x += self.speed
            self.direction = 1
        else:
            self.rect.x -= self.speed
            self.direction = -1
    
    def _attack(self, player_rect):
        # Face the player
        if self.rect.centerx < player_rect.centerx:
            self.direction = 1
        else:
            self.direction = -1
        
        # Attack if cooldown is ready
        if self.attack_cooldown == 0:
            self.attack_cooldown = 60  # Attack every 60 frames (1 second at 60 FPS)
            return True  # Signal that enemy is attacking
        
        return False
    
    def take_damage(self, amount):
        self.health -= amount
        return self.health <= 0  # Return True if enemy is defeated
    
    def get_points(self):
        return self.points_value
