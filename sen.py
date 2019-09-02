import RPi.GPIO as GPIO
import time,os
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)         #Read output from PIR motion sensor
try:
        print 'PIR Module Test'
        time.sleep(2)
        print 'Ready'
	while True:
		print 'Detecting'
                if GPIO.input(11):
                        print 'Motion Detected!!!'					    
		        print "Video streaming server started!!!"
			os.chdir("/usr/src/mjpg-streamer/mjpg-streamer-experimental/")
			os.system('./mjpg_streamer -o "output_http.so -w ./www" -i "input_uvc.so -f 20 -r 480x320" ')             
			#os.system("./vidcap.sh")
			time.sleep(1)
		time.sleep(10)
except KeyboardInterrupt:
               print 'Quit'
               GPIO.cleanup()
