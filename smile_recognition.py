from sklearn.externals import joblib
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, array_to_img
from PIL import Image
import numpy as np

# set new frame size dimensions
img_width, img_height = (100, 100)

# scaler and model imports
scaler = joblib.load('scaler.save')
model = load_model('my_model.h5')
model.compile(loss = 'binary_crossentropy', optimizer = 'adam', metrics = ['accuracy'])

def predict_smile (gray_img, box, count):
    # save a copy of current frame
    gray_img = gray_img.reshape(gray_img.shape+(1,))
    array_to_img(gray_img).save(f'current_frame{count}.jpg')

    # load image (with face cropped) into a numpy array
    gray_img = Image.open(f'current_frame{count}.jpg')
    face_crop = gray_img.resize((img_width, img_height), box = box)
    face_crop.save(f'face_crop_current_frame{count}.jpg')
    face_crop = Image.open(f'face_crop_current_frame{count}.jpg')
    new_face_array = np.array(img_to_array(face_crop))

    new_face_array = new_face_array.reshape(1, img_width*img_height)

    new_face_array = scaler.transform(new_face_array)
    new_face_array = new_face_array.reshape(1, img_width, img_height, 1)

    return model.predict(new_face_array)
