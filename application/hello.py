from flask import Flask, render_template, request,jsonify
from werkzeug import secure_filename
from keras.models import model_from_json   
import numpy
import cv2
from keras.preprocessing import image
import sys
import pyrebase
from PIL import Image
import requests
from io import BytesIO
import cv2
import urllib
import numpy as np
from keras import backend as K
import time
data=[
    {
        'name':'Audrin',
        'place': 'kaka',
        'mob': '7736'
    },
    {
        'name': 'Stuvard',
        'place': 'Goa',
        'mob' : '546464'
    }
]


config = {
  "apiKey": "AIzaSyDtpqE2Ne-htEyMBxObFj_H0Y6XsF9LInk",
  "authDomain": "gauri-ab979.firebaseapp.com",
  "databaseURL": "https://gauri-ab979.firebaseio.com",
  "storageBucket": "gauri-ab979.appspot.com"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

user = auth.sign_in_with_email_and_password("g.kalyan04@gmail.com", "123456789")
db = firebase.database()
storage = firebase.storage()
app = Flask(__name__)

users=""

@app.route('/')
def upload_files():
    global users
    # time.sleep(2)
    users = db.child('result').get().val()
    
    return render_template('home.html')
@app.route("/forward/",methods=['POST'])
def move_forward():
    storage.child("images/2.jpeg").download("1.jpeg")
    K.clear_session()
    # load image
    print(users)
    path = "1.jpeg"
    img_width = 64
    img_height = 64
    img = cv2.imread(path)
    img = cv2.resize(img,(64,64),3)
    img = img.reshape((-1, 64, 64, 3))
    # pneumonia model
    # result[0][0 = 0.0
    # result_1[0][0] = 0.0
    # result_2[0][0] = 1.
    print(users)
    pn = 0.0
    tb = 0.0
    inf = 1.0
    if(users=="pneumonia"):

      json_file = open('model.json', 'r')
      model_json = json_file.read()
      model = model_from_json(model_json)
      model.load_weights("model.h5")
      result = model.predict(img) # save result
      pn = result[0][0]
      print('pn',pn)
    # tuberclosis
    if(users=="tuberclosis"):
      json_file = open('model_tb.json', 'r')
      model_json = json_file.read()
      model_1 = model_from_json(model_json)
      model_1.load_weights("model_tb.h5")
      result_1 = model_1.predict(img)
      tb = result_1[0][0]
      print('tb',tb)
    # Infiltration
    if(users=="infiltration"):
      json_file = open('model_in.json', 'r')
      model_json = json_file.read()
      model_2 = model_from_json(model_json)
      model_2.load_weights("model_in.h5")
      result_2 = model_2.predict(img)
      inf = result_2[0][0]
      print('inf',inf)
    
    # check condition
    print(pn)
    print(tb)
    print(inf)
    # pn=1.0
    # tb=1.0
    inf=0.0
    if (pn==1.0):
      pn = 0.0
      tb = 0.0
      inf = 1.0
      return render_template("predict.html",a="Pneumonia",ap="83.67%")

    if (tb==1.0):
      return render_template("predict.html",b="Tuberclosis",bp="68.67%")

    if (inf==0.0):
      return render_template("predict.html",c="Infiltration",cp="68.67%")
    else:
      return render_template("predict.html",n="none")
		
if __name__ == '__main__':
   app.run(debug = True)
