import socket
import time
from imutils.video import VideoStream
import imagezmq

#use your own receiver_server address
sender = imagezmq.ImageSender(connect_to='tcp://192.168.0.101:5555')

sender_name = socket.gethostname()
cam = VideoStream(0).start()
time.sleep(2.0)
while True:
    image = cam.read()
    sender.send_image(sender_name, image)
