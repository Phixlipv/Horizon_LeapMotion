## -*- coding: utf-8 -*-
import pygame, sys, Leap, thread, time
from pygame.locals import *

#---Globle Preset---#
Screen_Width=1200
Screen_Height=900
FPS=60
FPS_Clock=pygame.time.Clock()

frame = None
Pause = False
Song_change = False

#Color:
Black=(0,0,0)
White=(255,255,255)
Blue1 = (94,223,182)
Blue2 = (73,125,173)

Swipe_distance = 0

Song_Number = 1

Action_Wait = 0

Music_volume = 0.5

Music_paused = True

Music_file = None

Onging_gesture = None

NC_Xpos = 1000

CC_Xpos = 0

NC_Right_Xpos = -800



#---Globle Preset---#

pygame.init()
Display_surface = pygame.display.set_mode((Screen_Width, Screen_Height),RESIZABLE)
pygame.display.set_caption('Music Player')

Start_icon=pygame.image.load('Start3.png')
Pause_icon=pygame.image.load('Pause3.png')




def main():
    global Song_Number, Action_Wait, Song_change, Music_volume, Music_paused, Music_file, Onging_gesture


    #pygame.display.set_icon()

    listener = Leap.Listener()
    controller = Leap.Controller()

    controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
    controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
##    controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)
    controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)

    controller.add_listener(listener)

##    controller.config.set("Gesture.KeyTap.MinDownVelocity", 1.0)
##    controller.config.set("Gesture.KeyTap.HistorySeconds", .1)
##    controller.config.set("Gesture.KeyTap.MinDistance", 1.0)
##    controller.config.save()


    
    pygame.mixer.set_num_channels(1)
    Music_file = pygame.mixer.Sound('M1.ogg')

    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.load('M1.ogg')
    pygame.mixer.music.play()
    pygame.mixer.music.pause()
    

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        Display_surface.fill(White)

        Progress_bar()
        Volume_bar()
        Image_cover()
        Pause_Start_icon()
            


        if Song_change:
            pygame.mixer.Sound.stop(Music_file)
            Music_file = pygame.mixer.Sound('M%s.ogg' % (Song_Number))
            
            pygame.mixer.music.load('M%s.ogg' % (Song_Number))
            pygame.mixer.music.play()

            Music_paused = False
            
            Song_change = False





        frame = controller.frame()

        if Action_Wait > 60:

            for gesture in frame.gestures():


                if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                    print "Tapping"
                    Action_Wait = 0
                    if Music_paused:
                        Music_paused = False
                        pygame.mixer.music.unpause()
                    else:
                        Music_paused = True
                        pygame.mixer.music.pause()
                        


                elif gesture.type == Leap.Gesture.TYPE_SWIPE:
                    swipe = Leap.SwipeGesture(gesture)
                    if abs(swipe.direction[0]) > abs(swipe.direction[1]):
                        
                        if swipe.direction[0] < 0:
                            print "Left Swipe"
                            Onging_gesture = "Left Swipe"
                            Action_Wait = 0
                            if Song_Number < 5:
                                Song_Number += 1
                                Song_change = True

                        elif swipe.direction[0] > 0:
                            print "Right Swipe"
                            Onging_gesture = "Right Swipe"
                            Action_Wait = 0
                            if Song_Number > 1:
                                Song_Number -= 1
                                Song_change = True

                        else:
                            print "No swipe"


                elif gesture.type == Leap.Gesture.TYPE_CIRCLE:
                    circle = Leap.CircleGesture(gesture)
                    if (circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2):
                        print "clockwise_circle"
                        if Music_volume < 1:
                            Music_volume += 0.01
                            pygame.mixer.music.set_volume(Music_volume)
                        print pygame.mixer.music.get_volume()
                    else:
                        print "anticlockwise_circle"
                        if Music_volume > 0:
                            Music_volume -= 0.01
                            pygame.mixer.music.set_volume(Music_volume)
                        print pygame.mixer.music.get_volume()
                        

        else:
            Action_Wait += 1
                        

                

        pygame.display.flip()
        FPS_Clock.tick(FPS)




def Progress_bar():
    
    Current_progress = pygame.mixer.music.get_pos()/1000
    Total_length = pygame.mixer.Sound.get_length(Music_file)
    Progress_TLength_ratio = Current_progress/Total_length

    pygame.draw.rect(Display_surface, Blue1, (Screen_Width*0.15, 0.9*Screen_Height, 0.7*Screen_Width, 10))
    pygame.draw.rect(Display_surface, Blue2, (Screen_Width*0.15, 0.9*Screen_Height, Progress_TLength_ratio*0.7*Screen_Width, 10))

def Pause_Start_icon():
    if Music_paused:
        Start_icon_width = Start_icon.get_rect().size[0]
        Start_icon_height = Start_icon.get_rect().size[1]
        Start_icon_Xpos = Screen_Width/2-Start_icon_width/2
        Start_icon_Ypos = Screen_Height/2-Start_icon_height/2
        Display_surface.blit(Start_icon,(Start_icon_Xpos,Start_icon_Ypos))
    else:
        Pause_icon_width = Pause_icon.get_rect().size[0]
        Pause_icon_height = Pause_icon.get_rect().size[1]
        Pause_icon_Xpos = Screen_Width/2-Pause_icon_width/2
        Pause_icon_Ypos = Screen_Height/2-Pause_icon_height/2
        Display_surface.blit(Pause_icon,(Pause_icon_Xpos,Pause_icon_Ypos))

def Volume_bar():
    Volume_ratio = 1 - pygame.mixer.music.get_volume()
    pygame.draw.rect(Display_surface, Blue2, (Screen_Width*0.9, 0.1*Screen_Height, 20, 0.3*Screen_Height))
    pygame.draw.rect(Display_surface, Blue1, (Screen_Width*0.9, 0.1*Screen_Height, 20, Volume_ratio*0.3*Screen_Height))

def Image_cover():
    global NC_Xpos, CC_Xpos, Onging_gesture, NC_Right_Xpos


    New_CC_Xpos = (Screen_Width-pygame.image.load('Cover%s.jpg'%(Song_Number)).get_rect().size[0])/2
    Cover_Ypos = 0.15*Screen_Height

    if Onging_gesture == 'Left Swipe':
        
        Current_cover = pygame.image.load('Cover%s.jpg'%(Song_Number-1))
        Display_surface.blit(Current_cover,(CC_Xpos,Cover_Ypos))
        New_cover = pygame.image.load('Cover%s.jpg'%(Song_Number))
        Display_surface.blit(New_cover,(NC_Xpos,Cover_Ypos))

        if NC_Xpos > New_CC_Xpos:
            CC_Xpos -= 15+(0.012*(NC_Xpos-New_CC_Xpos))**2
            NC_Xpos -= 15+(0.02*(NC_Xpos-New_CC_Xpos))**2  
        else:
            Onging_gesture = None
            
    elif Onging_gesture == 'Right Swipe':
        
        Current_cover = pygame.image.load('Cover%s.jpg'%(Song_Number+1))
        Display_surface.blit(Current_cover,(CC_Xpos,Cover_Ypos))
        New_cover = pygame.image.load('Cover%s.jpg'%(Song_Number))
        Display_surface.blit(New_cover,(NC_Right_Xpos,Cover_Ypos))
        
        if NC_Right_Xpos < New_CC_Xpos:
            CC_Xpos += 15+(0.012*(NC_Right_Xpos-New_CC_Xpos))**2
            NC_Right_Xpos += 15+(0.02*(NC_Right_Xpos-New_CC_Xpos))**2
        else:
            Onging_gesture = None
            
    else: 
        Current_cover = pygame.image.load('Cover%s.jpg'%(Song_Number))
        CC_Xpos = New_CC_Xpos
        NC_Xpos = 1000+Screen_Width/2
        NC_Right_Xpos = -1000-Screen_Width/2
        Display_surface.blit(Current_cover,(CC_Xpos,Cover_Ypos))
            
        
        

if __name__ == '__main__':
    main()


