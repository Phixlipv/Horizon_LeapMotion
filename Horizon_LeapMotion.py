
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



class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']

    def on_frame(self, controller):
        global frame, Pause
        # Get the most recent frame captured by the Leap Motion and report some basic information
        frame = controller.frame()

        #Get gestures
        for gesture in frame.gestures():

            #Return True when fingers are tapping the controller
            if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                print "Tapping"
                if Pause == False:
                    pause()
                    Pause = True
                else:
                    restart()
                    Pause = False

            #Detect whether a hand is swiping to the left or the right
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

            #Detect whether a finger is drawing circle clockwise or anticlockwise
            elif gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = Leap.CircleGesture(gesture)
                if (circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2):
                    print "clockwise_circle"
                    volume_up()
                else:
                    print "anticlockwise_circle"
                    volume_down()

        # Get hands
        for hand in frame.hands:

            handType = "Left hand" if hand.is_left else "Right hand"

            print "  %s, id %d, position: %s" % (
                handType, hand.id, hand.palm_position)

            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction

            # Calculate the hand's pitch, roll, and yaw angles
            print "  pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
                direction.pitch * Leap.RAD_TO_DEG,
                normal.roll * Leap.RAD_TO_DEG,
                direction.yaw * Leap.RAD_TO_DEG)

            # Get arm bone
            arm = hand.arm
            print "  Arm direction: %s, wrist position: %s, elbow position: %s" % (
                arm.direction,
                arm.wrist_position,
                arm.elbow_position)

            # Get fingers
            for finger in hand.fingers:

                print "    %s finger, id: %d, length: %fmm, width: %fmm" % (
                    self.finger_names[finger.type],
                    finger.id,
                    finger.length,
                    finger.width)

                # Get bones
                for b in range(0, 4):
                    bone = finger.bone(b)
                    print "      Bone: %s, start: %s, end: %s, direction: %s" % (
                        self.bone_names[bone.type],
                        bone.prev_joint,
                        bone.next_joint,
                        bone.direction)

        if not frame.hands.is_empty:
            print ""



def main():
    #Create a Leap Motion listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    #Enable 3 types of built-in gesture detection method
    controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
    controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
    controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)
    
    #Have the sample listener receive events from the controller
    controller.add_listener(listener)

    #Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        #Remove the sample listener when done
        controller.remove_listener(listener)
    
if __name__ == "__main__":
    main()
