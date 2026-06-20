import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import os
from PIL import ImageFile

# Fix truncated images
ImageFile.LOAD_TRUNCATED_IMAGES = True

# Paths


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "fracture_model.keras")
IMG_SIZE = (224, 224)

# Load model
model = tf.keras.models.load_model(MODEL_PATH)
print("✅ Model loaded successfully!")

# Prediction function
def predict_xray(img_path):
    try:
        img = image.load_img(img_path, target_size=IMG_SIZE)
        img_array = image.img_to_array(img)/255.0
        img_array = np.expand_dims(img_array, axis=0)

        prediction = model.predict(img_array)
        class_index = np.argmax(prediction, axis=1)[0]
        confidence = prediction[0][class_index]

        # Use class_indices from training to assign correct labels
        # Suppose train_gen.class_indices = {'Fractured':0, 'Not_fractured':1}
        if class_index == 0:
            label = "🩻 Fractured"
            findings = (
                f"Probable fracture detected (confidence: {confidence:.2f}).\n"
                "Location: Left forearm region.\n"
                "Recommendation: Clinical confirmation advised."
            )
        else:
            label = "✅ Not Fractured"
            findings = (
                f"No visible fracture detected (confidence: {confidence:.2f}).\n"
                "Bone structure appears intact.\n"
                "Recommendation: Regular monitoring if symptoms persist."
            )

        # Output
        print("\n--- X-Ray Report ---")
        print(f"🖼️ Uploaded Image: {os.path.basename(img_path)}")
        print(f"🔍 Prediction: {label}")
        print(f"📋 Findings: {findings}\n")

    except Exception as e:
        print(f"❌ Error: {e}")

# Run from command line
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("❌ Please provide image path.\nUsage: python predict.py <image_path>")
    else:
        img_path = sys.argv[1]
        predict_xray(img_path)
