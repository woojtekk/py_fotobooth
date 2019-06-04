import pygame
import time
#import picamera
import cv2
import shutil
import os
import PIL.Image
import datetime
import time
import numpy as np
from resizeimage import resizeimage
from imutils import build_montages


from threading import Thread
from pygame.locals import *
from time import sleep
from PIL import Image, ImageDraw


class camera():
    def __init__(self):
        pygame.init()  # Initialise pygame
        pygame.mouse.set_visible(False)  # hide the mouse cursor
        self.infoObject = pygame.display.Info()

        self.screen = pygame.display.set_mode((self.infoObject.current_w, self.infoObject.current_h), pygame.FULLSCREEN)  # Full screen
        #self.screen = pygame.display.set_mode((800,600))  # Full screen

        self.background = pygame.Surface(self.screen.get_size())  # Create the background object
        self.background = self.background.convert()  # Convert it to a background

        # self.screenPicture = pygame.display.set_mode((self.infoObject.current_w, self.infoObject.current_h), pygame.FULLSCREEN)  # Full screen
        # #self.screenPicture = pygame.display.set_mode((800,600))  # Full screen
        # self.backgroundPicture = pygame.Surface(self.screenPicture.get_size())  # Create the background object
        # self.backgroundPicture = self.background.convert()  # Convert it to a background

        self.screen.fill(pygame.Color("orange"))  # clear the screen
        pygame.display.flip()

        # self.camera=picamera.PiCamera()
        # camera.resolution = "720p"
        # camera.rotation = 0
        # camera.hflip = True
        # camera.vflip = False
        # camera.brightness = 50
        # camera.preview_alpha = 120
        # camera.preview_fullscreen = True
        sleep(1)
        self.UpdateDisplay("INIT ....")

    def check_file_name(self, fname):
        fname = fname
        index = 0
        root, ext = os.path.splitext(os.path.expanduser(fname))
        fname = os.path.basename(root)
        dir = os.path.dirname(root)
        filename = "{0}_{1:03d}{2}".format(fname, index, ext)
        while filename in os.listdir(dir):
            filename = "{0}_{1:03d}{2}".format(fname, index, ext)
            index += 1
        filename = str(dir + "/" + filename)
        with open(str("filename.log"), 'a') as the_file: the_file.write(str(datetime.datetime.now()) +"\t"+ str(filename) + "\n")
        return filename

    def camera_show_image(self,image_path):
        print("show start image")
        self.screen.fill(pygame.Color("white"))  # clear the screen
        img = pygame.image.load(image_path)  # load the image
        img = img.convert()
        w, h = pygame.display.get_surface().get_size()
        img = pygame.transform.scale(img, (w, h))

        x = (self.infoObject.current_w / 2) - (img.get_width() / 2)
        y = (self.infoObject.current_h / 2) - (img.get_height() / 2)
        self.screen.blit(img, (x, y))
        pygame.display.flip()

    def UpdateDisplay(self,Message,ImageShowed = False):
        pygame.event.get()

        self.background.fill(pygame.Color("white"))  # White background
        if (Message != ""):
            font = pygame.font.Font(None, 30)
            text = font.render(Message, 1, (227, 157, 200))
            textpos = text.get_rect()
            textpos.centerx = self.background.get_rect().centerx
            textpos.centery = self.background.get_rect().centery
            if (ImageShowed):
                self.backgroundPicture.blit(text, textpos)
            else:
                self.background.blit(text, textpos)

        if (ImageShowed == True):
            self.screenPicture.blit(self.backgroundPicture, (0, 0))
        else:
            self.screen.blit(self.background, (0, 0))

        pygame.display.flip()
        return


    def camera_CapturePicture(self):
        #camera.start_preview()
        self.UpdateDisplay("let's go ....")
        time.sleep(0.1)

        Fname = "foto/fotobudka"
        Fname = self.check_file_name(Fname + ".png")
        open(Fname, 'a').close()
        Fname_list=[Fname]
        for y in range(1,5,1):
            Fn = self.check_file_name(Fname)
            Fname_list.append(Fn)
            for x in range(5, -1, -1):
                if x == 0: Message = ".... P S T R Y K ......."
                else:      Message = str(y)+"/4 "+str(x)
                self.UpdateDisplay(Message,False)
                time.sleep(1)
            # camera.capture(Fn)
            # open(Fn, 'a').close()
            shutil.copy("ustawienia/start_image.png", Fn)
        # camera.stop_previe
        return Fname_list


    def create_colage_cv(self,fnames):
        FinalName=fnames[0]

        szablon = cv2.imread("ustawienia/szablon.png", cv2.IMREAD_COLOR)
        size=(int(szablon.shape[1]/2),int(szablon.shape[0]/2))
        size2=(size[0]*2,size[1]*2)

        szablon = cv2.resize(szablon, size2)

        img1 = cv2.imread(fnames[1], cv2.IMREAD_COLOR)
        img2 = cv2.imread(fnames[2], cv2.IMREAD_COLOR)
        img3 = cv2.imread(fnames[3], cv2.IMREAD_COLOR)
        img4 = cv2.imread(fnames[4], cv2.IMREAD_COLOR)

        img1 = cv2.resize(img1, size)
        img2 = cv2.resize(img2, size)
        img3 = cv2.resize(img3, size)
        img4 = cv2.resize(img4, size)

        imgA = np.concatenate((img1, img2), axis=0)
        imgB = np.concatenate((img3, img4), axis=0)

        imgC = np.concatenate((imgA, imgB), axis=1)
        img = cv2.addWeighted(imgC, 1, szablon, 1, 0)

        img = cv2.resize(img, None, fx = 0.5, fy = 0.5)

        cv2.imwrite(FinalName,img)
        return FinalName

    def camera_sequence(self):
        files  = self.camera_CapturePicture()

        start = time.time()
        colage = self.create_colage_cv(files)
        print("CV. ",time.time()-start)
        self.show_colage(colage)
        time.sleep(4)


    def show_colage(self,fn):
        image = pygame.image.load(fn).convert_alpha()
        image = pygame.transform.scale(image, self.screen.get_size())

        sprite = pygame.sprite.Sprite()
        sprite.image = image
        sprite.rect = image.get_rect()

        font = pygame.font.SysFont('Calibri', 100, bold=True)
        text = font.render(' Drukowanie ...... ', True, (227, 157, 200))
        sprite.image.blit(text, ( int(self.screen.get_rect().centerx/2) , int(self.screen.get_rect().centery/2) ))
        #
        text = font.render('...... troche to potrwa ', True, (227, 157, 200))
        sprite.image.blit(text, ( int(self.screen.get_rect().centerx/2) , int(self.screen.get_rect().centery/2)+300 ))

        group = pygame.sprite.Group()
        group.add(sprite)
        group.draw(self.screen)

        pygame.display.flip()


if __name__ == '__main__':
    start = time.time()
    c=camera()
    c.camera_show_image("./ustawienia/start_image.png")
    time.sleep(5)

    c.camera_sequence()
    print("caly program ", time.time()-start)
