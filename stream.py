import os,time,signal
#print "Video streaming server started!!!"
#os.chdir("/usr/src/mjpg-streamer/mjpg-streamer-experimental/")
#os.system('./mjpg_streamer -o "output_http.so -w ./www" -i "input_uvc.so -f 20 -r 480x320" &')
ip=raw_input("Enter IP Address of Raspberry Pi")
print "Recording video!!!"
filename = time.strftime("%Y%m%d%H%M%S",time.localtime())+".mp4"

try:
	os.system('cvlc http://'+ip+':8080/?action=stream --sout="#duplicate{dst=std{access=file,mux=mp4,dst='+filename+'}, dst=display}" --run-time=30 --stop-time=30 vlc://quit')

except Exception, e:
	print "error"
print "Done Recording!!!"
#print "Transferring file"
#user=raw_input("Enter Remote Machine Username")
#ip2=raw_input("Enter Remote Machine IP Address")
#path=raw_input("Enter path to tranfer the file")
#os.system("sudo scp "+filename+" "+user+"@"+ip2+":"+path)
#print "File Transferred!!!"
pid=os.system("pgrep mjpg_streamer")
#os.kill(pid,signal.SIGTERM)

