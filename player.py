import pygame
import math
from settings import VELOCIDAD, PLAYER_MAX_HEALTH, PLAYER_ATTACK_RANGE, PLAYER_ATTACK_DAMAGE, PLAYER_ATTACK_COOLDOWN

class Player():
    def __init__(self, x, y): 
        self.move_images = [pygame.image.load(f'assets/karel/move/pixil-frame-{i}.png') for i in range(5)]
        self.idle_images = [pygame.image.load(f'assets/karel/idle/pixil-frame-{i}.png') for i in range(3)]
        self.attack_image = pygame.image.load('assets/karel/attack.png')
        
        self.current_image = 0
        self.image = self.move_images[self.current_image]
        self.is_moving = False
        self.current_animation = self.move_images
        
        self.rect = self.image.get_rect()  
        self.rect.center = (x, y)
        self.animation_time = 0
        
        self.mirando_a_la_derecha = True   
        
        # Sistema de salud y combate
        self.health = PLAYER_MAX_HEALTH
        self.max_health = PLAYER_MAX_HEALTH
        self.attack_range = PLAYER_ATTACK_RANGE
        self.attack_damage = PLAYER_ATTACK_DAMAGE
        self.attack_cooldown = 0
        self.attacking = False
        self.attack_duration = 0.1  # duración visual del ataque
        
        # Sistema de lightballs para ataques a distancia
        self.lightballs = []
        self.lightball_damage = 30
        self.lightball_cooldown = 1.0  # segundos entre lanzamientos
        self.lightball_attack_cooldown = 0
        
    def dibujar(self, surface):
        flipped_image = pygame.transform.flip(self.image, not self.mirando_a_la_derecha, False)
        surface.blit(flipped_image, self.rect.topleft)
        
        # Dibujar ataque visual (círculo)
        if self.attacking:
            pygame.draw.circle(surface, (255, 255, 0), self.rect.center, self.attack_range, 3)
        
        # Dibujar lightballs
        for lightball in self.lightballs:
            lightball.dibujar(surface)
        
        self.animation_time += 1
        if self.animation_time >= 20:
            self.animation_time = 0
            self.current_image = (self.current_image + 1) % len(self.current_animation)
            self.image = self.current_animation[self.current_image]
        
        self.is_moving = False
        
    def move_up(self):
        self.rect.y -= VELOCIDAD
        self.is_moving = True
        self._update_animation()
        
    def move_down(self):
        self.rect.y += VELOCIDAD
        self.is_moving = True
        self._update_animation()
        
    def move_left(self):
        self.rect.x -= VELOCIDAD
        self.is_moving = True
        self._update_animation()
        self.mirando_a_la_derecha = False
        
    def move_right(self):
        self.rect.x += VELOCIDAD
        self.is_moving = True
        self._update_animation()
        self.mirando_a_la_derecha = True
    
    def _update_animation(self):
        if self.attacking:
            return
        
        if self.is_moving and self.current_animation != self.move_images:
            self.current_animation = self.move_images
            self.current_image = 0
        elif not self.is_moving and self.current_animation != self.idle_images:
            self.current_animation = self.idle_images
            self.current_image = 0
    
    def atacar(self):
        """Inicia un ataque"""
        if self.attack_cooldown <= 0:
            self.attacking = True
            self.attack_cooldown = PLAYER_ATTACK_COOLDOWN
            self.current_animation = [self.attack_image]
            self.current_image = 0
            self.attack_duration = 0.15
            return True
        return False
    
    def auto_atacar_enemigo_cercano(self, enemigos):
        """Auto-ataque a distancia con lightballs al enemigo más cercano"""
        if not enemigos or self.lightball_attack_cooldown > 0:
            return False
        
        # Encontrar enemigo más cercano
        enemigo_cercano = None
        distancia_minima = float('inf')
        
        for enemigo in enemigos:
            dx = enemigo.rect.centerx - self.rect.centerx
            dy = enemigo.rect.centery - self.rect.centery
            distancia = math.sqrt(dx**2 + dy**2)
            
            if distancia < distancia_minima:
                distancia_minima = distancia
                enemigo_cercano = enemigo
        
        # Lanzar lightball al enemigo más cercano si está en rango
        if enemigo_cercano and distancia_minima < 500:  # Rango de lanzamiento
            return self.lanzar_lightball(enemigo_cercano.rect.centerx, enemigo_cercano.rect.centery)
        
        return False
    
    def lanzar_lightball(self, target_x, target_y):
        """Lanzar un lightball hacia el objetivo"""
        if self.lightball_attack_cooldown <= 0:
            from lightball import Lightball
            lightball = Lightball(self.rect.centerx, self.rect.centery, target_x, target_y)
            self.lightballs.append(lightball)
            self.lightball_attack_cooldown = self.lightball_cooldown
            return True
        return False
    
    def actualizar(self, dt):
        """Actualizar el estado del jugador cada frame"""
        self.attack_cooldown -= dt
        self.lightball_attack_cooldown -= dt
        
        if self.attack_duration > 0:
            self.attack_duration -= dt
        else:
            self.attacking = False
            if self.current_animation == [self.attack_image]:
                self._update_animation()
        
        # Actualizar lightballs
        lightballs_a_eliminar = []
        for i, lightball in enumerate(self.lightballs):
            if not lightball.actualizar(dt, 1920, 1080):  # Usar dimensiones del mundo
                lightballs_a_eliminar.append(i)
        
        # Eliminar lightballs fuera de rango o expirados
        for i in reversed(lightballs_a_eliminar):
            self.lightballs.pop(i)
    
    def recibir_daño(self, daño):
        """El jugador recibe daño"""
        self.health -= daño
        if self.health < 0:
            self.health = 0
    
    def curar(self, cantidad):
        """Curar al jugador"""
        self.health = min(self.health + cantidad, self.max_health)
    
    def esta_vivo(self):
        """Verificar si el jugador está vivo"""
        return self.health > 0
