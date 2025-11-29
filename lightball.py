import pygame
import math

class Lightball:
    """Proyectil de ataque a distancia lanzado por el jugador"""
    
    def __init__(self, x, y, target_x, target_y):
        # Cargar imagen del lightball
        try:
            self.image = pygame.image.load('assets/karel/lightball.png')
        except:
            # Si no existe, crear una esfera simple
            self.image = pygame.Surface((16, 16))
            self.image.fill((255, 255, 0))
            pygame.draw.circle(self.image, (255, 200, 0), (8, 8), 8)
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Velocidad y dirección
        dx = target_x - x
        dy = target_y - y
        distancia = math.sqrt(dx**2 + dy**2)
        
        if distancia > 0:
            self.vel_x = (dx / distancia) * 300  # velocidad en píxeles por segundo
            self.vel_y = (dy / distancia) * 300
        else:
            self.vel_x = 0
            self.vel_y = 0
        
        # Propiedades del proyectil
        self.damage = 30
        self.velocidad = 300  # píxeles por segundo
        self.lifetime = 5.0  # segundos antes de desaparecer
        self.elapsed_time = 0
    
    def actualizar(self, dt, world_width, world_height):
        """Actualizar posición del lightball"""
        self.rect.x += self.vel_x * dt
        self.rect.y += self.vel_y * dt
        self.elapsed_time += dt
        
        # Verificar si está fuera del mundo
        if (self.rect.right < 0 or self.rect.left > world_width or 
            self.rect.bottom < 0 or self.rect.top > world_height):
            return False  # Eliminar proyectil
        
        # Verificar si expiró
        if self.elapsed_time >= self.lifetime:
            return False  # Eliminar proyectil
        
        return True
    
    def dibujar(self, surface):
        """Dibujar el lightball"""
        surface.blit(self.image, self.rect.topleft)
    
    def colisiona_con_enemigo(self, enemy_rect):
        """Verificar si colisiona con un enemigo"""
        return self.rect.colliderect(enemy_rect)
