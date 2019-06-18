# This script loads the pre-trained scaler and models and contains the
# predict_smile() function to take in an image and return smile predictions

import joblib
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, array_to_img
from PIL import Image
import numpy as np

# Set new frame size dimensions
img_width, img_height = (100, 100)

# Scaler and model imports
scaler = joblib.load('scaler.save')
model = load_model('my_model.h5')
model.compile(loss='binary_crossentropy', optimizer='adam',
              metrics=['accuracy'])


def predict_smile(gray_img, box, count):
    """Make prediction on a new image whether a person is smiling or not.

    Parameters
    ----------
    gray_img : numpy.ndarray of dtype int
        Grayscale image in numpy.ndarray of current frame.
    box : tuple
        (left, top, right, bottom) locating face bounding box in pixel locations.
    count : int
        Number of faces detected in current frame.

    Returns
    -------
    numpy.ndarray of dtype float
        Probabilities of no smile (second number) and smile (first number).
        i.e. array([[0.972528  , 0.02747207]], dtype=float32)

    """

    # Save a copy of current frame
    gray_img = gray_img.reshape(gray_img.shape+(1,))  # (height, width, 1)
    array_to_img(gray_img).save(f'./images/temp/current_frame_{count}.jpg')

    # Load image
    gray_img = Image.open(f'./images/temp/current_frame_{count}.jpg')

    # Crop face, resize to 100x100 pixels, and save a copy
    face_crop = gray_img.resize((img_width, img_height), box=box)
    face_crop.save(f'./images/temp/face_crop_current_frame_{count}.jpg')

    # Load image and convert to np.array
    face_crop = Image.open(f'./images/temp/face_crop_current_frame_{count}.jpg')
    new_face_array = np.array(img_to_array(face_crop))  # (100, 100, 1)

    # Reshape
    new_face_array = new_face_array.reshape(1, img_width*img_height)  # (1, 10_000)

    # Transform with pre-trained scaler
    new_face_array = scaler.transform(new_face_array)
    new_face_array = new_face_array.reshape(1, img_width, img_height, 1)  # (1, 100, 100, 1)

    return model.predict(new_face_array)
