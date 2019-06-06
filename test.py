import threading
import pygame
import pygame.camera
import time



class display(threading.Thread):

    def __init__(self):
        super(display, self).__init__()

        pygame.init()
        pygame.mouse.set_visible(False)
        # infoObject = pygame.display.Info()
        # size=((int(infoObject.current_w), int(infoObject.current_h)))
        size=(800,600)
        self.lcd = pygame.display.set_mode(size)#,pygame.FULLSCREEN)
        self.lcd.fill((0,0,255))
        self.tt=""
        self.x=0
        self.Message="hahaha"
        pygame.display.update()
        pygame.camera.init()

        self.cam = pygame.camera.Camera('/dev/video0', size, 'RGB')
        self.cam.start()

        self.font_big = pygame.font.Font(None, 50)
        self.surf = pygame.Surface(size)



    def run(self):
        self.go()



    def txt2(self):
        self.x=self.x+1
        self.tt=self.x

    def go(self):
        while True:
            # lcd.fill(RED)
            self.cam.get_image(self.surf)
            self.lcd.blit(self.surf, (0, 0))
            self.text()
            pygame.display.update()
            pygame.event.get()


    def get_img(self,fname="img.png"):
        img=self.cam.get_image(self.surf)
        pygame.image.save(img,fname)

    def txt(self,lcd):
        #self.tt=str(datetime.datetime.now())
        color=(0,0,255)
        text_surface = self.font_big.render(str(self.tt), True, color)
        rect = text_surface.get_rect(center=(88, 72))
        lcd.blit(text_surface, rect)

    def text(self):
        if (self.Message != ""):
            # self.lcd.fill(pygame.Color("white"))  # White background
            font = pygame.font.Font(None, 60)
            text = font.render(str(self.Message), 1, (227, 157, 200))
            textpos = text.get_rect()
            textpos.centerx = self.lcd.get_rect().centerx
            textpos.centery = self.lcd.get_rect().centery
            self.lcd.blit(text, textpos)






someClass = display()
someClass.start()
time.sleep(2)

x=0
while x<=10:
    x+=1
    someClass.txt2()
    time.sleep(1)

