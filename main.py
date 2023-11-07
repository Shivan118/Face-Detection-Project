import os
import streamlit as st
from werkzeug.utils import secure_filename
from src.logger import logging
from src.exception import FaceDetectionException
from src.components.face_detect_image import FaceDetectionImage
from src.components.face_detect_webcam import FaceDetectionWebcam

if not os.path.exists('uploads'):
    os.makedirs('uploads')

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'uploads'

# abc.jpg
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_image(uploaded_file):
    upload_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    filename = secure_filename(uploaded_file.name)
    file_path = os.path.join(upload_dir, filename)

    with open(file_path, 'wb') as f:
        f.write(uploaded_file.read())

    return file_path


def main():
    st.title('Face Detection Application')

    page = st.selectbox("Choose a page", ["Home", "Upload Image", "Webcam"])

    if page == "Home":
        st.write("Welcome to the Face Detection Application!")

    if page == "Upload Image":
        st.write("Upload an image and detect faces:")
        uploaded_file = st.file_uploader("Choose an image...", type=['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

        if uploaded_file is not None:
            if allowed_file(uploaded_file.name):
                st.image(uploaded_file, use_column_width=True, caption='Uploaded Image')

                # Perform face detection on the uploaded image
                if st.button("Detect Faces"):
                    try:
                        image_path = save_uploaded_image(uploaded_file)
                        face_detect_obj = FaceDetectionImage(image_path=image_path)
                        detected_image = face_detect_obj.display_image()
                        st.image(detected_image, use_column_width=True, caption='Detected Faces')
                        st.success("Faces successfully detected!")
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
            else:
                st.error("Invalid file format. Please upload an image.")

    if page == "Webcam":
        st.write("Click the button below to trigger the webcam:")
        if st.button("Trigger Webcam"):
            try:
                face_detect_web_obj = FaceDetectionWebcam()
                face_detect_web_obj.load_camera()
                st.success("Faces successfully detected!")
                st.write("To quit the webcam window, press 'q'.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()