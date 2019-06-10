# library imports
import cv2
import face_recognition
from smile_recognition import predict_smile

# Camera object to capture live video feed and return image with face detected and smile predictions
class Camera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        # set properties
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 270)
        self.video.set(cv2.CAP_PROP_FPS, 25)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, frame = self.video.read()

        # convert image into grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # find all the faces in the current frame of video
        face_locations = face_recognition.face_locations(gray)

        # for each face detected, put bounding box around face detected and display smile predictions
        for face_location in face_locations:
            count = 0

            # pixel location for face bounding box
            top, right, bottom, left = face_location
            box = (left, top, right, bottom)

            # call predict_smile method to prediction probabilities for smile or no smile
            predictions = predict_smile(gray, box, count)

            # draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 255, 255), 2)

            smile_prob = str(round((predictions[0][1])*100, 1))
            cv2.putText(frame, f'{smile_prob}% smiling', (left, bottom+35),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            count += 1

        ret, jpeg = cv2.imencode('.jpg', frame)

        return jpeg.tobytes()
