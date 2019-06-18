# This script contains the Camera class object, to capture live video feed and
# return frames with face bounding box and smile predictions marked

import cv2
import face_recognition
from smile_recognition import predict_smile


class Camera(object):
    """Camera class.

    Attributes
    ----------
    video : VideoCapture object
        Object for video capturing from cameras.

    """

    def __init__(self):
        """Initialize video capture object with set width, height and FPS.
        Note: When resolution or FPS of camera used is not available,
        nothing is changed or the nearest resolution is set."""
        self.video = cv2.VideoCapture(0)
        # Set properties
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 270)
        self.video.set(cv2.CAP_PROP_FPS, 25)

    def __del__(self):
        """Release capture when done"""
        self.video.release()

    def get_frame(self):
        """Get each frame from video feed, call face_locations() and
        predict_smile() to find face bounding box and smile prediction,
        and return frame with marked box and prediction."""

        # Grabs, decodes, and returns the next video frame
        ret, frame = self.video.read()

        # Convert image into grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Find all the faces in the current frame of video
        face_locations = face_recognition.face_locations(gray)

        # For each face detected, put bounding box around face detected
        # and display smile prediction
        for face_location in face_locations:
            count = 0

            # Pixel location for face bounding box
            top, right, bottom, left = face_location
            box = (left, top, right, bottom)

            # Call predict_smile() method to predict probabilities for smile
            # vs no smile
            predictions = predict_smile(gray, box, count)

            # Draw a box around the face on current frame
            cv2.rectangle(frame, (left, top), (right, bottom),
                          (255, 255, 255), 2)

            # Round predictions and display on current frame
            smile_prob = str(round((predictions[0][1])*100, 1))
            cv2.putText(frame, f'{smile_prob}% smiling', (left, bottom+35),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            count += 1

        # Encodes and return an image into a memory buffer
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
