
import Leap, sys, thread, time


#Global variables
frame = None
Pause = False


#Send instructions to a music player after receiving events from the Leap Motion controller.
#Since we have not selected a music player yet, all the functions in this part are left as blank.
def pause():
    pass

def restart():
    pass

def volume_up():
    pass

def volume_down():
    pass

def next_music():
    pass

def previous_music():
    pass



listener = Leap.Listener()
controller = Leap.Controller()

controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)

controller.add_listener(listener)


while True:
    
    frame = controller.frame()


    for gesture in frame.gestures():

        if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
            print "Tapping"
            if Pause == False:
                pause()
                Pause = True
            else:
                restart()
                Pause = False


        elif gesture.type == Leap.Gesture.TYPE_SWIPE:
            swipe = Leap.SwipeGesture(gesture)
            if abs(swipe.direction[0]) > abs(swipe.direction[1]):
                if swipe.direction[0] < 0:
                    print "Left Swipe"
                    previous_music()
                elif swipe.direction[0] > 0:
                    print "Right Swipe"
                    next_music()
                else:
                    print "No swipe"


        elif gesture.type == Leap.Gesture.TYPE_CIRCLE:
            circle = Leap.CircleGesture(gesture)
            if (circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2):
                print "clockwise_circle"
                volume_up()
            else:
                print "anticlockwise_circle"
                volume_down()




