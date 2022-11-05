import pygame
import os
pygame.font.init()
pygame.mixer.init() #for sounds


#global variables
WIDTH, HEIGHT = 900, 500 #define constant values in caps for convention sake
WIN = pygame.display.set_mode((WIDTH,HEIGHT)) #displays game
pygame.display.set_caption("It a game alright")

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

BORDER = pygame.Rect(WIDTH/2 - 5,0,10,HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade_1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun_Silencer.mp3'))

FPS = 60
VELOCITY = 5
BULLET_VELOCITY = 7
MAX_BULLETS = 3

SPACESHIP_WIDTH,SPACESHIP_HEIGHT = 55,40
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),270)
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','space.png')),(WIDTH,HEIGHT))

YELLOW_HIT = pygame.USEREVENT + 1 #user event + a number to make event unique
RED_HIT = pygame.USEREVENT + 2

HEALTH_FONT = pygame.font.SysFont('comicsans',40)
WINNER_FONT = pygame.font.SysFont('comicsans',100)

def draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health):
    WIN.blit(SPACE,(0,0))
    #WIN.fill(WHITE) #fills color of window, RGB, PUT THIS FIRST ORDER MATTERS CAN DRAW OVER TOP
    pygame.draw.rect(WIN,BLACK,BORDER)
    red_health_text = HEALTH_FONT.render("Health: "+ str(red_health),1,WHITE) #1 is for anti aliasing
    yellow_health_text = HEALTH_FONT.render("Health: "+ str(yellow_health),1,WHITE) #1 is for anti aliasing
    WIN.blit(red_health_text,(WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text,(10,10))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x,yellow.y)) #draws a surface onto screen, images known as surfaces in pygame
    WIN.blit(RED_SPACESHIP, (red.x,red.y))
    
    for bullet in red_bullets:
        pygame.draw.rect(WIN,RED,bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN,YELLOW,bullet)
        
    pygame.display.update() #necessary to update display

def yellow_handle_movement(keys_pressed,yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VELOCITY > 5: #left
        yellow.x -= VELOCITY
    if keys_pressed[pygame.K_d]and yellow.x + VELOCITY + SPACESHIP_WIDTH - 25 < BORDER.x: #right
        yellow.x += VELOCITY
    if keys_pressed[pygame.K_w] and yellow.y - VELOCITY > 0: #up
        yellow.y -= VELOCITY
    if keys_pressed[pygame.K_s]and yellow.y + VELOCITY + SPACESHIP_HEIGHT < HEIGHT - 14: #down
        yellow.y += VELOCITY    

def red_handle_movement(keys_pressed,red):
    if keys_pressed[pygame.K_LEFT] and red.x + VELOCITY > BORDER.x + BORDER.width:
        red.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT]and red.x + VELOCITY + SPACESHIP_WIDTH < WIDTH:
        red.x += VELOCITY
    if keys_pressed[pygame.K_UP] and red.y - VELOCITY > 0:
        red.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN]and red.y + VELOCITY + SPACESHIP_HEIGHT < HEIGHT-14:
        red.y += VELOCITY    

def handle_bullets(yellow_bullets,red_bullets,yellow,red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY
        if red.colliderect(bullet): #checks if yellow bullet collided with red, boolean
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)  
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)             
    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY
        if yellow.colliderect(bullet): #checks if yellow bullet collided with red, boolean
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet) 
        elif bullet.x <0:
            red_bullets.remove(bullet) 
            
def draw_winner(text):
    draw_text = WINNER_FONT.render(text,1,WHITE)
    WIN.blit(draw_text,(WIDTH//2 - draw_text.get_width()//2,HEIGHT//2 - draw_text.get_height()//2))  
    pygame.display.update()   
    pygame.time.delay(5000) # pause for 5 seconds
    
def main():
    red = pygame.Rect(700,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT) #rectangles to represent spaceships
    yellow = pygame.Rect(100,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    red_bullets = []
    yellow_bullets = []
    red_health = 10
    yellow_health = 10
    clock = pygame.time.Clock()
    run = True
    while run: #while run is true game will run
        clock.tick(FPS) # controls speed of while loop, up to 60 times per second in this case
        for event in pygame.event.get(): # check for events happening in the game
            if event.type == pygame.QUIT: #if user closes window
               run = False
               pygame.quit()
            if event.type == pygame.KEYDOWN: #handled differently than movement so shooting is methodical
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width,yellow.y + yellow.height//2 - 2,10,5) #x,y,width,height
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x,red.y + red.height//2 - 2,10,5) #x,y,width,height DOUBLE SLASH FOR INT DIVISION
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.PLAY()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.PLAY()
        winner_text = ""        
        if red_health <= 0:
            winner_text = "Yellow wins!"
        if yellow_health <=0:
            winner_text = "Red wins!" 
        if winner_text != "":
            draw_winner(winner_text)
            break   
        keys_pressed = pygame.key.get_pressed() # tells us what keys are currently being pressed
        yellow_handle_movement(keys_pressed,yellow)
        red_handle_movement(keys_pressed,red)
        handle_bullets(yellow_bullets,red_bullets,yellow,red)
        draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health) #function for display design
    main()
    
if __name__ == "__main__": #only runs main function if we run this file directly
    main()