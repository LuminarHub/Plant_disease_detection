import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .models import History

# -------------------- MODEL LOADING --------------------
MODEL_PATH = os.path.join(settings.BASE_DIR, 'prediction', 'Crop_disease.h5')

print("\n🚀 Django server starting — loading model...")
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print(f"✅ Model loaded successfully from: {MODEL_PATH}")
    print(f"🧠 Model input shape: {model.input_shape}")
except Exception as e:
    model = None
    print(f"❌ Model loading failed: {e}")

# -------------------- CLASS LABELS --------------------
class_labels = [
    "Apple Scab", "Apple Black Rot", "Apple Cedar Apple Rust", "Apple Healthy",
    "Blueberry Healthy", "Cherry (Including Sour) Powdery Mildew", "Cherry (Including Sour) Healthy",
    "Corn (Maize) Cercospora Leaf Spot Gray Leaf Spot", "Corn (Maize) Common Rust",
    "Corn (Maize) Northern Leaf Blight", "Corn (Maize) Healthy", "Grape Black Rot",
    "Grape Esca (Black Measles)", "Grape Leaf Blight (Isariopsis Leaf Spot)", "Grape Healthy",
    "Orange Haunglongbing (Citrus Greening)", "Peach Bacterial Spot", "Peach Healthy",
    "Pepper Bell Bacterial Spot", "Pepper Bell Healthy", "Potato Early Blight", "Potato Late Blight",
    "Potato Healthy", "Raspberry Healthy", "Soybean Healthy", "Squash Powdery Mildew",
    "Strawberry Leaf Scorch", "Strawberry Healthy", "Tomato Bacterial Spot", "Tomato Early Blight",
    "Tomato Late Blight", "Tomato Leaf Mold", "Tomato Septoria Leaf Spot",
    "Tomato Spider Mites Two-Spotted Spider Mite", "Tomato Target Spot",
    "Tomato Yellow Leaf Curl Virus", "Tomato Tomato Mosaic Virus"
]

# -------------------- PREDICTION VIEW --------------------
def predict_disease(request):
    """Allows prediction even for anonymous users. Saves history only for logged-in users."""
    print("\n➡️ Entered predict_disease view")
    print("Request method:", request.method)

    label = None
    confidence = None
    image_url = None

    if request.method == 'POST':
        print("📨 POST request detected.")
        print("FILES received:", request.FILES)

        if 'image' not in request.FILES:
            print("⚠️ No image uploaded.")
            messages.error(request, "⚠️ No image selected. Please choose a file.")
            return redirect('prediction')

        uploaded_image = request.FILES['image']

        if not model:
            print("❌ Model not loaded.")
            messages.error(request, "⚠️ Model not loaded. Please check configuration.")
            return redirect('prediction')

        try:
            print(f"📸 File received: {uploaded_image.name}")

            # Save only if user is logged in
            if request.user.is_authenticated:
                print("👤 User authenticated, saving to History model.")
                history_entry = History.objects.create(
                    user=request.user,
                    image=uploaded_image,
                    disease_name='Pending',
                    confidence=0.0
                )
                img_path = history_entry.image.path
            else:
                print("👥 Anonymous user — saving image temporarily.")
                from django.core.files.storage import default_storage
                temp_path = os.path.join(settings.MEDIA_ROOT, 'temp', uploaded_image.name)
                os.makedirs(os.path.dirname(temp_path), exist_ok=True)
                with default_storage.open(temp_path, 'wb+') as f:
                    for chunk in uploaded_image.chunks():
                        f.write(chunk)
                img_path = temp_path

            # Detect input size
            input_shape = model.input_shape[1:3]
            print(f"🧠 Model expects input shape: {input_shape}")

            # Preprocess image
            img = image.load_img(img_path, target_size=input_shape)
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0) / 255.0

            # Predict
            print("🔍 Running prediction...")
            predictions = model.predict(img_array)
            predicted_index = np.argmax(predictions)
            confidence = float(np.max(predictions)) * 100
            label = class_labels[predicted_index]
            print(f"✅ Prediction successful: {label} ({confidence:.2f}%)")

            # Save results if logged in
            if request.user.is_authenticated:
                history_entry.disease_name = label
                history_entry.confidence = confidence
                history_entry.save()
                print("💾 Prediction saved to history.")

            # For display
            image_url = (
                history_entry.image.url
                if request.user.is_authenticated
                else f"/media/temp/{uploaded_image.name}"
            )

            messages.success(request, f"✅ Prediction: {label} ({confidence:.2f}%)")

        except Exception as e:
            print("❌ Prediction error:", e)
            messages.error(request, f"Prediction failed: {e}")

    return render(request, 'prediction/disease_prediction.html', {
        'label': label,
        'confidence': confidence,
        'image_url': image_url,
    })

# -------------------- HISTORY VIEW --------------------
def prediction_history(request):
    """Shows history only for logged-in users."""
    print("\n➡️ Entered prediction_history view")
    if not request.user.is_authenticated:
        print("⚠️ Anonymous user trying to access history.")
        messages.warning(request, "⚠️ Login required to view history.")
        return redirect('prediction')

    user_history = History.objects.filter(user=request.user).order_by('-created_at')
    print(f"📜 Found {len(user_history)} history records for {request.user}.")
    return render(request, 'prediction/history.html', {'history': user_history})
