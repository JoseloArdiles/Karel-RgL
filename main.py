#Karel RogueLike - Supervivencia por Tiempo

import pygame
import random
from settings import WIDTH, HEIGHT, FPS, COLOR_BACKGROUND, ENEMY_SPAWN_RATE, WORLD_WIDTH, WORLD_HEIGHT, TILE_SIZE
from player import Player
from enemy import Enemy
from collision import CollisionSystem
from ui import UIManager
from tilemap import TileMap

pygame.init()

# Configuración del juego
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Karel RogueLike - Supervivencia')
clock = pygame.time.Clock()

# Crear el sistema de tiles
tilemap = TileMap(WORLD_WIDTH, WORLD_HEIGHT, TILE_SIZE)

# Variables del juego
karel = Player(WORLD_WIDTH // 2, WORLD_HEIGHT // 2)
enemigos = []
ui = UIManager(WIDTH, HEIGHT)

# Controles
enemy_spawn_timer = 0
juego_activo = True
enemigo_ataque_cooldown = {}  # Cooldown para ataques de enemigos

def reiniciar_juego():
    """Reiniciar el juego"""
    global karel, enemigos, ui, enemy_spawn_timer, juego_activo, enemigo_ataque_cooldown
    
    karel = Player(WORLD_WIDTH // 2, WORLD_HEIGHT // 2)
    enemigos = []
    ui.reiniciar()
    enemy_spawn_timer = 0
    juego_activo = True
    enemigo_ataque_cooldown = {}

def handle_player_attack(player, enemigos):
    """Manejar ataque del jugador"""
    if player.atacar():
        # Detectar enemigos golpeados
        hit_indices = CollisionSystem.check_attack_hit(
            player.rect, 
            player.attack_range, 
            [e.rect for e in enemigos]
        )
        
        # Aplicar daño a enemigos golpeados
        for i in hit_indices:
            enemigos[i].recibir_daño(player.attack_damage)

def actualizar_lightballs(player, enemigos):
    """Actualizar colisiones de lightballs con enemigos"""
    lightballs_a_eliminar = []
    
    for i, lightball in enumerate(player.lightballs):
        golpeado = False
        for j, enemigo in enumerate(enemigos):
            if lightball.colisiona_con_enemigo(enemigo.rect):
                # El lightball golpea al enemigo
                enemigo.recibir_daño(lightball.damage)
                # Curar al jugador con 1/4 del daño hecho
                player.curar(lightball.damage // 4)
                golpeado = True
                lightballs_a_eliminar.append(i)
                break
        
        if not golpeado:
            # El lightball sigue en movimiento
            pass
    
    # Eliminar lightballs que golpearon enemigos
    for i in reversed(lightballs_a_eliminar):
        if i < len(player.lightballs):
            player.lightballs.pop(i)

def actualizar_enemigos(enemigos, player, dt):
    """Actualizar todos los enemigos"""
    enemigos_a_eliminar = []
    
    for i, enemigo in enumerate(enemigos):
        # Actualizar comportamiento del enemigo
        enemigo.actualizar(player.rect, dt, WIDTH, HEIGHT)
        
        # Detectar colisión con el jugador
        if player.rect.colliderect(enemigo.rect):
            # El enemigo intenta atacar
            if enemigo.puede_atacar():
                daño = enemigo.atacar()
                player.recibir_daño(daño)
        
        # Eliminar enemigos muertos
        if not enemigo.esta_vivo():
            enemigos_a_eliminar.append(i)
            ui.enemigos_derrotados += 1
    
    # Eliminar en orden inverso para no afectar índices
    for i in reversed(enemigos_a_eliminar):
        enemigos.pop(i)

def generar_enemigos(dt):
    """Generar nuevos enemigos"""
    global enemy_spawn_timer
    
    enemy_spawn_timer += dt
    
    # Generar enemigos basado en la tasa de spawn
    if enemy_spawn_timer >= (1.0 / ENEMY_SPAWN_RATE):
        # Número de enemigos aumenta con el tiempo
        num_enemigos = min(1 + (int(ui.tiempo_transcurrido // 30)), 5)
        
        for _ in range(num_enemigos):
            # Generar en posición aleatoria en los bordes del mundo
            lado = random.choice(['arriba', 'abajo', 'izquierda', 'derecha'])
            
            if lado == 'arriba':
                x = random.randint(0, WORLD_WIDTH)
                y = -20
            elif lado == 'abajo':
                x = random.randint(0, WORLD_WIDTH)
                y = WORLD_HEIGHT + 20
            elif lado == 'izquierda':
                x = -20
                y = random.randint(0, WORLD_HEIGHT)
            else:  # derecha
                x = WORLD_WIDTH + 20
                y = random.randint(0, WORLD_HEIGHT)
            
            enemigos.append(Enemy(x, y))
        
        enemy_spawn_timer = 0

# Loop principal del juego
runing = True

while runing:
    dt = clock.tick(FPS) / 1000  # Delta time en segundos
    
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                runing = False
            elif event.key == pygame.K_r and not juego_activo:
                reiniciar_juego()
            elif event.key == pygame.K_SPACE and juego_activo:
                handle_player_attack(karel, enemigos)
    
    if juego_activo:
        # Obtener entrada del teclado
        keys = pygame.key.get_pressed()
        moved = False
        
        if keys[pygame.K_w]:
            karel.move_up()
            moved = True
        if keys[pygame.K_s]:
            karel.move_down()
            moved = True
        if keys[pygame.K_a]:
            karel.move_left()
            moved = True
        if keys[pygame.K_d]:
            karel.move_right()
            moved = True
        
        if not moved:
            karel.is_moving = False
            karel._update_animation()
        
        # Mantener jugador dentro del mundo confinado
        CollisionSystem.check_screen_bounds(karel.rect, WORLD_WIDTH, WORLD_HEIGHT)
        
        # Actualizar jugador
        karel.actualizar(dt)
        
        # Auto-ataque al enemigo más cercano con lightballs
        karel.auto_atacar_enemigo_cercano(enemigos)
        
        # Actualizar colisiones de lightballs
        actualizar_lightballs(karel, enemigos)
        
        # Generar enemigos
        generar_enemigos(dt)
        
        # Actualizar enemigos
        actualizar_enemigos(enemigos, karel, dt)
        
        # Actualizar UI
        ui.actualizar(dt)
        
        # Verificar si el jugador está muerto
        if not karel.esta_vivo():
            juego_activo = False
    
    # Dibujar
    screen.fill(COLOR_BACKGROUND)
    
    # Dibujar tilemap (piso)
    tilemap.dibujar(screen)
    
    # Dibujar jugador
    karel.dibujar(screen)
    
    # Dibujar enemigos
    for enemigo in enemigos:
        enemigo.dibujar(screen)
    
    # Dibujar UI
    ui.dibujar(screen, karel, len(enemigos))
    
    # Dibujar pantalla de muerte si es necesario
    if not juego_activo:
        ui.dibujar_pantalla_muerte(screen)
    
    pygame.display.flip()

pygame.quit()