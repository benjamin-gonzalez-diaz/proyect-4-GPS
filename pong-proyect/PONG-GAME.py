import pygame, sys, random
import math
from components.button import ButtonSetUp, ButtonLaunch
from components.dropdown import DropDown
from components.text import Text
from util.colors import Colors


# ------------------------------------------------ SETUP ------------------------------------------------
pygame.init()

# Dimensions
HEIGHT_SCREEN = 667
WIDTH_SCREEN = 1000

# Screen setup
try:
    background_image = pygame.image.load("fondos\photoinicio.jpg")
    background_rect = background_image.get_rect()
except:
     None
screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
pygame.display.set_caption("configuration")
clock = pygame.time.Clock()



width_obstacle = 10
text_obstacle = Text(width_obstacle, 0, "ball size")
options = ["very_EASY","Easy", "Medium", "Hard", "ultra_Hard"] # easy  grande, medium normal, hard chica
drop_down_obstacle = DropDown(
    width_obstacle, text_obstacle.font_size, 190, 40, options)

width_wind = width_obstacle + drop_down_obstacle.width + 10
text_wind = Text(width_wind, 0, "palette size")
options = ["Easy", "Medium", "Hard", "full"] # easy  grande, medium normal, hard chica
drop_down_wind = DropDown(width_wind, text_wind.font_size, 200, 40, options)


width_obstacle_2 = width_wind + drop_down_wind.width + 10
text_obstacle_2 = Text(width_obstacle_2, 0, "mouse/keyboard guest") # opcion extra
options_2 = ["mouse", "teclado (w,s)"]
drop_down_obstacle_2 = DropDown(width_obstacle_2, text_obstacle_2.font_size, 210, 40, options_2)


end = width_obstacle_2 + drop_down_obstacle_2.width + 190
text_end_matched = Text(end, 0, "end match")
options_3 = ["1", "2", "3","4","5","6","7","8","9","10"]
end_matched = DropDown(end, text_end_matched.font_size, 180, 40, options_3)

button = ButtonSetUp(540, 300, 160, 50, "Continue")
note_izq = ButtonSetUp(230, 550, 570, 40, "teclado|mouse: w|click izq = arriba")
note_der = ButtonSetUp(230, 600, 570, 40, "teclado|mouse:  s|click der = abajo")

setup_options = None

while setup_options is None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        obstacle_selected_option = drop_down_obstacle.handle_event(event)
        wind_selected_option = drop_down_wind.handle_event(event)
        obstacle_2_selected_option = drop_down_obstacle_2.handle_event(event)
        end_matched_option = end_matched.handle_event(event)
        setup_options = button.handle_event(
            event, drop_down_obstacle, drop_down_wind, drop_down_obstacle_2,end_matched)
        if setup_options:
            break
    try:
        screen.blit(background_image, background_rect)
    except:
        screen.fill(Colors.light_salmon)

    text_obstacle.draw(screen)
    drop_down_obstacle.draw(screen)

    text_wind.draw(screen)
    drop_down_wind.draw(screen)

    text_obstacle_2.draw(screen)
    drop_down_obstacle_2.draw(screen)

    text_end_matched.draw(screen)
    end_matched.draw(screen)
    
    button.draw(screen)
    note_izq.draw(screen)
    note_der.draw(screen)

    pygame.display.update()
    clock.tick(60)

pygame.quit()

# ---------------------------------main Game------------------------------------------------------
palets_size = setup_options["palets_size"]
balls_size = setup_options["balls_size"]
count_balls = setup_options["balls"] # opcion extra
end_matchs = setup_options["end"]

def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time, tick
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1

    if ball.left <= 0:
        opponent_score += 1
        score_time = pygame.time.get_ticks()
        reset_ball()

    if ball.right >= screen_width:
        player_score += 1
        score_time = pygame.time.get_ticks()
        reset_ball()

    if ball.colliderect(player) and ball_speed_x > 0:
        ball_speed_x = -ball_speed_x -0.05 
        ball_speed_y = random.choice([1, -1]) * random.uniform(1, 5)
        # Aumenta la velocidad de la bola cada vez que colisiona con la paleta
        if(-ball_speed_x < 25 or palets_size == "full"):
            ball_speed_x *= 1.05
        tick += 1
        print(f"velocidad de la bola jugador:{ball_speed_x}")
        #print(f"total de toques que esta haciendo el jugador {tick}")

    if ball.colliderect(opponent) and ball_speed_x < 0:
        ball_speed_x = -ball_speed_x -0.05
        ball_speed_y = random.choice([1, -1]) * random.uniform(1, 5)
        if(ball_speed_x < 25 or palets_size == "full"):
            ball_speed_x *= 1.05
        print(f"velocidad de la bola opponent:{ball_speed_x}")
        
def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.center = (screen_width / 2, screen_height / 2)
    ball_speed_x = random.choice([1, -1]) * random.uniform(5, 7)
    ball_speed_y = random.choice([1, -1]) * random.uniform(1, 5)
    
def player_animation():
	player.y += player_speed
	if player.top <= 0:
		player.top = 0
	if player.bottom >= screen_height:
		player.bottom = screen_height

def opponent_animation():
    global opponent_speed

    if opponent.top < ball.y:
        opponent.y += opponent_speed
    if opponent.bottom > ball.y:
        opponent.y -= opponent_speed

    # Añade estas condiciones para mantener al oponente dentro de la pantalla
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height



def ball_start():
	global ball_speed_x, ball_speed_y, score_time

	current_time = pygame.time.get_ticks()
	ball.center = (screen_width/2, screen_height/2)

	if current_time - score_time < 700:
		number_three = game_font.render("3", False, white)
		screen.blit(number_three, (screen_width/2 - 10, screen_height/2 + 20))
	if 700 < current_time - score_time < 1400:
		number_number = game_font.render("2", False, white)
		screen.blit(number_number, (screen_width/2 - 10, screen_height/2 + 20))
	if 1400 < current_time - score_time < 2100:
		number_one = game_font.render("2", False, white)
		screen.blit(number_one, (screen_width/2 - 10, screen_height/2 + 20))

	if current_time - score_time < 3100:
		ball_speed_x, ball_speed_y = 0,0
	else:
		if(ball_speed_y >= 1 and ball_speed_x >= 1):
			ball_speed_y += random.randint(0,10)
			ball_speed_x += random.randint(0,10)
		else:
			ball_speed_y = 7 * random.choice((1, -1))
			ball_speed_x = 7 * random.choice((1, -1))
		score_time = None

def winner_player(player):
    pygame.init()

    WIDTH_WINNER_SCREEN = 640
    HEIGHT_WINNER_SCREEN = 640

    # screen to display winner
    try:
        background_image = pygame.image.load("fondos\winner trophy.jpg")
        background_rect = background_image.get_rect()
    except:
         None
    screen = pygame.display.set_mode((WIDTH_WINNER_SCREEN, HEIGHT_WINNER_SCREEN))
    pygame.display.set_caption("Winner")
    clock = pygame.time.Clock()

    padding = 10
    # Las coordenadas no importan aquí porque las ajustaremos después
    text = Text(0, 0, f"Player {player} wins!")

    text_width, text_height = text.text_surface.get_size()
    text.x = (WIDTH_WINNER_SCREEN - text_width) // 2
    text.y = (HEIGHT_WINNER_SCREEN - text_height) // 2


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        try:
            screen.blit(background_image, background_rect)
        except:
            screen.fill(Colors.light_salmon)
        text.draw(screen)

        pygame.display.update()
        clock.tick(60)


# Configuración del juego
pygame.mixer.pre_init()
pygame.init()
clock = pygame.time.Clock()

# Configuración de pantalla
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')
winner = ""

# variables del juego (elegidas en setup)
balls_sized = {
    "very_EASY": random.randint(170,210),
    "Easy": random.randint(100, 170),
    "Medium": random.randint(40, 70),
    "Hard": 20,
    "ultra_Hard": random.randint(5, 19)
}
# pallet_sized = {
#     "full": screen_width,
#     "Easy": random.randint(screen_width/4, screen_width/2),
#     "Medium": random.randint(screen_width/8, screen_width/4-100),
#     "Hard": random.randint(screen_width/10-30, screen_width/8),
# }
pallet_sized = {
    "full": screen_width,
    "Easy": screen_width/4+50,
    "Medium": screen_width/8+25,
    "Hard": screen_width/10-30,
}



# Rectángulos del juego
ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, balls_sized[setup_options["balls_size"]], balls_sized[setup_options["balls_size"]]) # cambio de tamaño de la pelota
#ball2 = pygame.Rect(screen_width/8 - 15, screen_height/2 - 15, balls_sized[setup_options["balls_size"]], balls_sized[setup_options["balls_size"]])
player = pygame.Rect(screen_width - 30, screen_height/2 - 70, 30, pallet_sized[setup_options["palets_size"]]) # cambio de tamaño de la paleta
opponent = pygame.Rect(0, screen_height/2 - 70, 30, pallet_sized[setup_options["palets_size"]])
initial_ball_speed = 7
#color list
blues = [(0, 0, 128), (178, 34, 34),(135, 206, 235),(240, 128, 128) ,(0, 0, 205), (192, 192, 192)]
reds = [(139, 0, 0),(65, 105, 225), (255, 99, 71), (30, 144, 255), (255, 140, 0), (105, 105, 105)]
# Colores
bg_color = Colors.sea_green
ball_color = (255, 255, 255)
ball_color_2 = Colors.silver
line_color = Colors.black
player_color = random.choice(blues)
opponent_color =  random.choice(reds)
white = Colors.brown

# Velocidades iniciales de la pelota
tick = 0
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
opponent_speed = 0

# Temporizador del marcador
score_time = True

# Texto y fuentes
player_score = 0
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf", 32)
current_time = 0
print(count_balls)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7

    ball_animation()
    player_animation()
    opponent_animation()
    #logica de los botones
	# Obtiene el estado de los botones del mouse
    if(count_balls == "mouse"):
        mouse_buttons = pygame.mouse.get_pressed()
        # mouse_buttons[0] representa el botón izquierdo, mouse_buttons[2] representa el botón derecho
        if mouse_buttons[0]:  # Botón izquierdo presionado
            opponent.y -= 7
        if mouse_buttons[2]:  # Botón derecho presionado
            opponent.y += 7
        if mouse_buttons[1]:
            print("pulsando boton")
    # Nueva lógica para controlar al oponente con el teclado
    if(count_balls == "teclado (w,s)"):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            opponent.y += 7
        if keys[pygame.K_w]:
            opponent.y -= 7

    # Game visuals
    screen.fill(bg_color)
    pygame.draw.rect(screen, player_color, player)
    pygame.draw.rect(screen, opponent_color, opponent)
    pygame.draw.ellipse(screen, ball_color, ball)
    #pygame.draw.ellipse(screen, ball_color_2, ball2)
    pygame.draw.aaline(screen, line_color, (screen_width/2,0), (screen_width/2, screen_height))

    if score_time:
        ball_start()
    current_time = round(pygame.time.get_ticks()/1000,1)
    player_text = game_font.render(f"Jugador Der/local: {opponent_score}", False, player_color)
    screen.blit(player_text, (660, 10))

    opponent_text = game_font.render(f"Jugador Izq/guest: {player_score}", False, opponent_color)
    screen.blit(opponent_text, (320, 10))
	
    time_text = game_font.render(f"Time: {current_time} Segundos", False, Colors.gold)
    screen.blit(time_text, (550, 50))

    time_text = game_font.render(f"end match: {end_matchs}", False, Colors.purple)
    screen.blit(time_text, (33, 10))

    pygame.display.flip()
    clock.tick(75)

    if(int(end_matchs) == opponent_score):
        winner = "Der"
        break
    if(int(end_matchs) == player_score):
        winner = "Izq"
        break

pygame.quit()
pygame.init()
winner_player(winner)