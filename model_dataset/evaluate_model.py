import matplotlib.pyplot as plt
import tensorflow as tf

# Load trained model
model = tf.keras.models.load_model("overstimulating_audio_detector.h5")


# Plot training history
def plot_training_history(history):
    plt.figure(figsize=(12, 5))

    # Accuracy plot
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Train Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()

    # Loss plot
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()

    plt.show()


# Load training history
import pickle

with open('training_history.pkl', 'rb') as f:
    history = pickle.load(f)

plot_training_history(history)
