import pygame
import math

class TileMap:
    """Sistema de tiles para crear el piso del juego"""
    
    def __init__(self, world_width, world_height, tile_size=32):
        self.world_width = world_width
        self.world_height = world_height
        self.tile_size = tile_size
        try:
            self.tile_image = pygame.image.load('assets/tile/tile.png')
            self.tile_image = pygame.transform.scale(self.tile_image, (tile_size, tile_size))
        except:
            # Si no existe, crear un tile de relleno
            self.tile_image = pygame.Surface((tile_size, tile_size))
            self.tile_image.fill((100, 100, 100))
        
        self.tiles_x = math.ceil(world_width / tile_size)
        self.tiles_y = math.ceil(world_height / tile_size)
        self.map_surface = pygame.Surface((world_width, world_height))
        self._generar_mapa()
    
    def _generar_mapa(self):
        """Generar el mapa de tiles"""
        for y in range(self.tiles_y):
            for x in range(self.tiles_x):
                tile_x = x * self.tile_size
                tile_y = y * self.tile_size
                self.map_surface.blit(self.tile_image, (tile_x, tile_y))
    
    def dibujar(self, surface, camera_x=0, camera_y=0):
        """Dibujar el mapa en la pantalla (con offset de cámara si es necesario)"""
        surface.blit(self.map_surface, (-camera_x, -camera_y))
    
    def obtener_limites(self):
        """Obtener los límites del mundo"""
        return pygame.Rect(0, 0, self.world_width, self.world_height)
