# -*- coding: UTF-8 -*-

#Borrows from GitHub Keras-Flask-Deploy-Webapp
#see also https://blog.keras.io/index.html


# Keras
from keras.models import load_model
from keras import optimizers
from keras.preprocessing import image
import numpy as np

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.wsgi import WSGIServer

#Webscraping
import requests, urllib, urllib.request #urllib sometimes results in 403 forbidden, try requests instead
from bs4 import BeautifulSoup
import os, tempfile #for file manipulation
import concurrent.futures 
import time

image_bucket =[]
site_url =[]
tmp_image_path = []
predictions =[]

print ("Loading and compiling model...")
#Load and compile Keras model
#MUST use EXACTLY same configuration (incl. dependencies) as in training
#otherwise it won't load
model = 'res_better_layers.h5' #Classes 0 Bombers, 1 Missiles, 2 Other, 3 Submarines
model = load_model(model)
model.compile(loss='categorical_crossentropy',
              optimizer=optimizers.RMSprop(lr=1e-4),
              metrics=['acc'])
print ("Model loaded.")

#Keras predictor
def predict_it(image_name):
    #preprocesses images to same set-up as in model, then uses model to predict class
    img = image.load_img(image_name, target_size=(224, 224)) #use same size as in training
    my_tensor = image.img_to_array(img) # convert image to tensor (height, width, channels)
    my_tensor = np.expand_dims(my_tensor, axis=0) # add 1 dimension because model expects (samples, height, width, channels)
    my_tensor = my_tensor/255 #normalize to between 0-1
    
    prediction = model.predict_classes(my_tensor) #model.predict will return softmax probabilities
    #predictions.append(prediction[0])
    return prediction[0] #use indexing to return actual number, not list of number

#Image grabber. Makes list of image src links.
def get_it(url):
    try:
        url = url.strip()
        r = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data, "html5lib")
        for img in soup.findAll('img'):
            src = img.get('src')
            src = urllib.parse.urljoin(url, src) #used to get full path when sites give relative paths.
            if ".jpg" in src:
                image_bucket.append(src)
            elif ".jpeg" in src:
                image_bucket.append(src)
            elif ".svg" in src:
                image_bucket.append(src)
            elif ".png" in src:
                image_bucket.append(src)
            elif ".gif" in src:
                image_bucket.append(src)
                
            site_url.append(url)
    except:
        pass

#Temp save of images to disk for passing to classifier        
def save_it(src):

    parsed_path=[]
    filebinary = requests.get(src)
    tmp = tempfile.NamedTemporaryFile(delete=False)
    path = tmp.name
    tmp.write(filebinary.content)
    parsed_path.append(path)
    tmp_image_path.append(path)
    
    tmp.close()

    return parsed_path

# Define a flask app
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
        #siteurl = []
        #images =[]
        #got_it =[] #container for website images
        classified = []
        if request.method == 'POST':
            start = time.time()
            urls = request.form['urls'].split(",")
            with concurrent.futures.ThreadPoolExecutor() as executor1:
                print("Starting executor1")
                executor1.map(get_it, urls)

            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor2:
                print("Starting executor2")
                result2 = executor2.map(save_it, image_bucket)


            for item in result2:
                try: 
                    classified.append(predict_it(item[0]))
                except:
                    pass
                os.remove(item[0]) #clean up temp files
            
            full_results = list(zip(site_url, classified, image_bucket)) #List of site_url, class, image src
            parsed_results = [item for item in full_results if item[1]!=2]
            print("Elapsed time: " , time.time()-start)
            #urllib.request.urlcleanup() #clean up tempfiles from urlretrieve
            return render_template('parser.html', results=parsed_results, full_results=full_results)
        return render_template('index.html')
    

@app.route('/about')
def about():
    return render_template('about.html')
    
@app.route('/parser')
def parser():
    return render_template('parser.html')



if __name__ == '__main__':
    #app.run(debug=True) #put debug to avoid restarting server each time during testing
    
    #Serve with gevent
    http_server = WSGIServer(('',5000), app)
    http_server.serve_forever()
