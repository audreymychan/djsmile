# djsmile <img src="./static/images/dad_black.png" alt="Dad black icon" width="30"/>

> Smile detection app based on deep learning CNN models and a pinch of dad jokes

**djsmile** is a Flask-powered web application to showcase a smile detection algorithm trained using convolutional neural networks. It takes input from a user's webcam and returns predictions on how much they're smiling! It also provides random dad jokes from *icanhazdadjoke*'s API for fun, because why not. 

#### Motivation
Motivation came from a previous program I wrote to detect smiles 7 years ago, where the algorithm was based on my naive knowledge of what it means for someone to be smiling. For example, I detected the mouth using edge detection then identified smiles based on color pixel changes (red vs white). 

#### Problem
Of course, this was highly sensitive to noise (i.e. lighting, face orientation, etc). Now we can simply use machine learning to do a better job and remove human bias! CNNs can find new variables we didn't even know matter and their weights to improve our model. Hypothetically, it might determine how much ones's crow's feet around the eye impact smile predictions?

## Demo Video
Click the screenshot below to see a demo.

[![App screen recording](https://img.youtube.com/vi/g3G3tXIf4fk/0.jpg)](https://www.youtube.com/watch?v=g3G3tXIf4fk)

## Process

### <img src="./static/images/scraper.png" alt="scraper" width="30"/> Web Scraping
Total of 8,600 images were scraped from Getty Images based on searches for "smile" and "no smile".

Refer to `getty_scraping.py`

Tools used: `requests`, `BeautifulSoup`

### <img src="./static/images/edit.png" alt="edit" width="30"/> Image Pre-processing
Images collected were then:
- cropped with a bounding box around faces detected
- converted to grayscale
- resized down to 100 x 100 px
- convert into an array
- normalized

Refer to `cnn_model_training.ipynb`

Tools used: `PIL` - Image, `face_recognition`, `tensorflow.keras` - array_to_img, img_to_array, ImageDataGenerator, to_categorical, `sklearn` - MinMaxScaler, LabelEncoder, train_test_split

### <img src="./static/images/training.png" alt="training" width="30"/> Convolutional Neural Network (CNN)
A convolutional neural network model was trained using the images.

Refer to `cnn_model_training.ipynb` for layers and weights used

Tools used: `tensorflow.keras` - Sequential, Input, Conv2D, MaxPooling2D, Dropout, Dense, Flatten, EarlyStopping

### <img src="./static/images/save.png" alt="save" width="30"/> Saving the Model
The CNN model and weights learned were saved and can be used to predict smile versus no smile on any new image coming from the app. The model was saved under `my_model.h5` and MinMaxScaler under `scaler.save`.

Refer to `cnn_model_training.ipynb`

Tools: `sklearn` - joblib, `tensorflow.keras` - save, load_model

### <img src="./static/images/internet.png" alt="internet" width="30"/> Flask App
The app can be generated with the following files:
- `app.py`: main application to run
- `camera.py`: contains Camera object to capture live video feed and `get_frame()` function return image with a bounding box marked around the face and text indicating smile probabilities
- `generate_joke.py`: contains `get_joke()` function to access *icanhazdadjoke*'s API and return a random generated joke
- `smile_recognition.py`: contains `predict_smile()` function which takes in an image frame and returns smile predictions

## Future Work
- Publish the app online

*Keep smiling.. it makes people wonder what you are up to.*
