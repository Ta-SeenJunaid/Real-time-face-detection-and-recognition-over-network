import socket
import time
from imutils.video import VideoStream
import imagezmq
import argparse


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="This is sender which will send"
                    "real time video to receiver")

    parser.add_argument('--receiver_ip', required=False,
                        help='please provide the receiver IP, '
                             'example: --receiver_ip \'tcp://192.168.0.101:5555\', '
                             'default=\'tcp://0.0.0.0:5555\'',
                        type=str,
                        default='tcp://0.0.0.0:5555')

    args = parser.parse_args()

    # use your own receiver_server address
    sender = imagezmq.ImageSender(connect_to=args.receiver_ip)

    sender_name = socket.gethostname()
    cam = VideoStream(0).start()
    time.sleep(2.0)
    while True:
        image = cam.read()
        sender.send_image(sender_name, image)


