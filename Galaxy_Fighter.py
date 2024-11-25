import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIN_WIDTH = 900
WIN_HEIGHT  = 500

WIN = pygame.display.set_mode((WIN_WIDTH,  WIN_HEIGHT))

pygame.display.set_caption("Galaxy Fighter")

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIN_WIDTH//2 - 5, 0, 10, WIN_HEIGHT)

HEALTH_TEXT = pygame.font.SysFont("comicsans", 40)
WIN_TEXT = pygame.font.SysFont("comicsans", 50)

HIT_SOUND = pygame.mixer.Sound(os.path.join("./Resources", "Galaxy_Fighter", "hit_sound.mp3"))
FIRE_SOUND = pygame.mixer.Sound(os.path.join("./Resources", "Galaxy_Fighter", "fire_sound.mp3"))
MOVEMENT_SOUND = pygame.mixer.Sound(os.path.join("./Resources", "Galaxy_Fighter", "movement_sound.mp3"))
CELEBRATION_SOUND = pygame.mixer.Sound(os.path.join("./Resources", "Galaxy_Fighter", "celebration_sound.mp3"))

BULLET_VEL = 7

MAX_BULLTES = 3

SPACE1_HIT = pygame.USEREVENT + 1
SPACE2_HIT = pygame.USEREVENT + 2

FPS = 60

VEL = 5

#defining the space-ships
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 100, 100
spaceship_1 = pygame.image.load("./Resources/Galaxy_Fighter/spaceship_1.png")
spaceship_1 = pygame.transform.rotate(pygame.transform.scale(spaceship_1, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 360)

spaceship_2 = pygame.image.load(os.path.join("Resources",  "Galaxy_Fighter", "spaceship_2.png")) 
spaceship_2 = pygame.transform.rotate(pygame.transform.scale(spaceship_2, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 360)

space = pygame.transform.scale(pygame.image.load(os.path.join("Resources", "Galaxy_Fighter", "space.jpg")),(WIN_WIDTH, WIN_HEIGHT))

def draw_window(space_1, space_2, space1_bullets, space2_bullets, space1_health, space2_health):
    # WIN.fill(WHITE)
    WIN.blit(space, (0,0))

    pygame.draw.rect(WIN, BLACK, BORDER)

    space1_health_text = HEALTH_TEXT.render("Health: " +str(space1_health), 1, WHITE)
    space2_health_text = HEALTH_TEXT.render("Health: " +str(space2_health), 1, WHITE)

    WIN.blit(space1_health_text, (WIN_WIDTH  - space1_health_text.get_width() - 10, 10))
    WIN.blit(space2_health_text, (10, 10))

    WIN.blit(spaceship_1, (space_1.x, space_1.y))
    WIN.blit(spaceship_2, (space_2.x, space_2.y))



    for bullet in space1_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in space2_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    

    pygame.display.update()


def spaceship1_movement(keys_pressed, space_1):
    if  keys_pressed[pygame.K_a] and space_1.x - VEL > -26: #for left key
        space_1.x -= VEL
        MOVEMENT_SOUND.play()
    if  keys_pressed[pygame.K_d] and space_1.x + VEL + space_1.width - 25 < BORDER.x: #for right key
        space_1.x += VEL
        MOVEMENT_SOUND.play()
    if  keys_pressed[pygame.K_w] and space_1.y - VEL > -35: #for up key
        space_1.y -= VEL 
        MOVEMENT_SOUND.play()
    if  keys_pressed[pygame.K_s] and space_1.y + VEL  + space_1.height - 38 < WIN_HEIGHT: #for down key
        space_1.y += VEL
        MOVEMENT_SOUND.play()


def spaceship2_movement(keys_pressed, space_2):
    if  keys_pressed[pygame.K_LEFT] and space_2.x - VEL + 10 > BORDER.x: #for left key
        space_2.x -= VEL 
        MOVEMENT_SOUND.play()
    if  keys_pressed[pygame.K_RIGHT] and space_2.x + VEL + space_2.width - 20 < WIN_WIDTH: #for right key
        space_2.x += VEL 
        MOVEMENT_SOUND.play()
    if  keys_pressed[pygame.K_UP] and space_2.y - VEL > -12: #for up key
        space_2.y -= VEL 
        MOVEMENT_SOUND.play()
    if  keys_pressed[pygame.K_DOWN] and space_2.y + VEL  + space_2.height - 12 < WIN_HEIGHT: #for down key
        space_2.y += VEL
        MOVEMENT_SOUND.play()
    

def handle_bullets(space1_bulltes, space2_bulltes, space_1, space_2):
    for bullet in space1_bulltes:
        bullet.x += BULLET_VEL
        if space_2.colliderect(bullet):
            pygame.event.post(pygame.event.Event(SPACE2_HIT))
            space1_bulltes.remove(bullet)
        elif bullet.x > WIN_WIDTH:
            space1_bulltes.remove(bullet)


    for bullet in space2_bulltes:
        bullet.x -= BULLET_VEL
        if space_1.colliderect(bullet):
            pygame.event.post(pygame.event.Event(SPACE1_HIT))
            space2_bulltes.remove(bullet)
        elif bullet.x < 0:
            space2_bulltes.remove(bullet)

def draw_msg(win_msg):
    msg = WIN_TEXT.render(win_msg, 1, WHITE)
    WIN.blit(msg, (WIN_WIDTH/2 -msg.get_width()/2, WIN_HEIGHT/2 - msg.get_height()/2))
    pygame.display.update()
    CELEBRATION_SOUND.play()
    pygame.time.delay(5000)

def main():

    space_1 = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    space_2 = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    clock = pygame.time.Clock()

    space1_bulltes = []
    space2_bulltes = []

    space1_health = 10
    space2_health = 10

    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LALT and len(space1_bulltes) < MAX_BULLTES:
                    bullet = pygame.Rect(space_1.x + space_1.width, space_1.y + space_1.height//2 - 2, 10, 5)
                    space1_bulltes.append(bullet)
                    FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(space2_bulltes) < MAX_BULLTES:
                    bullet = pygame.Rect(space_2.x, space_2.y + space_2.height//2 - 2, 10, 5)
                    space2_bulltes.append(bullet)
                    FIRE_SOUND.play()

            if event.type == SPACE1_HIT:
                space2_health -= 1
                HIT_SOUND.play()
            if event.type == SPACE2_HIT:
                space1_health -= 1
                HIT_SOUND.play()
        
        win_msg = ""
        if space1_health <= 0:
            win_msg = "Spaceships 1 WIN !!"
        if space2_health <= 0:
            win_msg = "Spaceships 2 WIN !!"
        if win_msg != "":
            draw_msg(win_msg) #one of the player won
            break


        keys_pressed = pygame.key.get_pressed()
        spaceship1_movement(keys_pressed, space_1) 
        spaceship2_movement(keys_pressed, space_2) 

        handle_bullets(space1_bulltes, space2_bulltes, space_1, space_2)

        draw_window(space_1, space_2,  space1_bulltes, space2_bulltes, space1_health, space2_health)

    main()
    # pygame.quit()

if  __name__ == "__main__":
    main()