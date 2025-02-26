import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import VGG16
from tensorflow.keras import layers, models
import os
import pickle  # Import pickle to save training history

# Define dataset path
dataset_path = "C:/Akira/modify-audio/model_dataset"
train_dir = os.path.join(dataset_path, "train")
val_dir = os.path.join(dataset_path, "val")

# Image preprocessing
train_datagen = ImageDataGenerator(rescale=1.0/255)
val_datagen = ImageDataGenerator(rescale=1.0/255)

train_generator = train_datagen.flow_from_directory(
    train_dir, target_size=(224, 224), batch_size=32, class_mode='binary'
)

val_generator = val_datagen.flow_from_directory(  # Use separate generator for validation
    val_dir, target_size=(224, 224), batch_size=32, class_mode='binary'
)

# Load VGG16 model
base_model = VGG16(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
for layer in base_model.layers[:-4]:
    layer.trainable = False

# Build the model
model = models.Sequential([
    base_model,
    layers.Flatten(),
    layers.Dense(256, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Train the model
history = model.fit(train_generator, epochs=20, validation_data=val_generator)

# Save the model
model.save("overstimulating_audio_detector.h5")
print("Model training completed and saved!")

# ✅ Save training history
with open("training_history.pkl", "wb") as f:
    pickle.dump(history.history, f)
print("Training history saved!")
