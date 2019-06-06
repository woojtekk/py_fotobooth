import time
import pygame
import pygame.camera
from pygame.locals import *

DEVICE = '/dev/video0'
SIZE = (640, 480)
FILENAME = 'capture.png'

def camstream():
    pygame.init()
    pygame.camera.init()

    pygame.mouse.set_visible(False)  # hide the mouse cursor

    infoObject = pygame.display.Info()

    screen = pygame.display.set_mode(( infoObject.current_w,  infoObject.current_h),
                                          pygame.FULLSCREEN)  # Full screen
    #  screen = pygame.display.set_mode((800,600))  # Full screen

    background = pygame.Surface( screen.get_size())  # Create the background object
    background =  background.convert()  # Convert it to a background



    #display = pygame.display.set_mode(SIZE, 0)
    camera = pygame.camera.Camera(DEVICE, SIZE)
    camera.start()

    #screen = pygame.surface.Surface(SIZE, 0, background)
    while True:
        sc = camera.get_image(screen)
        background.blit(sc,(0,0))
        #display.blit(screen, (0,0))
        pygame.background.flip()

    camera.stop()
    pygame.quit()
    return

if __name__ == '__main__':
    camstream()