# import libraries
import cv2
import face_recognition
from PIL import Image
from tensorflow.keras.preprocessing.image import img_to_array, array_to_img
import h5py
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pickle

# grab the reference to the webcam
cap = cv2.VideoCapture(0)
# width = 360
# height = 240
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

from sklearn.externals import joblib
scaler_filename = "scaler.save"
scaler = joblib.load(scaler_filename)

# Initialize variables
img_width, img_height = (100, 100)
face_locations = []
text = 'test'
new_model = load_model('my_model.h5')
new_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

def predict_smile (gray, box, count):
    gray = gray.reshape(gray.shape+(1,))
    array_to_img(gray).save(f'current_frame{count}.jpg')

    # load image into a numpy array
    new_img = Image.open(f'current_frame{count}.jpg')

    new_img_resized = new_img.resize((img_width, img_height), box = box)
    new_img_resized.save(f'pre_processed_current_frame{count}.jpg')

    img = Image.open(f'pre_processed_current_frame{count}.jpg')

    new_img_array = img_to_array(img)

    new_img_array = np.array(new_img_array)

    new_img_array = new_img_array.reshape(1, img_width*img_height)
    new_img_array = scaler.transform(new_img_array)

    new_img_array = new_img_array.reshape(1, img_width, img_height, 1)

    return new_model.predict(new_img_array)

while True:
    # Grab a single frame of video
    ret, frame = cap.read()

    # percent = 25
    # width = int(frame.shape[1] * percent/ 100)
    # height = int(frame.shape[0] * percent/ 100)
    # dim = (width, height)
    # frame25 = cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

    # Convert the image from BGR color (which OpenCV uses) to grayscale (which face_recognition uses)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Find all the faces in the current frame of video
    face_locations = face_recognition.face_locations(gray)

    # Display the results
    for face_location in face_locations:
        count = 0

        top, right, bottom, left = face_location
        box = (left, top, right, bottom)

        predictions = predict_smile(gray, box, count)

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        if np.argmax(predictions) == 0:
            cv2.putText(frame, f'NOT smiling', (left, top-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.60, (0, 0, 255), 2)
        else:
            cv2.putText(frame, f'smiling', (left, top-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.60, (0, 0, 255), 2)
        cv2.putText(frame, f'not_smile:{round(predictions[0][0],1)}, smile:{round(predictions[0][1],1)}', (left, bottom+30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.60, (0, 0, 255), 2)
        count += 1

    output_width = 720
    output_height = 480
    output_dim = (output_width, output_height)
    output_frame = cv2.resize(frame, output_dim, interpolation =cv2.INTER_AREA)

    # Display the resulting image
    cv2.imshow('are you smiling?', output_frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
cap.release()
cv2.destroyAllWindows()
