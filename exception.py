from flask import Flask
from src.logger import logging
from src.exception import FaceDetectionException
import sys

app = Flask(__name__)

#/shivan -> localhost:5000/shivan
# / -> localhost:5000
@app.route('/', methods = ['GET', 'POST'])
def index():

    try:
        
        raise Exception('We are testing our cutom exception file')

    except Exception as e:
        test = FaceDetectionException(e, sys)

        logging.info(test.error_message)


        logging.info('We are testing our logging file')

        return "Face Detection project Implementation for Exception"

if __name__ == '__main__':
    app.run(debug=True)# 5000