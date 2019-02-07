import numpy as np
import cv2
import os
import argparse
import glob
import shutil
import vision_test
import pygame
from Settings import Settings

bgTrash = pygame.image.load("trash-small.jpg")
bgRecycle = pygame.image.load("recycle-small.jpg")
bgCompost = pygame.image.load("compost-small.jpg")
bgNone = pygame.image.load("none.jpg")

def take_video():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_POS_MSEC,60)

    FILE_OUTPUT = 'output.mov'

    if os.path.isfile(FILE_OUTPUT):
        os.remove(FILE_OUTPUT)

    currentFrame = 0

    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    out = cv2.VideoWriter()
    success = out.open('output.mov',fourcc, 15.0, (1280,720),True)

    while(cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()

        if ret == True:
            # Handles the mirroring of the current frame
            frame = cv2.flip(frame,1)

            # Saves for video
            out.write(frame)

            # Display the resulting frame
            cv2.imshow('frame',frame)
        else:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # To stop duplicate images
        currentFrame += 1


    # When everything done, release the capture
    cap.release()
    out.release()
    cv2.destroyAllWindows()


def FrameCapture(path):
    shutil.rmtree('shots')
    os.makedirs('shots')

    # Path to video file
    vidObj = cv2.VideoCapture(path)

    # Used as counter variable
    count = 0

    # checks whether frames were extracted
    success = 1

    while success:

        # vidObj object calls read
        # function extract frames
        success, image = vidObj.read()

        # Saves the frames with frame-count
        cv2.imwrite("shots/%d.jpg" % count, image)

        count += 1

def updateScreen(settings, screen):
    screen.fill(settings.bg_color)

    pygame.display.flip()


# Driver Code
if __name__ == '__main__':

    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("RESULT")
    # Calling the function
    take_video()
    FrameCapture("output.mov")
    result = vision_test.check_imgs()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print("quiting")
                quit()
        if result == 'TRASH':
            screen.blit(bgTrash, (0, 0))
        elif result == "RECYCLE":
            screen.blit(bgRecycle, (0,0))
        elif result == "COMPOST":
            screen.blit(bgCompost, (0,0))
        else:
            updateScreen(settings, screen)
            screen.blit(bgNone, (0,0))
        pygame.display.update()

