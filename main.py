import pygame
import random 
import sys
from pygame.locals import *

fps = 32
screenwidth = 289
screenheight = 511

screen = pygame.display.set_mode((screenwidth, screenheight))
groundy = screenheight * 0.8
game_sprites = {}
game_sounds = {}
player = 'gallery/sprites/player.png'
background = 'gallery/sprites/background.png'
pipe = 'gallery/sprites/pipe.png'

def welcomeScreen():
    playerx = int(screenwidth / 2)
    playery = int((screenheight - game_sprites['player'].get_height()) / 2)
    messagex = int((screenwidth - game_sprites['message'].get_width()) / 2)
    messagey = int(screenheight * 0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN or event.type == KEYDOWN and (event.key == K_UP or event.key == K_SPACE) :
                return

            else:
                screen.blit(game_sprites['background'], (0, 0))
                screen.blit(game_sprites['base'], (basex, groundy))
                # screen.blit(game_sprites['pipe'], (0,-390))

                screen.blit(game_sprites['player'], (playerx , playery))
                screen.blit(game_sprites['message'], (messagex, messagey))

                pygame.display.update()
                fpsclock.tick(fps)

def mainGame():
    score = 0
    playerx = int(screenwidth / 5)
    playery = int(screenheight / 2)
    basex = 0

    # Creating a pipe
    newPipe = getRandomPipe()

    # List for pipes
    pipes = [
        {'x': screenwidth +200, 'y': newPipe[0]['y']},
        {'x': screenwidth +200 +(screenwidth/2), 'y': getRandomPipe()[0]['y']}
    ]

    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccV = -8
    playerFlapped = False

    while True:
        for event in pygame.event.get():
            # Quit condition
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # Mouse input
            if event.type == MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                if playery > 0:
                    playerVelY = playerFlapAccV
                    playerFlapped = True
                    game_sounds['wing'].play()

            # Keyboard input
            if event.type == KEYDOWN and (event.key == K_UP or event.key == K_SPACE):
                if playery > 0:
                    playerVelY = playerFlapAccV
                    playerFlapped = True
                    game_sounds['wing'].play()

            if event.type == KEYDOWN and (event.key == K_h):
                score += score + 10


        crashTest = isCollide(playerx, playery, pipes)
        if crashTest:
            return

        # Check for score
        playerMidPos = playerx + game_sprites['player'].get_width() / 2
        for pipe in pipes:
            pipeMidPos = pipe['x'] + game_sprites['pipe'].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f"Your score is {score}")
                game_sounds['point'].play()




        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False

        playerHeight = game_sprites['player'].get_height()
        playery = playery + min(playerVelY, groundy - playery - playerHeight)

        # Move pipes
        for pipe in pipes:
            pipe['x'] += pipeVelX

        # Add a new pipe when the first is about to leave the screen
        if 0 < pipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            pipes.append(newPipe[0])

        # Remove pipe if it is out of the screen
        if pipes[0]['x'] < -game_sprites['pipe'].get_width():
            pipes.pop(0)

        # Blit sprites
        screen.blit(game_sprites['background'], (0, 0))
        for pipe in pipes:
            screen.blit(game_sprites['pipe'], (pipe['x'], pipe['y']))
        screen.blit(game_sprites['base'], (basex, groundy))
        screen.blit(game_sprites['player'], (playerx, playery))






        # Display score
        myDigits = [int(x) for x in list(str(score))]
        width = sum(game_sprites['numbers'][digit].get_width() for digit in myDigits)
        Xoffset = (screenwidth - width) / 2

        for digit in myDigits:
            screen.blit(game_sprites['numbers'][digit], (Xoffset, screenheight * 0.12))
            Xoffset += game_sprites['numbers'][digit].get_width()

        pygame.display.update()
        fpsclock.tick(fps)

def isCollide(playerx, playery, pipes):
    # Collision logic to be implemented
    if playery>groundy-25 or playery<0:
        game_sounds['hit'].play()
        return True
    playerMidPos = playerx + game_sprites['player'].get_width() / 2
    for pipe in pipes:
        pipe_y = pipe['y']
        pipeMidPos = pipe['x'] + game_sprites['pipe'].get_width() / 2
        if pipeMidPos-4 <= playerMidPos < pipeMidPos + 4:
            if playery <= 300+int(pipe_y) :
                game_sounds['hit'].play()
                return True
    for pipe in pipes:
        pipe_y = pipe['y']
        pipeMidPos = pipe['x'] + game_sprites['pipe'].get_width() / 2
        if pipeMidPos-4 <= playerMidPos < pipeMidPos + 4:
            if groundy-20 >= playery >= 370+int(pipe_y) :
                game_sounds['hit'].play()
                return True

    return False

def getRandomPipe():
    y = random.randint(4, 26) * -10
    pipex = screenwidth + 10
    return [{'x': pipex, 'y': y}]

if __name__ == '__main__':
    pygame.init()
    fpsclock = pygame.time.Clock()
    pygame.display.set_caption("Himanshu Flappy Bird")

    # Load sprites
    game_sprites['numbers'] = (
        pygame.image.load("gallery/sprites/0.png").convert_alpha(),
        pygame.image.load("gallery/sprites/1.png").convert_alpha(),
        pygame.image.load("gallery/sprites/2.png").convert_alpha(),
        pygame.image.load("gallery/sprites/3.png").convert_alpha(),
        pygame.image.load("gallery/sprites/4.png").convert_alpha(),
        pygame.image.load("gallery/sprites/5.png").convert_alpha(),
        pygame.image.load("gallery/sprites/6.png").convert_alpha(),
        pygame.image.load("gallery/sprites/7.png").convert_alpha(),
        pygame.image.load("gallery/sprites/8.png").convert_alpha(),
        pygame.image.load("gallery/sprites/9.png").convert_alpha(),

    )
    game_sprites['enemy'] = pygame.image.load("gallery/sprites/enemy.png").convert_alpha()
    game_sprites['message'] = pygame.image.load("gallery/sprites/message.png").convert_alpha()
    game_sprites['base'] = pygame.image.load("gallery/sprites/base.png").convert_alpha()
    game_sprites['pipe'] = pygame.image.load(pipe).convert_alpha()
    game_sprites['player'] = pygame.image.load(player).convert_alpha()
    game_sprites['background'] = pygame.image.load(background).convert()

    # Load sounds
    game_sounds['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    game_sounds['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    game_sounds['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    game_sounds['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    game_sounds['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    while True:
        welcomeScreen()
        mainGame()
