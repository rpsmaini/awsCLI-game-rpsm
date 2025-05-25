import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Constants
        self.GRAVITY = 1
        self.JUMP_STRENGTH = 15
        self.SPEED = 5
        
        # Load player images (placeholder for now)
        self.standing_image = pygame.Surface((50, 80))
        self.standing_image.fill((255, 0, 0))  # Red
        
        self.punching_image = pygame.Surface((70, 80))
        self.punching_image.fill((0, 255, 0))  # Green
        
        self.jumping_image = pygame.Surface((50, 80))
        self.jumping_image.fill((255, 255, 0))  # Yellow
        
        self.dodging_image = pygame.Surface((50, 40))
        self.dodging_image.fill((0, 0, 255))  # Blue
        
        # Set initial image and rect
        self.image = self.standing_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Movement state
        self.velocity_y = 0
        self.is_jumping = False
        self.is_punching = False
        self.is_dodging = False
        self.facing_right = True
        
        # Animation timers
        self.punch_timer = 0
        self.dodge_timer = 0
        
        # Game stats
        self.score = 0
        self.health = 100
    
    def update(self, ground_height):
        # Apply gravity if not on ground
        if not self.is_on_ground(ground_height):
            self.velocity_y += self.GRAVITY
            self.rect.y += self.velocity_y
        else:
            self.rect.bottom = ground_height
            self.velocity_y = 0
            self.is_jumping = False
        
        # Handle punch animation
        if self.is_punching:
            self.punch_timer += 1
            if self.punch_timer > 15:  # Punch lasts 15 frames
                self.is_punching = False
                self.punch_timer = 0
                self.image = self.standing_image
        
        # Handle dodge animation
        if self.is_dodging:
            self.dodge_timer += 1
            if self.dodge_timer > 30:  # Dodge lasts 30 frames
                self.is_dodging = False
                self.dodge_timer = 0
                self.image = self.standing_image
                self.rect.y -= 40  # Stand back up
    
    def is_on_ground(self, ground_height):
        return self.rect.bottom >= ground_height
    
    def jump(self, ground_height):
        if self.is_on_ground(ground_height) and not self.is_dodging:
            self.velocity_y = -self.JUMP_STRENGTH
            self.is_jumping = True
            self.image = self.jumping_image
    
    def move_left(self):
        if not self.is_dodging:
            self.rect.x -= self.SPEED
            self.facing_right = False
    
    def move_right(self):
        if not self.is_dodging:
            self.rect.x += self.SPEED
            self.facing_right = True
    
    def punch(self):
        if not self.is_punching and not self.is_dodging:
            self.is_punching = True
            self.punch_timer = 0
            self.image = self.punching_image
    
    def dodge(self, ground_height):
        if self.is_on_ground(ground_height) and not self.is_jumping and not self.is_dodging:
            self.is_dodging = True
            self.dodge_timer = 0
            self.image = self.dodging_image
            self.rect.y += 40  # Move down to simulate crouching
    
    def get_punch_rect(self):
        """Returns a rectangle representing the punch hitbox"""
        if not self.is_punching:
            return None
            
        punch_rect = self.rect.copy()
        if self.facing_right:
            punch_rect.width += 30
        else:
            punch_rect.left -= 30
            punch_rect.width += 30
        
        return punch_rect
    
    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
    
    def add_score(self, points):
        self.score += points
