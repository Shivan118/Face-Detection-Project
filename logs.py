from flask import Flask
from src.logger import logging

app = Flask(__name__)

#/shivan -> localhost:5000/shivan
# / -> localhost:5000
@app.route('/', methods = ['GET', 'POST'])
def index():

    logging.info('We are testing our logging file')

    return "Face Detection project Implementation"

if __name__ == '__main__':
    app.run(debug=True)# 5000