import cv2
import imagezmq


def process_image(image, sender_name):
    image = cv2.flip(image, 1)
    cv2.imshow(sender_name, image)

image_hub = imagezmq.ImageHub()

while True:
    sender_name, image = image_hub.recv_image()
    image_hub.send_reply(b'ok')
    process_image(image, sender_name)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
