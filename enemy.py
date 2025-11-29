import pygame
import math
from settings import ENEMY_SPEED, ENEMY_HEALTH, ENEMY_DAMAGE, ENEMY_DETECT_RANGE

class Enemy():
    def __init__(self, x, y):
        # Cargar animación del enemigo
        self.animation_frames = []
        for i in range(1, 4):
            try:
                self.animation_frames.append(pygame.image.load(f'assets/demonCybor/pixil-frame-{i}.png'))
            except:
                pass
        
        # Si no se cargaron frames, crear una superficie simple
        if not self.animation_frames:
            temp_surface = pygame.Surface((32, 32))
            temp_surface.fill((255, 0, 0))
            self.animation_frames = [temp_surface]
        
        self.current_frame = 0
        self.animation_time = 0
        self.image = self.animation_frames[self.current_frame]
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Movimiento
        self.velocidad = ENEMY_SPEED
        self.direccion_x = 0
        self.direccion_y = 0
        
        # Combate
        self.health = ENEMY_HEALTH
        self.max_health = ENEMY_HEALTH
        self.damage = ENEMY_DAMAGE
        self.detect_range = ENEMY_DETECT_RANGE
        self.attack_cooldown = 0
        self.attack_interval = 0.5  # segundos entre ataques
        
        # Para parpadear cuando recibe daño
        self.damage_flash_time = 0
        self.damage_flash_duration = 0.1
        
    def dibujar(self, surface):
        # Actualizar animación
        self.animation_time += 1
        if self.animation_time >= 15:  # Cambiar frame cada 15 frames
            self.animation_time = 0
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
            self.image = self.animation_frames[self.current_frame]
        
        # Si está siendo dañado, parpadear
        if self.damage_flash_time > 0:
            temp_image = self.image.copy()
            temp_image.fill((255, 100, 100), special_flags=pygame.BLEND_MULT)
            surface.blit(temp_image, self.rect.topleft)
        else:
            surface.blit(self.image, self.rect.topleft)
        
        # Dibujar barra de vida
        barra_ancho = 32
        barra_alto = 4
        barra_rect = pygame.Rect(self.rect.x, self.rect.y - 10, barra_ancho, barra_alto)
        pygame.draw.rect(surface, (100, 100, 100), barra_rect)
        
        salud_rect = pygame.Rect(self.rect.x, self.rect.y - 10, 
                                 (self.health / self.max_health) * barra_ancho, barra_alto)
        pygame.draw.rect(surface, (0, 255, 0), salud_rect)
        
    def actualizar(self, player_rect, dt, width, height):
        """Actualizar el estado del enemigo"""
        # Reducir cooldown de ataque
        self.attack_cooldown -= dt
        self.damage_flash_time -= dt
        
        # Calcular distancia al jugador
        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery
        distancia = math.sqrt(dx**2 + dy**2)
        
        # Si el jugador está en rango de detección, perseguirlo
        if distancia < self.detect_range and distancia > 0:
            # Normalizar dirección
            self.direccion_x = (dx / distancia) * self.velocidad
            self.direccion_y = (dy / distancia) * self.velocidad
        else:
            # Movimiento aleatorio
            self.direccion_x = 0
            self.direccion_y = 0
        
        # Mover el enemigo
        self.rect.x += self.direccion_x * dt * 100
        self.rect.y += self.direccion_y * dt * 100
        
        # Mantener dentro de pantalla
        self.rect.clamp_ip(pygame.Rect(0, 0, width, height))
    
    def recibir_daño(self, daño):
        """El enemigo recibe daño"""
        self.health -= daño
        self.damage_flash_time = self.damage_flash_duration
        if self.health < 0:
            self.health = 0
    
    def esta_vivo(self):
        """Verificar si el enemigo está vivo"""
        return self.health > 0
    
    def puede_atacar(self):
        """Verificar si el enemigo puede atacar"""
        return self.attack_cooldown <= 0
    
    def atacar(self):
        """Realizar un ataque"""
        if self.puede_atacar():
            self.attack_cooldown = self.attack_interval
            return self.damage
        return 0