import pygame
import random

pygame.init() # Inicializamos pygame

size = 350, 650
ventana = pygame.display.set_mode(size)
pygame.display.set_caption("Ball")
clock = pygame.time.Clock()
FPS = 60

# Definir la clase player
class Player():
    def __init__(self, x, y):
        self.image = pygame.image.load("ball.png")
        self.image = pygame.transform.scale(self.image, (35, 35))
        self.x = x
        self.y = y
        self.dx = 0.2
    
    # Damos movimiento a ball, y evitamos que salga de la pantalla
    def move(self):
        keys = pygame.key.get_pressed() # Obtiene el estado de la tecla
        if keys[pygame.K_LEFT]: # Verifica de la tecla izquierda esta presionada
            self.x -= self.dx
        if keys[pygame.K_RIGHT]: # Verifica de la tecla derecha esta presionada
            self.x += self.dx

        if self.x < 0: # Vefifica que ball no sobrepase la pantalla izquierda
            self.x = 0
        if self.x > size[0] - self.image.get_width(): # Vefifica que ball no sobrepase la pantalla derecha
            self.x = size[0] - self.image.get_width()

# Definimos la clase rectangulo
class Rectangle():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vy = 0.4
        
    # Dibuja el rectangulo en la pantalla
    def draw(self, ventana):
        pygame.draw.rect(ventana, (230, 138, 230), pygame.Rect(self.x, self.y, self.width, self.height)) # Dibuja los rectangulos
   
    # Actualiza la posicion del rectangulo
    def update(self):
        self.y += self.vy # Mueve el rectangulo hacia abajo
        if self.y > size[1]: # Verifica si el rectangulo ha salido de la pantalla
            self.y = -self.height # Reinicia la posicion 
            gap_position = random.randint(gap, size[0] - gap) # Gernera una posicion aleatoria para la brecha de los rectangulos
            self.x = 0
            self.width = gap_position # Establece el ancho del rectangulo
            return True # Indica que el rectangulo ha salido de la pantalla y ha sido reiniciado
        return False # Si el rectangulo no ha salido de la pantalla

# Fondo del juego
background = pygame.image.load('background_space.jpg')

# Posicion de la bola
ball = Player(183, 500)

# Establecemos variables para los rectangulos
gap = 60 
rect_height = 50
gap_position = random.randint(gap, size[0] - gap) # Posicion aleatoria para el hueco entre los dos rectangulos
rect1 = Rectangle(0, 0, gap_position, rect_height)
rect2 = Rectangle(gap_position + gap, 0, size[0] - (gap_position + gap), rect_height)

# Verifica las colisiones
def check_collision(player, rect):
    player_rect = pygame.Rect(player.x, player.y, player.image.get_width(), player.image.get_height())
    rect_rect = pygame.Rect(rect.x, rect.y, rect.width, rect.height)
    return player_rect.colliderect(rect_rect)

# Definimos variables de score
score = 0
font = pygame.font.Font(None, 36)

# Muestra la pantalla game over
def game_over_screen():
    ventana.fill((0, 0, 0))
    game_over_text = font.render("Game Over", 1, (255, 255, 255))
    restart_text = font.render("Presiona R para reiniciar", 1, (255, 255, 255))
    score_over_text = font.render("Tu score: " + str(score), 1, (255, 255, 255))
    ventana.blit(game_over_text, (size[0] // 2 - game_over_text.get_width() // 2, size[1] // 2 - game_over_text.get_height() // 2))
    ventana.blit(restart_text, (size[0] // 2 - restart_text.get_width() // 2, size[1] // 2 + game_over_text.get_height()))
    ventana.blit(score_over_text, (size[0] // 2 - game_over_text.get_width() // 2, size[1] // 2 + restart_text.get_height() * 2.5))
    pygame.display.flip()

running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            ball = Player(183, 500)
            gap_position = random.randint(gap, size[0] - gap)
            rect1 = Rectangle(0, 0, gap_position, rect_height)
            rect2 = Rectangle(gap_position + gap, 0, size[0] - (gap_position + gap), rect_height)
            score = 0
            game_over = False

    if not game_over:
        ventana.blit(background, (0, 0))
        ventana.blit(ball.image, (ball.x, ball.y))
        rect1.draw(ventana)
        rect2.draw(ventana)
        ball.move()

        if rect1.update():
            gap_position = random.randint(gap, size[0] - gap)
            rect1 = Rectangle(0, 0, gap_position, rect_height)
            rect2 = Rectangle(gap_position + gap, 0, size[0] - (gap_position + gap), rect_height)
            score += 1

        if rect2.update():
            gap_position = random.randint(gap, size[0] - gap)
            rect1 = Rectangle(0, 0, gap_position, rect_height)
            rect2 = Rectangle(gap_position + gap, 0, size[0] - (gap_position + gap), rect_height)
            score += 1

        rect2.x = gap_position + gap

        if check_collision(ball, rect1) or check_collision(ball, rect2):
            game_over = True

        score_text = font.render("Score: " + str(score), 1, (255, 255, 255))
        ventana.blit(score_text, (10, 10))
        pygame.display.flip()
    else:
        game_over_screen()

pygame.quit()
