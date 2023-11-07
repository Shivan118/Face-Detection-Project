import cv2, os, sys
from src.exception import FaceDetectionException
from src.logger import logging

class FaceDetectionImage:
    def __init__(self,image_path ):
        self.image_path = image_path

    
    def display_image(self) :
        try:
            
            # Create a CascadeClassifier Object
            face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

            # Black and White image (2 channels)
            img = cv2.imread(self.image_path) #  This line reads the image from the specified 

            # Will print shape of numpy array ie(426,500)
            resized_img = cv2.resize(img, (int(img.shape[1]*2),int(img.shape[0]*2)))

            # Reading image as gray scale image
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Search the coordinates of the image
            faces = face_cascade.detectMultiScale(gray_img , scaleFactor = 1.05, minNeighbors =5)

            # x and y are the coordinates of the top-left corner of a face, 
            # and w and h are the width and height of the face's bounding box.
            for x,y,w,h in faces:
                img = cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 3)


            # Opens a window to show image
            # Here People is name of window
            cv2.imshow("People", img)

            # Wait until user presses key
            cv2.waitKey(0)

            # closes the window based on waitkey parameter 
            cv2.destroyAllWindows()
        except Exception as e:
            sharing = FaceDetectionException(e,sys)
            logging.info(sharing.error_message)

