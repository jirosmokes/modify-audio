import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

# Load the trained model
model = tf.keras.models.load_model("audio-detector.h5")

# Function to predict a new image
def predict_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    return "Overstimulating" if prediction[0][0] > 0.5 else "Non-Overstimulating"

# Test on a sample image
test_image_path = "test-data/test-spectro-2.png"
result = predict_image(test_image_path)
print(f"Prediction: {result}")
