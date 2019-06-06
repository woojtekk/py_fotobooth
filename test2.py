#/usr/bin/env python
# coding: utf-8

import pygame
import pygame.camera
from pygame.locals import *
import time

pygame.init()
pygame.camera.init()


class Capture(object):
    def __init__(self,width=640,heigh=480):
        self.size = (width,heigh)
        self.display = pygame.display.set_mode(self.size, 0,)
        self.clist = pygame.camera.list_cameras()
        if not self.clist:
            raise ValueError("Sorry, no cameras detected!")
        self.cam = pygame.camera.Camera(self.clist[0], self.size, 'RGB') #  RGB HSV YUV
        self.cam.start()
        self.cam.set_controls(hflip = True,vflip = True,brightness =10)  #
        print (self.cam.get_controls())
        self.snapshot = pygame.Surface(self.size, 0, self.display)
        self.thresholded = pygame.surface.Surface(self.size, 0, self.display)

    def get_and_flip(self):
        if self.cam.query_image():
            self.snapshot = self.cam.get_image()
        self.display.blit(self.snapshot, (0,0))
        pygame.display.flip()

    def live(self):
        going = True
        while going:
            events = pygame.event.get()
            for e in events:
                if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                    self.cam.stop()
                    pygame.display.quit()
                    exit()
                    going = False
            if e.type == KEYDOWN:
                if pygame.key.get_pressed()[K_LCTRL] and pygame.key.get_pressed()[K_s]:
                    pygame.image.save(self.snapshot,'%s.jpg' %int(time.time()))
                    print ('save jpg')
                if e.key == K_m:
                    print ('m')
                    pygame.transform.threshold(self.thresholded,self.snapshot,self.ccolor,(30,30,30),(0,0,0),1)
                    pygame.image.save(self.thresholded,'%s.jpg' %self.cc )

            self.get_and_flip()

class effect(Capture):

    def get_and_flip(self):
        self.snapshot = self.cam.get_image(self.snapshot)
        self.display.blit(self.snapshot,(0,0))
        crect = pygame.draw.rect(self.display, (255,0,0,), (305,225,30,30), 2)
        self.ccolor = pygame.transform.average_color(self.snapshot, crect)
        self.cc = "-".join([ str(i) for i in list(self.ccolor[0:3]) ])
        self.display.fill(self.ccolor, (0,0,50,50))
        pygame.display.flip()

    # def get_and_flip(self):
    #     self.snapshot = self.cam.get_image(self.snapshot)
    #     # threshold against the color we got before
    #     mask = pygame.mask.from_threshold(self.snapshot, self.ccolor, (30, 30, 30))
    #     self.display.blit(self.snapshot,(0,0))
    #     # keep only the largest blob of that color
    #     connected = mask.connected_component()
    #     # make sure the blob is big enough that it isn't just noise
    #     if mask.count() > 100:
    #         # find the center of the blob
    #         coord = mask.centroid()
    #         # draw a circle with size variable on the size of the blob
    #         pygame.draw.circle(self.display, (0,255,0), coord, max(min(50,mask.count()/400),5))
    #     pygame.display.flip()

if __name__ == '__main__':
    camera = effect()
    camera.live()