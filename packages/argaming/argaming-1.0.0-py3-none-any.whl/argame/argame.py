
from multiprocessing import Process, current_process


import cv2
import mediapipe as mp
import time
import numpy as np


# hand_dectection_value=0

def hand_dectection():
    time.sleep(2)
    # TO OPEN WEBCAM
    cap = cv2.VideoCapture(0)

    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils

    pTime = 0
    ctIME = 0
    while True:
        global hand_dectection_value
        hand_dectection_value=0

        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        # If it detects hand then it will draw 20 red points and lines connecting those points.

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                # Lets get id no for hand and landmark location
                for id, lm in enumerate(handLms.landmark):
                    # print(id, lm)
                    h, w, c = img.shape  # it gives us height and width and channel on image
                    cx, cy = int(lm.x * w), int(lm.y * h)  # it will give us cx and xy position
                    print(id, cx, cy)

                    if id == 8:
                        cv2.circle(img, (cx, cy), 15, (200, 100, 200), cv2.FILLED)
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)


                hand_dectection_value=1
                return(hand_dectection_value)
        # Lets show time on top corner
        cTime = time.time()
        fpS = 1 / (cTime - pTime)
        pTime = cTime
        return (hand_dectection_value)
        cv2.putText(img, str(int(fpS)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)











def index_finger_coordinates():
    time.sleep(2)
    # TO OPEN WEBCAM
    cap = cv2.VideoCapture(0)

    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils

    pTime = 0
    ctIME = 0
    while True:


        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        # If it detects hand then it will draw 20 red points and lines connecting those points.

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                # Lets get id no for hand and landmark location
                for id, lm in enumerate(handLms.landmark):
                    # print(id, lm)
                    h, w, c = img.shape  # it gives us height and width and channel on image
                    cx, cy = int(lm.x * w), int(lm.y * h)  # it will give us cx and xy position
                    # print(id, cx, cy)

                    if id == 8:
                        cv2.circle(img, (cx, cy), 15, (200, 100, 200), cv2.FILLED)
                        print(cx,cy)
                        return (cx,cy)
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

        return(0,0)


        # Lets show time on top corner
        cTime = time.time()
        fpS = 1 / (cTime - pTime)
        pTime = cTime
        return (index_finger_coordinates_value)
        cv2.putText(img, str(int(fpS)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)





















def finger_count():
    cap = cv2.VideoCapture(0)

    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils

    pTime = 0
    ctIME = 0

    while True:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        # If it detects hand then it will draw 20 red points and lines connecting those points.
        tip_index1 = 0
        compair_index1 = 0

        tip_index2 = 0
        compair_index2 = 0

        tip_index3 = 0
        compair_index3 = 0

        tip_index4 = 0
        compair_index4 = 0

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                # Lets get id no for hand and landmark location
                for id, lm in enumerate(handLms.landmark):
                    # print(id, lm)
                    h, w, c = img.shape  # it gives us height and width and channel on image
                    # print(h,w, c)

                    cx, cy = int(lm.x * w), int(lm.y * h)  # it will give us cx and xy position
                    # if id == 8:
                    # here you can get value of index not confirm
                    # print(id, cx, cy)

                    # Index fingure1
                    if id == 8:
                        tip_index1 = cy
                    if id == 6:
                        compair_index1 = cy

                    # Index fingure2
                    if id == 12:
                        tip_index2 = cy
                    if id == 10:
                        compair_index2 = cy

                    # Index fingure1
                    if id == 16:
                        tip_index3 = cy
                    if id == 13:
                        compair_index3 = cy

                    # Index fingure1
                    if id == 20:
                        tip_index4 = cy
                    if id == 17:
                        compair_index4 = cy

                    fingure_countt = 0
                    if tip_index1 < compair_index1:
                        fingure_countt = 1

                    if tip_index1 < compair_index1 and tip_index2 < compair_index2:
                        fingure_countt = 2

                    if tip_index1 < compair_index1 and tip_index2 < compair_index2 and tip_index3 < compair_index3:
                        fingure_countt = 3

                    if tip_index1 < compair_index1 and tip_index2 < compair_index2 and tip_index3 < compair_index3 and tip_index4 < compair_index4:
                        fingure_countt = 4

                return(fingure_countt)
                    # cv2.circle(img, (cx, cy), 15, (200, 100, 200), cv2.FILLED)

                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)


def face_direction():
    mp_face_mesh = mp.solutions.face_mesh  # MediaPipe -- Face Mesh is a face geometry solution that estimates 468 3D face landmarks in real-time
    face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5,
                                      min_tracking_confidence=0.5)  # confidence score in tracking the face

    mp_drawing = mp.solutions.drawing_utils

    drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

    cap = cv2.VideoCapture(0)

    while cap.isOpened():

        global face_dectection_value
        face_dectection_value=0
        success, image = cap.read()

        start = time.time()

        # Flip the image horizontally for a later selfie-view display
        # Also convert the color space from BGR to RGB
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

        # To improve performance
        image.flags.writeable = False

        # Get the result
        results = face_mesh.process(image)

        # To improve performance
        image.flags.writeable = True

        # Convert the color space from RGB to BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        img_h, img_w, img_c = image.shape  # Get height, width and channel from shape.
        face_3d = []
        face_2d = []

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                for idx, lm in enumerate(face_landmarks.landmark):
                    if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                        if idx == 1:
                            nose_2d = (lm.x * img_w, lm.y * img_h)
                            nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 3000)

                        x, y = int(lm.x * img_w), int(lm.y * img_h)

                        # Get the 2D Coordinates
                        face_2d.append([x, y])

                        # Get the 3D Coordinates
                        face_3d.append([x, y, lm.z])

                        # Convert it to the NumPy array
                face_2d = np.array(face_2d, dtype=np.float64)

                # Convert it to the NumPy array
                face_3d = np.array(face_3d, dtype=np.float64)

                # The camera matrix
                focal_length = 1 * img_w

                cam_matrix = np.array([[focal_length, 0, img_h / 2],
                                       [0, focal_length, img_w / 2],
                                       [0, 0, 1]])

                # The distortion parameters
                dist_matrix = np.zeros((4, 1), dtype=np.float64)

                # Solve PnP
                success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)

                # Get rotational matrix
                rmat, jac = cv2.Rodrigues(rot_vec)

                # Get angles
                angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

                # Get the y rotation degree
                x = angles[0] * 360
                y = angles[1] * 360
                z = angles[2] * 360

                # See where the user's head tilting
                if y < -10:
                    text = "Looking Left"
                    face_dectection_value='L'
                    print("L E F T")
                    return(face_dectection_value)
                elif y > 10:
                    text = "Looking Right"
                    face_dectection_value='R'
                    return(face_dectection_value)
                    print("R I G H T")
                elif x < -10:
                    text = "Looking Down"
                    face_dectection_value='D'
                    return(face_dectection_value)
                    print("D O W N")
                elif x > 10:
                    text = "Looking Up"
                    face_dectection_value='U'
                    return(face_dectection_value)
                    print("U P")
                else:
                    text = "Forward"
                    face_dectection_value='F'
                    print("F O R W A R D")
                    return(face_dectection_value)

                # Display the nose direction
                nose_3d_projection, jacobian = cv2.projectPoints(nose_3d, rot_vec, trans_vec, cam_matrix, dist_matrix)

                p1 = (int(nose_2d[0]), int(nose_2d[1]))
                p2 = (int(nose_2d[0] + y * 10), int(nose_2d[1] - x * 10))  # Scaling the line

                # cv2.line(image, p1, p2, (255, 0, 0), 3)   # Drawing the line on nose

                # Add the text on the image
                cv2.putText(image, text, (20, 50), cv2.FONT_HERSHEY_DUPLEX, 2, (200, 140, 200), 3)
                cv2.putText(image, "x: " + str(np.round(x, 2)), (1100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 110, 255),
                            2)
                cv2.putText(image, "y: " + str(np.round(y, 2)), (1100, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 110, 255),
                            2)
                cv2.putText(image, "z: " + str(np.round(z, 2)), (1100, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 110, 255),
                            2)

            end = time.time()
            totalTime = end - start

            fps = 1 / totalTime
            # print("FPS: ", fps)

            cv2.putText(image, f'FPS: {int(fps)}', (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (200, 255, 90), 2)
        face_dectection_value='N'
        return(face_dectection_value)
        # Showing all landmarks on face
        # mp_drawing.draw_landmarks(
        #     image=image,
        #     landmark_list=face_landmarks,
        #     connections=mp_face_mesh.FACE_CONNECTIONS,
        #     landmark_drawing_spec=drawing_spec,
        #     connection_drawing_spec=drawing_spec)

        cv2.imshow('Head Pose Estimation', image)













if __name__ == '__main__':

    # print(value)
    # worker1 = Process(name='Worker 1', target=worker)
    hand_dectectionS = Process(target=hand_dectection) # use default name
    face_directionS = Process(target=face_direction)
    index_finger_coordinatesS = Process(target=index_finger_coordinates)
    finger_countS = Process(target=finger_count)

    #
    hand_dectectionS.start()
    face_directionS.start()
    index_finger_coordinatesS.start()
    finger_countS.start()










#
# from argame import main
# while True:
#     print(finger_count())


