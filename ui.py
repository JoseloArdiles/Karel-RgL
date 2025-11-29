import pygame

class UIManager:
    """Gestor de la interfaz de usuario"""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        self.tiempo_transcurrido = 0
        self.enemigos_derrotados = 0
        
    def actualizar(self, dt):
        """Actualizar el tiempo transcurrido"""
        self.tiempo_transcurrido += dt
    
    def dibujar(self, surface, player, enemigos_vivos):
        """Dibujar la interfaz de usuario"""
        # Barra de vida del jugador
        self._dibujar_barra_vida(surface, player)
        
        # Información de estadísticas
        self._dibujar_stats(surface, player, enemigos_vivos)
    
    def _dibujar_barra_vida(self, surface, player):
        """Dibujar barra de vida del jugador"""
        # Fondo de la barra
        barra_width = 300
        barra_height = 30
        barra_x = 20
        barra_y = 20
        
        pygame.draw.rect(surface, (100, 100, 100), 
                        (barra_x, barra_y, barra_width, barra_height))
        
        # Barra de vida
        vida_width = (player.health / player.max_health) * barra_width
        pygame.draw.rect(surface, (0, 255, 0), 
                        (barra_x, barra_y, vida_width, barra_height))
        
        # Borde
        pygame.draw.rect(surface, (255, 255, 255), 
                        (barra_x, barra_y, barra_width, barra_height), 2)
        
        # Texto de vida
        texto = self.font_small.render(f"Vida: {int(player.health)}/{int(player.max_health)}", 
                                       True, (255, 255, 255))
        surface.blit(texto, (barra_x + 10, barra_y + 5))
    
    def _dibujar_stats(self, surface, player, enemigos_vivos):
        """Dibujar estadísticas del juego"""
        # Tiempo
        minutos = int(self.tiempo_transcurrido // 60)
        segundos = int(self.tiempo_transcurrido % 60)
        texto_tiempo = self.font_medium.render(f"Tiempo: {minutos}:{segundos:02d}", 
                                               True, (255, 255, 255))
        surface.blit(texto_tiempo, (self.width - 300, 20))
        
        # Enemigos vivos
        texto_enemigos = self.font_medium.render(f"Enemigos: {enemigos_vivos}", 
                                                 True, (255, 100, 100))
        surface.blit(texto_enemigos, (self.width - 300, 60))
        
        # Enemigos derrotados
        texto_derrotados = self.font_small.render(f"Derrotados: {self.enemigos_derrotados}", 
                                                  True, (100, 255, 100))
        surface.blit(texto_derrotados, (self.width - 300, 100))
    
    def dibujar_pantalla_muerte(self, surface):
        """Dibujar pantalla de muerte"""
        # Fondo oscuro
        fondo = pygame.Surface((self.width, self.height))
        fondo.set_alpha(200)
        fondo.fill((0, 0, 0))
        surface.blit(fondo, (0, 0))
        
        # Texto
        texto_muerte = self.font_large.render("¡GAME OVER!", True, (255, 0, 0))
        texto_tiempo = self.font_medium.render(
            f"Tiempo sobrevivido: {int(self.tiempo_transcurrido//60)}:{int(self.tiempo_transcurrido%60):02d}", 
            True, (255, 255, 255)
        )
        texto_derrotados = self.font_medium.render(
            f"Enemigos derrotados: {self.enemigos_derrotados}", 
            True, (100, 255, 100)
        )
        texto_reinicio = self.font_small.render("Presiona R para reiniciar o ESC para salir", 
                                               True, (200, 200, 200))
        
        # Posicionar textos
        superficie_muerte = pygame.Surface(
            (texto_muerte.get_width() + 40, texto_muerte.get_height() * 4 + 80)
        )
        superficie_muerte.fill((50, 50, 50))
        pygame.draw.rect(superficie_muerte, (255, 255, 255), 
                        (0, 0, superficie_muerte.get_width(), superficie_muerte.get_height()), 3)
        
        superficie_muerte.blit(texto_muerte, (20, 20))
        superficie_muerte.blit(texto_tiempo, (20, 80))
        superficie_muerte.blit(texto_derrotados, (20, 130))
        superficie_muerte.blit(texto_reinicio, (20, 180))
        
        # Centrar en pantalla
        x = (self.width - superficie_muerte.get_width()) // 2
        y = (self.height - superficie_muerte.get_height()) // 2
        surface.blit(superficie_muerte, (x, y))
    
    def reiniciar(self):
        """Reiniciar estadísticas"""
        self.tiempo_transcurrido = 0
        self.enemigos_derrotados = 0
