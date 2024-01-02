# Importation des bibliothèques
import pygame
import time
import random
import sys

snake_speed = 15

# Taille de la fenêtre
window_x = 600
window_y = 600

# Définition des couleurs
fond_ecran = pygame.Color(0,0,0) # (0, 100, 200)
score_color = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Initialisation de pygame
pygame.init()

# Initialisation de la fenêtre de jeu
pygame.display.set_caption('GeeksforGeeks Snakes')
game_window = pygame.display.set_mode((window_x, window_y))

# Contrôleur de FPS (images par seconde)
fps = pygame.time.Clock()

# Définition de la position par défaut du serpent
snake_position = [100, 50]

# Définition des 4 premiers blocs du corps du serpent
snake_body = [[100, 50],
			[90, 50],
			[80, 50],
			[70, 50]
			]
# Position du fruit
fruit_position = [random.randrange(1, (window_x//10)) * 10, 
				random.randrange(1, (window_y//10)) * 10]

fruit_spawn = True

# Direction du serpent par défaut vers la droite
direction = 'RIGHT'
change_to = direction

# Score initial
score = 0

# Fonction d'affichage du score
def show_score(choice, color, font, size, snake_speed):

	# Création de l'objet de police score_font
	score_font = pygame.font.SysFont(font, size)
	
	# Création de l'objet de surface d'affichage du score
	score_surface = score_font.render('Score : ' + str(score) + ' vitesse : ' + str(snake_speed) + ' fps', True, color)
	
	# Création d'un objet rectangulaire pour la surface de texte
	score_rect = score_surface.get_rect()
	
	# Affichage du texte
	game_window.blit(score_surface, score_rect)

# Fonction de fin de jeu
def game_over():

	# Création de l'objet de police my_font
	my_font = pygame.font.SysFont('times new roman', 50)
	
	# Création de la surface de texte sur laquelle le texte sera dessiné
	game_over_surface = my_font.render(
		'Votre score est : ' + str(score), True, red)
	
	# Création d'un objet rectangulaire pour la surface de texte
	game_over_rect = game_over_surface.get_rect()
	
	# Positionnement du texte
	game_over_rect.midtop = (window_x/2, window_y/4)
	
	# blit dessinera le texte à l'écran
	game_window.blit(game_over_surface, game_over_rect)
	pygame.display.flip()
	
	# Après 2 secondes, nous quitterons le programme
	time.sleep(2)
	
	# Désactivation de la bibliothèque pygame
	pygame.quit()
	
	# Quitter le programme
	quit()

#creation du fond decran
def drawSquares(win, size = 10):
   colors = [(0, 102, 0), (25, 25, 112)]
   for i in range(0, win.get_width(), size):
       for j in range(0, win.get_height(), size):
           color = colors[(i // size + j // size) % 2]
           pygame.draw.rect(win, color, pygame.Rect(i, j, size, size))

# Fonction principale
while True:
	
	# Gestion des événements clavier
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit ()
			sys.exit ()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				change_to = 'UP'
			if event.key == pygame.K_DOWN:
				change_to = 'DOWN'
			if event.key == pygame.K_LEFT:
				change_to = 'LEFT'
			if event.key == pygame.K_RIGHT:
				change_to = 'RIGHT'

	# Si deux touches sont pressées simultanément
	# nous ne voulons pas que le serpent se déplace dans deux
	# directions simultanément
	if change_to == 'UP' and direction != 'DOWN':
		direction = 'UP'
	if change_to == 'DOWN' and direction != 'UP':
		direction = 'DOWN'
	if change_to == 'LEFT' and direction != 'RIGHT':
		direction = 'LEFT'
	if change_to == 'RIGHT' and direction != 'LEFT':
		direction = 'RIGHT'

	# Déplacement du serpent
	if direction == 'UP':
		snake_position[1] -= 10
	if direction == 'DOWN':
		snake_position[1] += 10
	if direction == 'LEFT':
		snake_position[0] -= 10
	if direction == 'RIGHT':
		snake_position[0] += 10

	# Mécanisme de croissance du corps du serpent
	# si les fruits et les serpents entrent en collision, le score
	# sera incrémenté de 10
	snake_body.insert(0, list(snake_position))
	if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
		score += 10
		fruit_spawn = False
		snake_speed += 1
	else:
		snake_body.pop()
		
	if not fruit_spawn:
		fruit_position = [random.randrange(1, (window_x//10)) * 10, 
						random.randrange(1, (window_y//10)) * 10]
		
	fruit_spawn = True
	game_window.fill(fond_ecran)
	drawSquares (game_window)
	
	for pos in snake_body:
		pygame.draw.rect(game_window, green,
						pygame.Rect(pos[0], pos[1], 10, 10))
	pygame.draw.rect(game_window, red, pygame.Rect(
		fruit_position[0], fruit_position[1], 10, 10))

	# Conditions de fin de jeu
	if snake_position[0] < 0 or snake_position[0] > window_x-10:
		game_over()
	if snake_position[1] < 0 or snake_position[1] > window_y-10:
		game_over()

	# Toucher le corps du serpent
	for block in snake_body[1:]:
		if snake_position[0] == block[0] and snake_position[1] == block[1]:
			game_over()

	# Affichage du score en continu
	show_score(1, score_color, 'times new roman', 20, snake_speed)

	# Actualiser l'écran de jeu
	pygame.display.update()

	# Images par seconde / Taux de rafraîchissement
	fps.tick(snake_speed)
