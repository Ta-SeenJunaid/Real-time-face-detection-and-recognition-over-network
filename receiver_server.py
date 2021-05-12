import cv2
import face_recognition
import imagezmq
import numpy as np
import os

path = 'image_attendance'
images = []
class_names = []
my_list = os.listdir(path)


def process_image(image, sender_name):
    image = cv2.flip(image, 1)

    img_small = cv2.resize(image, (0,0), None, 0.25, 0.25)
    img_small = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)

    faces_current_frame = face_recognition.face_locations(img_small)
    encodes_current_frame = face_recognition.face_encodings(img_small, faces_current_frame)

    for encode_face, face_loc in zip(encodes_current_frame, faces_current_frame):
        matches = face_recognition.compare_faces(encode_list_known, encode_face)
        face_dis = face_recognition.face_distance(encode_list_known, encode_face)
        # print(face_dis)
        match_index = np.argmin(face_dis)

        if matches[match_index]:
            name = class_names[match_index].upper()
            # print(name)
            y1, x2, y2, x1 = face_loc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(image, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(image, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            mark_attendance(name)

    cv2.imshow(sender_name, image)


for cl in my_list:
    cur_img = cv2.imread(f'{path}/{cl}')
    images.append(cur_img)
    class_names.append(os.path.splitext(cl)[0])
print(class_names)


def find_encodings(images):
    encode_list = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encode_list.append(encode)
    return encode_list


def mark_attendance(name):
    pass

encode_list_known = find_encodings(images)
print('Encoding Complete')

image_hub = imagezmq.ImageHub()

while True:
    sender_name, image = image_hub.recv_image()
    image_hub.send_reply(b'ok')
    process_image(image, sender_name)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
