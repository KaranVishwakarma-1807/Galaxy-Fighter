#Importing all the required modules
import pygame  #for games 
import os #for file operations
pygame.font.init() #for font rendering
pygame.mixer.init() #for sound effects

#Initializing the window's dimensions
WIN_WIDTH = 900
WIN_HEIGHT  = 500
#creating a window
WIN = pygame.display.set_mode((WIN_WIDTH,  WIN_HEIGHT))
#adding the caption
pygame.display.set_caption("Galaxy Fighter")

#defining colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255, 255, 0)

#making a making in the middle of the board
BORDER = pygame.Rect(WIN_WIDTH//2 - 5, 0, 10, WIN_HEIGHT)

#defining the text
HEALTH_TEXT = pygame.font.SysFont("comicsans", 40)
WIN_TEXT = pygame.font.SysFont("comicsans", 50)

#loading the sounds
HIT_SOUND = pygame.mixer.Sound(os.path.join("./Resources", "hit_sound.mp3"))
FIRE_SOUND = pygame.mixer.Sound(os.path.join("./Resources", "fire_sound.mp3"))
MOVEMENT_SOUND = pygame.mixer.Sound(os.path.join("./Resources", "movement_sound.mp3"))
CELEBRATION_SOUND = pygame.mixer.Sound(os.path.join("./Resources", "celebration_sound.mp3"))

#velocity of the bullets
BULLET_VEL = 7

#maximun number of the bullets
MAX_BULLTES = 3

#to keep track of the bullets by defining the event of ship getting hit by the bullet
SPACE1_HIT = pygame.USEREVENT + 1
SPACE2_HIT = pygame.USEREVENT + 2

#frame per seconds
FPS = 60

#velocity of the ship
VEL = 5

#defining the space-ships
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 100, 100   #dimensions for the ship
spaceship_1 = pygame.image.load("./Resources/spaceship_1.png") #loading the image of the spaceship1
spaceship_1 = pygame.transform.rotate(pygame.transform.scale(spaceship_1, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 360) #to rotate the image

spaceship_2 = pygame.image.load(os.path.join("./Resources", "spaceship_2.png")) #loading the image of the spaceship2
spaceship_2 = pygame.transform.rotate(pygame.transform.scale(spaceship_2, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 360) #to rotate the image
#scaling the backgroud image
space = pygame.transform.scale(pygame.image.load(os.path.join("./Resources", "space.jpg")),(WIN_WIDTH, WIN_HEIGHT))

#defining a function to draw all the images and texts on the window
def draw_window(space_1, space_2, space1_bullets, space2_bullets, space1_health, space2_health):
    # WIN.fill(WHITE)
    WIN.blit(space, (0,0)) #to draw the background

    pygame.draw.rect(WIN, BLACK, BORDER) #to draw the border

    space1_health_text = HEALTH_TEXT.render("Health: " +str(space1_health), 1, WHITE) #to render the text of the health of the spaceship1
    space2_health_text = HEALTH_TEXT.render("Health: " +str(space2_health), 1, WHITE) #to render the text of the health of the spaceship2

    WIN.blit(space1_health_text, (WIN_WIDTH  - space1_health_text.get_width() - 10, 10)) #to draw the health of spaceship1
    WIN.blit(space2_health_text, (10, 10)) #to draw the health of spaceship2

    WIN.blit(spaceship_1, (space_1.x, space_1.y)) #to draw the spaceship1
    WIN.blit(spaceship_2, (space_2.x, space_2.y)) #to draw the spaceship2

    #to draw bullets on the window
    for bullet in space1_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in space2_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()  #to update the window


#defining a function for the movement for the spaceship1
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

#defining a function for the movement for the spaceship2
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
    
#function to handle bullets and there collision with the spaceship2 and spaceship1
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

#function to draw win message in the screen
def draw_msg(win_msg):
    msg = WIN_TEXT.render(win_msg, 1, WHITE)
    WIN.blit(msg, (WIN_WIDTH/2 -msg.get_width()/2, WIN_HEIGHT/2 - msg.get_height()/2))
    pygame.display.update()
    CELEBRATION_SOUND.play()
    pygame.time.delay(5000)


#creating the main function
def main():
    #definig rectangle for the spaceship1 and spaceship2
    space_1 = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    space_2 = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    
    #creating clock to regulate the frame rate
    clock = pygame.time.Clock()
    
    #definig list to store the bullets of spaceship1 and spaceship2
    space1_bulltes = []
    space2_bulltes = []

    #health for both spaceship1 and spaceship2
    space1_health = 10
    space2_health = 10

    
    run = True
    #man event loop
    while run:
        #to regulating the frames
        clock.tick(FPS)
        #handling the events
        for event in pygame.event.get(): #returns a list of all the events
            if event.type == pygame.QUIT: #if user closes the window
                run = False
                pygame.quit() #closes the window
            
            #for bullet firing
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LALT and len(space1_bulltes) < MAX_BULLTES: #condition to fire a bullet
                    bullet = pygame.Rect(space_1.x + space_1.width, space_1.y + space_1.height//2 - 2, 10, 5)
                    space1_bulltes.append(bullet)
                    FIRE_SOUND.play() #play the sound of firing
                if event.key == pygame.K_RCTRL and len(space2_bulltes) < MAX_BULLTES: #condition to fire a bullet
                    bullet = pygame.Rect(space_2.x, space_2.y + space_2.height//2 - 2, 10, 5)
                    space2_bulltes.append(bullet)
                    FIRE_SOUND.play() #play the sound of firing
            #when bullet hits a ship
            if event.type == SPACE1_HIT:
                space2_health -= 1
                HIT_SOUND.play()
            if event.type == SPACE2_HIT:
                space1_health -= 1
                HIT_SOUND.play()
        
        #to draw the msg
        win_msg = ""
        if space1_health <= 0:
            win_msg = "Spaceships 1 WIN !!"
        if space2_health <= 0:
            win_msg = "Spaceships 2 WIN !!"
        if win_msg != "":
            draw_msg(win_msg) #one of the player won
            break

        #calling the movement function
        keys_pressed = pygame.key.get_pressed()
        spaceship1_movement(keys_pressed, space_1) 
        spaceship2_movement(keys_pressed, space_2) 
        handle_bullets(space1_bulltes, space2_bulltes, space_1, space_2)
        draw_window(space_1, space_2,  space1_bulltes, space2_bulltes, space1_health, space2_health)

    main()
    

if  __name__ == "__main__": #to run the main function when the script is running 
    main()
