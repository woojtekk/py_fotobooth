import queue
import threading
import pygame
import pygame.camera
import datetime
import time
import os



class display(threading.Thread):

    def __init__(self, q, loop_time = 1.0/60):
        self.q = q
        self.timeout = loop_time
        super(display, self).__init__()
        pygame.init()
        pygame.mouse.set_visible(True)
        # infoObject = pygame.display.Info()
        # size=((int(infoObject.current_w), int(infoObject.current_h)))
        size=(800,600)
        self.lcd = pygame.display.set_mode(size)#,pygame.FULLSCREEN)
        self.tt="............."
        self.x=0
        self.lcd.fill((0,0,255))

        pygame.display.update()
        pygame.camera.init()

        self.cam = pygame.camera.Camera('/dev/video0', size, 'RGB')
        self.cam.start()

        self.font_big = pygame.font.Font(None, 50)
        self.surf = pygame.Surface(size)


    def onThread(self, function, *args, **kwargs):
        self.q.put((function, args, kwargs))

    def run(self):
        self.go()

    def txt(self,lcd):
        #self.tt=str(datetime.datetime.now())
        color=(0,0,255)

        text_surface = self.font_big.render(self.tt, True, color)
        rect = text_surface.get_rect(center=(88, 72))
        lcd.blit(text_surface, rect)

    def txt2(self):
        print(self.tt,"--------------",self.x)
        self.x=self.x+1
        self.tt=self.x

    def go(self):
        while True:
            # lcd.fill(RED)
            self.cam.get_image(self.surf)
            self.lcd.blit(self.surf, (0, 0))
            self.txt(self.lcd)
            pygame.display.update()





someClass = display(1)
someClass.start()
time.sleep(2)
while True:
    print("ssss")
    someClass.txt2()
    time.sleep(2)




#
# t1 = Thread(target=display)
# t1.daemon = False
# #t2 = Thread(target=display2)
# #t2.daemon = False
#
#
# t1.start()
# #t2.start()
