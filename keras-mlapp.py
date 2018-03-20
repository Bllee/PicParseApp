#Borrows from GitHub Keras-Flask-Deploy-Webapp

import sys
import os
import glob
import re
import numpy as np

# Keras
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.wsgi import WSGIServer

#Webscraping
import requests, urllib, urllib.request #urllib sometimes results in 403 forbidden, try requests instead
from bs4 import BeautifulSoup
import os, tempfile #for file manipulation
from io import BytesIO #to open requests binary content

# Define a flask app
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
		errors = []
		images =[]
		parsedID =[]
		parsedClass = []
		if request.method == 'POST':
			urls = request.form['urls'].split(",")
			for url in urls:  # build list of image urls for display and image file names for classification
				url = url.strip()
				r = requests.get(url)
				data = r.text
				soup = BeautifulSoup(data, "html5lib")
				for img in soup.findAll('img'):
					src = img.get('src')
					src = urllib.parse.urljoin(url, src) #used to get full path when sites give relative paths.
					images.append(src)
					#parsedID.append(urllib.request.urlretrieve(src)[0]) 
					filebinary = requests.get(src)
					tmp = tempfile.NamedTemporaryFile(delete=False)
					path = tmp.name
					tmp.write(filebinary.content)
					parsedID.append(path)
					tmp.close()
					
			for	fn in parsedID:
				#print(fn)
				try:
					parsedClass.append(predict_it(fn))
				except:
					pass
				os.remove(fn) #delete tmp files
			results = list(zip(parsedClass, images))
			#urllib.request.urlcleanup() #clean up tempfiles from urlretrieve
			return render_template('parser.html', results=results, sites=urls)
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