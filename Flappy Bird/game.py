from lib2to3.pygram import python_grammar_no_print_statement
from tkinter import CENTER
import pygame, sys, random, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def draw_floor():
    screen.blit(floor_surface,(floor_x_pos,900/2))
    screen.blit(floor_surface,(floor_x_pos+576/2,900/2))
    
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (576/2, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (576/2, random_pipe_pos - 150))
    return bottom_pipe, top_pipe
    
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2.5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024/2:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)
    
def check_collision(pipes):
    for pipe in pipes: 
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -100/2 or bird_rect.bottom >= 900/2:
            return False
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -4*bird_movement, 1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird,new_bird_rect
            
# Init pygame
pygame.init()
screen = pygame.display.set_mode((576/2,1024/2))
clock = pygame.time.Clock()

#General variables
game_active = True
fps = 120
floor_x_pos = 0



# Game variables
gravity = 0.25
bird_movement = 0

bg_surface = pygame.image.load('assets/sprites/background-day.png').convert()
floor_surface = pygame.image.load('assets/sprites/base.png').convert()

bird_downflap = pygame.image.load('assets/sprites/bluebird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0

bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center =(100,1024/2/2))

pipe_surface = pygame.image.load('assets/sprites/pipe-green.png')

pipe_list = []
pipe_height = [200, 300, 400]
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)


## Gameloop
while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 6
                
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100,1024/2/2)
                bird_movement = 0
                
        elif event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
            
        elif event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else: bird_index = 0
            
            bird_surface,bird_rect = bird_animation()
                  
    screen.blit(bg_surface, (0,0))
    
    if game_active:
        # Bird logic
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, (bird_rect))
        game_active = check_collision(pipe_list)
        
        # Pipe
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
    
    # Floor logic
    
    floor_x_pos += -0.5
    draw_floor()
    if floor_x_pos <= -576/2:
        floor_x_pos = 0
    
    pygame.display.update()
    clock.tick(fps) # limits fps