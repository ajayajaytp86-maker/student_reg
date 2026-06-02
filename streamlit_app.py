import streamlit as st
import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import pandas as pd

st.set_page_config(
    page_title="AI Vision Dashboard",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Advanced AI Vision Dashboard")
st.markdown(
    "Upload an image to run object detection, face detection, and image classification with a single AI-powered dashboard."
)

uploaded_file = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"]
)

@st.cache_resource
def load_models():
    yolo = YOLO("yolov8n.pt")
    mobilenet = MobileNetV2(weights="imagenet")
    return yolo, mobilenet

if uploaded_file:
    with st.spinner("Loading AI models and analyzing image..."):
        yolo_model, mobilenet_model = load_models()

        img = Image.open(uploaded_file).convert("RGB")
        img_np = np.array(img)

        col1, col2 = st.columns(2)
        with col1:
            st.image(img, caption="Original Image", use_column_width=True)

        # Object detection
        results = yolo_model(img_np)
        detected_objects = []
        annotated = img_np.copy()

        for r in results:
            boxes = r.boxes
            for box in boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                label = yolo_model.names[cls]
                detected_objects.append({"Object": label, "Confidence": round(conf * 100, 2)})
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(
                    annotated,
                    f"{label} {conf:.2f}",
                    (x1, max(y1 - 10, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2,
                )

        with col2:
            st.image(annotated, caption="Object Detection Result", use_column_width=True)

        st.markdown("---")
        st.subheader("📊 Detected Objects")
        if detected_objects:
            df = pd.DataFrame(detected_objects)
            st.dataframe(df)
        else:
            st.info("No objects detected in the image.")

        # Image classification
        resized = img.resize((224, 224))
        arr = image.img_to_array(resized)
        arr = np.expand_dims(arr, axis=0)
        arr = preprocess_input(arr)
        preds = mobilenet_model.predict(arr)
        decoded = decode_predictions(preds, top=5)[0]

        st.subheader("🧠 Image Classification")
        for _, label, score in decoded:
            st.write(f"**{label}** : {score * 100:.2f}%")

        # Face detection
        st.markdown("---")
        st.subheader("🙂 Face Detection")
        face_img = img_np.copy()
        gray = cv2.cvtColor(face_img, cv2.COLOR_RGB2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        for (x, y, w, h) in faces:
            cv2.rectangle(face_img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        st.image(face_img, caption="Face Detection Result", use_column_width=True)
        st.success(
            f"Analysis completed | Objects found: {len(detected_objects)} | Faces found: {len(faces)}"
        )

else:
    st.info("Upload a JPG or PNG image to start AI vision analysis.")
    st.write(
        "This dashboard uses YOLOv8 for object detection, MobileNetV2 for image classification, and OpenCV for face detection."
    )
