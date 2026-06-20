from fpdf import FPDF

# Use FPDF with UTF-8 support
pdf = FPDF()
pdf.add_page()

# Set a Unicode font (must be TTF)
pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
pdf.set_font("DejaVu", "", 12)

# Title
pdf.set_font("DejaVu", "B", 16)
pdf.multi_cell(0, 10, "Bone Fracture Detection System Documentation", align='C')
pdf.ln(5)

# Content (exactly as you provided)
pdf.set_font("Arial", "", 12)
content = """
1. Project Overview
The Bone Fracture Detection System is an AI-powered application designed to detect fractures in bone X-ray images. The system uses deep learning for image classification and provides a detailed report for each uploaded X-ray image. The project also includes a web interface where users can upload images, view analysis results, and download reports.

Key Objectives:
- Detect fractured vs. non-fractured bones from X-ray images.
- Provide accurate reports with confidence scores and recommendations.
- Maintain a history of uploaded images and their analyses.
- Allow downloading reports for record-keeping.

2. Dataset
Dataset Source: Personal dataset of bone X-ray images.
Total images: ~64,000 images
Categories: Fractured, Not Fractured
Folder Structure:
dataset/
│
├── train/
│   ├── Fractured/
│   └── Not_Fractured/
├── val/
│   ├── Fractured/
│   └── Not_Fractured/
└── test/
    ├── Fractured/
    └── Not_Fractured/

Preprocessing:
- Images resized to 224x224 pixels.
- Pixel values normalized to [0,1].

3. Tools & Technologies
- Python 3.12
- TensorFlow, Keras
- PIL (Python Imaging Library)
- Flask, HTML, CSS
- VS Code / PyCharm
- GitHub
- Windows 10/11

4. Model Architecture
- Base Model: MobileNetV2 (pre-trained on ImageNet)
- Feature extraction: include_top=False
- Global Average Pooling layer
- Dropout (0.3) for regularization
- Dense layer with 2 outputs (softmax for classification)
- Compilation: Adam optimizer (learning_rate=1e-4), Categorical Crossentropy loss, Metrics: Accuracy, AUC
- Training: 10 epochs, batch size 32

5. Code Structure
Project Folder Layout:
Bone-Fracture-Detection/
├── dataset/            # X-ray images
├── model/              # Trained model
│   └── fracture_model.keras
├── static/             # Web static files (CSS, JS, uploads)
├── templates/          # HTML files for Flask
│   └── index.html
├── predict.py          # Prediction script
└── app.py              # Flask web app

5.1 predict.py
Handles image preprocessing, model loading, prediction, and generating a detailed report.
- Normalizes images
- Returns confidence scores
- Provides human-readable report with recommendations

5.2 app.py
Handles web interface:
- Upload X-ray images
- Display uploaded image and report
- Show previous uploads
- Download report (with images embedded)
- Dark theme interface

5.3 index.html
- Upload form
- Display section for uploaded image and report
- List previous uploads
- Responsive dark theme

6. Web App Features
- Upload Image: Users can upload X-ray images for analysis.
- Display Result: Shows image and AI-generated report.
- Previous Uploads: Maintains history of uploaded images and their reports.
- Download Report: Users can download a text file including:
  - Image (as Base64-encoded)
  - Prediction results
  - Confidence score
  - Recommendations

7. Code Explanation
7.1 Data Preparation
from tensorflow.keras.preprocessing.image import ImageDataGenerator
train_datagen = ImageDataGenerator(rescale=1.0/255.0)
val_datagen = ImageDataGenerator(rescale=1.0/255.0)
test_datagen = ImageDataGenerator(rescale=1.0/255.0)
train_gen = train_datagen.flow_from_directory(
    TRAIN_DIR, target_size=IMG_SIZE, batch_size=BATCH_SIZE, class_mode="categorical"
)

Explanation:
- ImageDataGenerator: Prepares images for the model.
- rescale=1.0/255.0: Normalizes pixel values (0–255) to (0–1).
- flow_from_directory: Reads images from folders and labels based on folder names.

7.2 Model Building
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models
base_model = MobileNetV2(weights="imagenet", include_top=False, input_shape=(224,224,3))
base_model.trainable = False
model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.3),
    layers.Dense(2, activation="softmax")
])

Explanation:
- MobileNetV2: Pre-trained AI model for feature extraction.
- include_top=False: Replace top layer with custom classifier.
- GlobalAveragePooling2D: Summarizes learned features.
- Dropout: Prevents overfitting.
- Dense(2, softmax): Output for Fractured/Not Fractured.

7.3 Compilation & Training
model.compile(
    optimizer=Adam(learning_rate=1e-4),
    loss="categorical_crossentropy",
    metrics=["accuracy", tf.keras.metrics.AUC(name="auc")]
)
history = model.fit(train_gen, validation_data=val_gen, epochs=10)

Explanation:
- Optimizer updates model weights.
- Categorical crossentropy used for classification.
- Accuracy and AUC metrics show model performance.

7.4 Saving & Loading Model
MODEL_PATH = "model/fracture_model.keras"
model.save(MODEL_PATH)
model = tf.keras.models.load_model(MODEL_PATH)

Explanation:
- Saves model for future predictions.
- Load model without retraining.

7.5 Prediction Function
def predict_xray(img_path):
    img = image.load_img(img_path, target_size=IMG_SIZE)
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array)
    class_index = np.argmax(prediction, axis=1)[0]
    confidence = prediction[0][class_index]
    if class_index == 0:
        label = "✅ Not Fractured"
    else:
        label = "🩻 Fractured"
    findings = f"Prediction: {label} (confidence: {confidence:.2f})"
    print(findings)

Explanation:
- Preprocess image same as training.
- np.argmax: Class with highest probability.
- Generates human-readable report.

7.6 Web App (Flask)
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))
            predict_xray(file.filename)
    return render_template("index.html")

Explanation:
- Upload image via browser.
- Saves image in static/uploads.
- Calls predict_xray to analyze.
- Shows uploaded image and report.
- Dark theme, previous uploads, downloadable report.

8. Project Workflow Diagram
Upload X-ray → Preprocess → AI Model Predicts → Report → Display on Web

9. Sample Outputs
1. Not Fractured Image
- Prediction: Not Fractured
- Confidence: 0.99
- Recommendation: Regular monitoring

2. Fractured Image
- Prediction: Fractured
- Confidence: 0.93
- Recommendation: Clinical confirmation

10. Conclusion
- Detect fractures automatically with high accuracy
- Supports doctors and patients
- Future: Multi-class fracture detection, mobile app, hospital integration
"""

pdf.set_font("DejaVu", "", 12)
pdf.multi_cell(0, 6, content)

# Save PDF
pdf_file = "Bone_Fracture_Detection_Documentation.pdf"
pdf.output(pdf_file)
print(f"✅ PDF generated successfully: {pdf_file}")
