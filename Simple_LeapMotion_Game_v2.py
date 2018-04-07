# -*- coding: utf-8 -*-
import pygame, sys, random, thread, time, Leap
from pygame.locals import *

#---Global Preset---#

Screen_Width=900
Screen_Height=900


Mouse_Is_Pressing=False

#Color:
Black=(0,0,0)
White=(255,255,255)
Red=(255,0,0)


C_Color = Black
Red_Time = 0


FPS_Clock=pygame.time.Clock()
Display_surface = pygame.display.set_mode((Screen_Width, Screen_Height))



listener = Leap.Listener()
controller = Leap.Controller()

controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)

controller.add_listener(listener)

pygame.init()
pygame.display.set_caption('Game 2')

First_Time_Play = True



x_pos = Screen_Width/2
y_pos = Screen_Height/2

Top_Enemy_pos_fix = []
Bottom_Enemy_pos_fix = []
Left_Enemy_pos_fix = []
Right_Enemy_pos_fix = []

Top_Enemy_pos_change = []
Bottom_Enemy_pos_change = []
Left_Enemy_pos_change = []
Right_Enemy_pos_change = []

Create_Enemies = True
Character_rect = None
You_Failed_Flag = False



def main():
    global x_pos,y_pos,Top_Enemy_pos_fix,Bottom_Enemy_pos_fix,Left_Enemy_pos_fix,Right_Enemy_pos_fix,Top_Enemy_pos_change,Bottom_Enemy_pos_change,Left_Enemy_pos_change,Right_Enemy_pos_change,Create_Enemies,Character_rect,You_Failed_Flag,First_Time_Play

    while True:


        Display_surface.fill(White)
        
        if First_Time_Play == False:
        
            x_pos = Screen_Width/2
            y_pos = Screen_Height/2

            Top_Enemy_pos_fix = []
            Bottom_Enemy_pos_fix = []
            Left_Enemy_pos_fix = []
            Right_Enemy_pos_fix = []

            Top_Enemy_pos_change = []
            Bottom_Enemy_pos_change = []
            Left_Enemy_pos_change = []
            Right_Enemy_pos_change = []

            Create_Enemies = True
            Character_rect = None
            You_Failed_Flag = False

            Write_Words("You failed, press R to restart",Screen_Width/2,Screen_Height/2,30,Black)

        else:
            Write_Words("Press R to start",Screen_Width/2,Screen_Height/2,30,Black)


        
        pygame.display.flip()
        FPS_Clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP and event.key == K_r:

                First_Time_Play = False

                while True:

                    Display_surface.fill(White)

                    Leap_Motion_part()


                    Character(x_pos, y_pos, C_Color)

                    Enemies(3)

                    
                    pygame.display.flip()
                    FPS_Clock.tick(60)


                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()

                    if You_Failed_Flag == True:
                        break




def Leap_Motion_part():
    global x_pos, y_pos, C_Color

    frame = controller.frame()

    for gesture in frame.gestures():

        if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
            print "Tapping"
            C_Color = Red

        elif gesture.type == Leap.Gesture.TYPE_SWIPE:
            swipe = Leap.SwipeGesture(gesture)
            if abs(swipe.direction[0]) > abs(swipe.direction[1]):
                if swipe.direction[0] < 0:
                    print "Left Swipe"
                    x_pos -= 10
                    
                elif swipe.direction[0] > 0:
                    print "Right Swipe"
                    x_pos += 10
                   
                else:
                    print "No swipe"

        elif gesture.type == Leap.Gesture.TYPE_CIRCLE:
            circle = Leap.CircleGesture(gesture)
            if (circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2):
                print "clockwise_circle"
                y_pos -= 4
            else:
                print "anticlockwise_circle"
                y_pos += 4
                

def Character(Xaxis_pos, Yaxis_pos, Color):
    global C_Color, Red_Time
    Character_rect = pygame.draw.rect(Display_surface, Color, (Xaxis_pos, Yaxis_pos, 40, 40))
    
    if C_Color == Red and Red_Time <= 50:
        Red_Time += 1
    else:
        C_Color = Black
        Red_Time = 0


def Enemies(Num):
    global Create_Enemies, Top_Enemy_pos_change, Bottom_Enemy_pos_change, Left_Enemy_pos_change, Right_Enemy_pos_change, Top_Enemy_pos_fix, Bottom_Enemy_pos_fix, Left_Enemy_pos_fix, Right_Enemy_pos_fix, You_Failed_Flag
    
    if Create_Enemies == True:
        for i in range(Num):
            Top_Enemy = random.randint(0,Screen_Width)
            Bottom_Enemy = random.randint(0,Screen_Width)
            Left_Enemy = random.randint(0,Screen_Height)
            Right_Enemy = random.randint(0,Screen_Height)
            
            Top_Enemy_pos_fix.append(Top_Enemy)
            Bottom_Enemy_pos_fix.append(Bottom_Enemy)
            Left_Enemy_pos_fix.append(Left_Enemy)
            Right_Enemy_pos_fix.append(Right_Enemy)
            
            Top_Enemy_pos_change.append(0)
            Bottom_Enemy_pos_change.append(Screen_Height)
            Left_Enemy_pos_change.append(0)
            Right_Enemy_pos_change.append(Screen_Width)

            
        Create_Enemies = False


    Rect_pos = (x_pos, y_pos, 40, 40)
    for i in range(Num):
        Top_Enemy_rect = pygame.draw.rect(Display_surface, Black, (Top_Enemy_pos_fix[i],Top_Enemy_pos_change[i], 10, 10))
        Bottom_Enemy_rect = pygame.draw.rect(Display_surface, Black, (Bottom_Enemy_pos_fix[i],Bottom_Enemy_pos_change[i], 10, 10))
        Left_Enemy_rect = pygame.draw.rect(Display_surface, Black, (Left_Enemy_pos_change[i],Left_Enemy_pos_fix[i], 10, 10))
        Right_Enemy_rect = pygame.draw.rect(Display_surface, Black, (Right_Enemy_pos_change[i],Right_Enemy_pos_fix[i], 10, 10))
        if Top_Enemy_rect.colliderect(Rect_pos) or Bottom_Enemy_rect.colliderect(Rect_pos) or Left_Enemy_rect.colliderect(Rect_pos) or Right_Enemy_rect.colliderect(Rect_pos):
            print "You Failed"
            You_Failed_Flag = True
    
    for i in range(Num):
        Top_Enemy_pos_change[i] += (i+1)*2
        Bottom_Enemy_pos_change[i] -= (i+1)*2
        Left_Enemy_pos_change[i] += (i+1)*2
        Right_Enemy_pos_change[i] -= (i+1)*2

    if Left_Enemy_pos_change[0] > Screen_Width:
        
        Top_Enemy_pos_change = []
        Bottom_Enemy_pos_change = []
        Left_Enemy_pos_change = []
        Right_Enemy_pos_change = []

        Top_Enemy_pos_fix = []
        Bottom_Enemy_pos_fix = []
        Left_Enemy_pos_fix = []
        Right_Enemy_pos_fix = []

        Create_Enemies = True


                    
def Write_Words(string,center_x,center_y,font_size,text_color):
    global Black,White
    font_1 = pygame.font.SysFont('simhei', font_size)
    textSurfaceObj = font_1.render('%s'%(string), True, text_color)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (center_x,center_y)     
    Display_surface.blit(textSurfaceObj, textRectObj)


def Mouse_Clicked_Release():
    global Mouse_Is_Pressing
    if pygame.mouse.get_pressed()[0]:
        Mouse_Is_Pressing=True
    if pygame.mouse.get_pressed()[0]==False and Mouse_Is_Pressing==True:
        Mouse_Is_Pressing=False
        return True
    else:
        return False

    
        
if True:
    main()

