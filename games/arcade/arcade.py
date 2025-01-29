"""
Space Shooter Game with Advanced Features
Features:
- Player ship with movement and dual fire modes
- Armed asteroids that return fire
- Different bullet types with unique behaviors
- Score tracking and game state management
"""

import pygame
import random
import math

# === Initialize Pygame ===
pygame.init()

# === Game Constants ===
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
PLAYER_SPEED = 7
BULLET_SPEED = -10  # Negative for upward movement
ASTEROID_MIN_SPEED = 3
ASTEROID_MAX_SPEED = 6

# === Color Definitions ===
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# === Initialize Display ===
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)  # Default font

class Player(pygame.sprite.Sprite):
    """
    Player-controlled spaceship with dual fire modes
    Key features:
    - Horizontal movement with arrow keys
    - Automatic firing when space is held
    - Fire mode switching (TAB key)
    - Cooldown system for balanced shooting
    """
    def __init__(self):
        super().__init__()
        # Ship visualization (triangle)
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, GREEN, [(15, 0), (0, 30), (30, 30)])
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT-50))
        
        # Shooting properties
        self.shoot_cooldown = 0
        self.fire_mode = "airburst"  # Initial mode
        self.shot_counter = 0  # For airburst timing

    def update(self):
        """Handle movement and automatic firing"""
        # Horizontal movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED
        
        # Continuous firing when space is held
        if keys[pygame.K_SPACE]:
            self.shoot()
        
        # Keep player in bounds
        self.rect.clamp_ip(screen.get_rect())
        
        # Cooldown management
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def shoot(self):
        """Create bullets based on current fire mode"""
        if self.shoot_cooldown == 0:
            if self.fire_mode == "airburst":
                self.shot_counter += 1
                # Every 5th shot is a powerful airburst
                if self.shot_counter % 5 == 0:
                    AirburstBullet(self.rect.centerx, self.rect.top)
                else:
                    Bullet(self.rect.centerx, self.rect.top)
            else:  # Birdshot mode
                # Create spread pattern
                for dx in [-3, 0, 3]:
                    BirdShotBullet(self.rect.centerx, self.rect.top, dx)
            
            self.shoot_cooldown = 10  # Reset cooldown

    def toggle_fire_mode(self):
        """Switch between airburst and birdshot modes"""
        self.fire_mode = "birdshot" if self.fire_mode == "airburst" else "airburst"

class Bullet(pygame.sprite.Sprite):
    """Base class for all player projectiles"""
    def __init__(self, x, y):
        super().__init__(bullets, all_sprites)
        self.image = pygame.Surface((4, 15))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        """Vertical movement and cleanup"""
        self.rect.y += BULLET_SPEED
        if self.rect.bottom < 0:  # Off-screen check
            self.kill()

class AirburstBullet(Bullet):
    """Special high-impact bullet"""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.Surface((8, 20))  # Larger size
        self.image.fill(YELLOW)  # Distinct color

class BirdShotBullet(Bullet):
    """Spread-fire projectile with lateral movement"""
    def __init__(self, x, y, dx):
        super().__init__(x, y)
        self.image = pygame.Surface((6, 12))
        self.image.fill((0, 255, 255))  # Cyan color
        self.dx = dx  # Horizontal movement component

    def update(self):
        """Diagonal movement pattern"""
        self.rect.x += self.dx
        super().update()

class Asteroid(pygame.sprite.Sprite):
    """Enemy asteroid with combat capabilities"""
    def __init__(self, player):
        super().__init__(asteroids, all_sprites)
        # Basic properties
        self.image = pygame.Surface((40, 40))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(
            center=(random.randint(20, SCREEN_WIDTH-20), -20)
        )
        self.speed = random.randint(ASTEROID_MIN_SPEED, ASTEROID_MAX_SPEED)
        
        # Combat properties
        self.player = player  # Reference for targeting
        self.shoot_cooldown = random.randint(30, 90)  # Initial delay

    def update(self):
        """Movement and combat logic"""
        # Vertical movement
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
        
        # Shooting logic
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        else:
            # 2% chance per frame to shoot when cooldown is ready
            if random.random() < 0.02:
                self.shoot()
                self.shoot_cooldown = random.randint(60, 120)

    def shoot(self):
        """Fire projectile at player's current position"""
        # Calculate direction vector
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)
        
        if distance != 0:
            # Normalize direction and create projectile
            EnemyProjectile(self.rect.centerx, self.rect.centery, dx/distance, dy/distance)

class EnemyProjectile(pygame.sprite.Sprite):
    """Asteroid-fired projectile with tracking"""
    def __init__(self, x, y, dir_x, dir_y):
        super().__init__(enemy_projectiles, all_sprites)
        self.image = pygame.Surface((8, 8))
        self.image.fill(ORANGE)  # Distinct color
        self.rect = self.image.get_rect(center=(x, y))
        
        # Movement properties
        self.speed = 5
        self.dx = dir_x * self.speed  # Locked direction
        self.dy = dir_y * self.speed  # No continuous tracking

    def update(self):
        """Persistent directional movement"""
        self.rect.x += self.dx
        self.rect.y += self.dy
        # Cleanup when off-screen
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

# === Game Initialization ===
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
enemy_projectiles = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# Game state
score = 0
game_over = False

# === Main Game Loop ===
running = True
while running:
    clock.tick(FPS)
    
    # === Event Handling ===
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                player.toggle_fire_mode()
            if event.key == pygame.K_r and game_over:
                # Reset game state
                game_over = False
                score = 0
                player.shot_counter = 0
                player.rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT-50)
                # Clear all sprites except player
                for sprite in all_sprites:
                    if sprite != player:
                        sprite.kill()        
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit(0)



    # === Game Logic ===
    if not game_over:
        # Asteroid spawning
        if random.random() < 0.02:
            Asteroid(player)

        # Update all game objects
        all_sprites.update()

        # === Collision Detection ===
        # Player vs asteroids/enemy projectiles
        if (pygame.sprite.spritecollide(player, asteroids, True) or
            pygame.sprite.spritecollide(player, enemy_projectiles, True)):
            game_over = True
        
        # Bullets vs asteroids
        for bullet in pygame.sprite.groupcollide(bullets, asteroids, True, True):
            score += 10

    # === Rendering ===
    screen.fill(BLACK)
    all_sprites.draw(screen)
    
    # UI Elements
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    mode_text = font.render(f"Mode: {player.fire_mode.upper()}", True, WHITE)
    screen.blit(mode_text, (10, 50))

    # Game Over display
    if game_over:
        game_over_text = font.render("Game Over! Press R to restart", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - 180, SCREEN_HEIGHT//2))

    pygame.display.flip()

pygame.quit()