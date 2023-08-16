import random # for generating random numbers
import sys  # to exit the program
import pygame
from pygame.locals import *  # pygame impoprt

# Global Variables for the game
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
GROUNDY = SCREENHEIGHT *0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER ='gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe.png'

def WelcomeScreen():
    """ show welcome image on the screen  
    """
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0

    while True:
        for event in pygame.event.get():
            # if user click on cross button close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If the user presses space or up key, start the game for them
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
                SCREEN.blit(GAME_SPRITES['message'], (messagex,messagey ))    
                SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0

    # creating pipes
    pipe1 = getRandomPipe()
    pipe2 = getRandomPipe()

    # list of upper pipe
    upperPipes = [
        {'x':SCREENWIDTH+200, 'y':pipe1[0]['y']},
        {'x' : SCREENWIDTH+200 + (SCREENWIDTH/2), 'y':pipe2[0]['y']},]
    # list of lower pipe
    lowerPipes = [
        {'x':SCREENWIDTH+200, 'y':pipe1[1]['y']},
        {'x': SCREENWIDTH+200 + (SCREENWIDTH/2), 'y':pipe2[1]['y']},] 

    pipeVelX = -4
    PlayerVelY = -9
    PlayermaxVelY = 10
    PlayerminVelY = -8
    PlayerAccY = 1

    PlayerFlapAcc = -8  # velocity while flapping
    PlayerFlapped = False 

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    PlayerVelY = PlayerFlapAcc
                    PlayerFlapped = True
                    GAME_SOUNDS['wing'].play()

        crash_test = isCollide(playerx , playery , upperPipes, lowerPipes) # return True if the player is crashed
        if crash_test:
            return
        # check the score
        Player_mid_pos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width/2
            if pipeMidPos <= Player_mid_pos < pipeMidPos +4:
                score+=1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()
            if PlayerVelY < PlayermaxVelY and not PlayerFlapped:
                PlayerVely += PlayerAccY
            if PlayerFlapped:
                Playerlapped = False

            playerHeight = GAME_SPRITES['player'].get_height()
            playery = playery + min(PlayerVelY, GROUNDY - playery - playerHeight)

            # move pipe to the left
            for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
                upperPipes['x'] += pipeVelX
                lowerPipes['x'] += pipeVelX

            # new pipe when previous is about to cross the screen
            if 0 < upperPipes[0]['x'] <5:
                newpipe = getRandomPipe()
                upperPipes.append(newpipe[0])
                lowerPipes.append(newpipe[1])

            # when pipe is out of the screen remove it
            if upperPipes[0]['x'] < GAME_SPRITES['pipe'][0].get_width():
                upperPipes.pop(0)
                lowerPipes.pop(0)

            # blit our sprites 
            SCREEN.blit(GAME_SPRITES['background'],(0,0))
            for upperPipe,lowerPipe in zip(upperPipes,lowerPipes):
                SCREEN.blit(GAME_SPRITES['pipe'][0],(upperPipe['x'],upperPipe['y']))
                SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'],lowerPipe['y']))
            SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
            SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
            myDigits = [int(x) for x in list(str(score))]
            width = 0            
            for digit in myDigits:
                width += GAME_SPRITES['numbers'][digit].get_width()
            xoffset = (SCREENWIDTH-width)/2

            for digit in myDigits:
                SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset), SCREENHEIGHT/2)
                Xoffset += GAME_SPRITES['numbers'][digit].get_width()
            pygame.display.update()
            FPSCLOCK.tick(FPS)

def isCollide(playerx , playery , upperPipes, lowerPipes):
    if playery > GROUNDY - 25 or playery < 0:
        GAME_SOUNDS['hit'].play()
        return True

    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if (playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True
    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True
    return True

def getRandomPipe():
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 * offset))
    pipeX = SCREENWIDTH +10
    y1 = pipeHeight - y2 + 10 
    pipe = [{'x': pipeX, 'y': -y1},
            {'x' : pipeX,'y':y2}]
    return pipe

if  __name__ == '__main__':
    # This is main point from which our game will start
    pygame.init() # Initialize pygame all modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird by Farwah')
    GAME_SPRITES['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
     )  
        
    GAME_SPRITES['message'] = pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
    pygame.image.load(PIPE).convert_alpha()
    )

    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()     
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        WelcomeScreen()
        mainGame()
