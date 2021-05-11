import cv2
import face_recognition
import imagezmq
import os

path = 'image_attendance'
images = []
class_names = []
my_list = os.listdir(path)


for cl in my_list:
    cur_img = cv2.imread(f'{path}/{cl}')
    images.append(cur_img)
    class_names.append(os.path.splitext(cl)[0])
print(class_names)


def process_image(image, sender_name):
    image = cv2.flip(image, 1)
    cv2.imshow(sender_name, image)


def find_encodings(images):
    encode_list = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encode_list.append(encode)
    return encode_list


encode_list_known = find_encodings(images)
print('Encoding Complete')


image_hub = imagezmq.ImageHub()

while True:
    sender_name, image = image_hub.recv_image()
    image_hub.send_reply(b'ok')
    process_image(image, sender_name)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
