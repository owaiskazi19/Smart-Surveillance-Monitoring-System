import cv2
import sys
import time
import numpy as np
# The two main parameters that affect movement detection sensitivity
# are BLUR_SIZE and NOISE_CUTOFF. Both have little direct effect on
# CPU usage. In theory a smaller BLUR_SIZE should use less CPU, but
# for the range of values that are effective the difference is
# negligible. The default values are effective with on most light
# conditions with the cameras I have tested. At these levels the
# detectory can easily trigger on eye blinks, yet not trigger if the
# subject remains still without blinking. These levels will likely be
# useless outdoors.
BLUR_SIZE = 3
NOISE_CUTOFF = 12
# Ah, but the third main parameter that affects movement detection
# sensitivity is the time between frames. I like about 10 frames per
# second. Even 4 FPS is fine.
#FRAMES_PER_SECOND = 10

cam = cv2.VideoCapture(0)
# 320*240 = 76800 pixels
#cam.set(3, 320)
#cam.set(4, 240)
# 640*480 = 307200 pixels
cam.set(3,1080)
cam.set(4,720)
window_name = "delta view"
#window_name = cv2.resize(window_nam, (100, 50)) 
#cv2.namedWindow(window_name, cv2.CV_WINDOW_AUTOSIZE)
window_name_now = "now view"
#cv2.namedWindow(window_name_now, cv2.CV_WINDOW_AUTOSIZE)

# Stabilize the detector by letting the camera warm up and
# seeding the first frames.
#frame_no = cam.read()[1]
frame_now = cam.read()[1]
#np.array(frame_now)[:50,:50]
frame_now = frame_now[:100,:100]
print (len(frame_now[0]))
#frame_now = [[0 for x in range(50)] for x in range(50)] 
#for i in range(50):
#    for j in range(50):
#        frame_now[i][j] = frame_no[i][j]
frame_now = cv2.cvtColor(frame_now, cv2.COLOR_RGB2GRAY)
frame_now = cv2.blur(frame_now, (BLUR_SIZE, BLUR_SIZE))
frame_prior = frame_now

delta_count_last = 1
while True:
    frame_delta = cv2.absdiff(frame_prior, frame_now)
    frame_delta = cv2.threshold(frame_delta, NOISE_CUTOFF, 255, 3)[1]
    delta_count = cv2.countNonZero(frame_delta)

    # Visual detection statistics output.
    # Normalize improves brightness and contrast.
    # Mirror view makes self display more intuitive.
    cv2.normalize(frame_delta, frame_delta, 0, 255, cv2.NORM_MINMAX)
    frame_delta = cv2.flip(frame_delta, 1)
    cv2.putText(frame_delta, "DELTA: %d" % (delta_count),
            (5, 15), cv2.FONT_HERSHEY_PLAIN, 0.8, (255, 255, 255))
    cv2.imshow(window_name, frame_delta)

    #frame_delta = cv2.threshold(frame_delta, 92, 255, 0)[1]
    dst = cv2.flip(frame_now, 1)
    dst = cv2.addWeighted(dst,1.0, frame_delta,0.9,0)
    cv2.imshow(window_name_now, dst)

    # Stdout output.
    # Only output when there is new movement or when movement stops.
    # Time codes are in epoch time format.
    if (delta_count_last == 0 and delta_count != 0):
        sys.stdout.write("MOVEMENT %f\n" % time.time())
        sys.stdout.flush()
    elif delta_count_last != 0 and delta_count == 0:
        sys.stdout.write("STILL    %f\n" % time.time())
        sys.stdout.flush()
    delta_count_last = delta_count

    # Advance the frames.
    frame_prior = frame_now
    frame_now = cam.read()[1]
    frame_now = frame_now[:100,:100]
    frame_now = cv2.cvtColor(frame_now, cv2.COLOR_RGB2GRAY)
    frame_now = cv2.blur(frame_now, (BLUR_SIZE, BLUR_SIZE))
    # Wait up to 10ms for a key press. Quit if the key is either ESC or 'q'.
    key = cv2.waitKey(10)
    if key == 0x1b or key == ord('q'):
        cv2.destroyWindow(window_name)
        break

#    # Morphology noise filters. They work, but really don't help much.
#    # A simple noise cutoff and blur is good enough.
#kernel = numpy.ones((5,5), numpy.uint8)
#    cv2.morphologyEx(frame_delta, cv2.MORPH_OPEN, kernel)
#    cv2.morphologyEx(frame_delta, cv2.MORPH_CLOSE, kernel)
#    # A bilateral filter also seems pointless.
#    #frame_now = cv2.bilateralFilter(frame_now,9,75,75)

# vim: set ft=python fileencoding=utf-8 sr et ts=4 sw=4 : See help 'modeline'
