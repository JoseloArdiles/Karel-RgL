import pygame
import math

class CollisionSystem:
    """Sistema de colisiones y detección de hits"""
    
    @staticmethod
    def check_attack_hit(attack_rect, attack_range, enemy_rects):
        """Detectar enemigos golpeados por un ataque
        
        Args:
            attack_rect: Rectángulo del atacante
            attack_range: Radio del ataque
            enemy_rects: Lista de rectángulos de enemigos
            
        Returns:
            Lista de índices de enemigos golpeados
        """
        hit_enemies = []
        
        for i, enemy_rect in enumerate(enemy_rects):
            distance = math.sqrt(
                (attack_rect.centerx - enemy_rect.centerx)**2 + 
                (attack_rect.centery - enemy_rect.centery)**2
            )
            
            if distance <= attack_range:
                hit_enemies.append(i)
        
        return hit_enemies
    
    @staticmethod
    def check_enemy_collision(player_rect, enemy_rects):
        """Detectar colisión entre jugador y enemigos
        
        Args:
            player_rect: Rectángulo del jugador
            enemy_rects: Lista de rectángulos de enemigos
            
        Returns:
            Lista de índices de enemigos en colisión
        """
        colliding_enemies = []
        
        for i, enemy_rect in enumerate(enemy_rects):
            if player_rect.colliderect(enemy_rect):
                colliding_enemies.append(i)
        
        return colliding_enemies
    
    @staticmethod
    def check_screen_bounds(rect, width, height):
        """Mantener un rectángulo dentro de los límites de la pantalla"""
        if rect.left < 0:
            rect.left = 0
        if rect.right > width:
            rect.right = width
        if rect.top < 0:
            rect.top = 0
        if rect.bottom > height:
            rect.bottom = height
