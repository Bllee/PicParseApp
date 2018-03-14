#from YouTube:  https://www.youtube.com/watch?v=zRwy8gtgJ1A
#uses Bootstrap CDN for CSS and JavaScript:  https://www.bootstrapcdn.com/
#This is the local copy.  The PythonAnywhere copy is called flask_app.py
##To Do List
##User entry error handling and picture format error handling (currently just PASS)
##Need better picture pre-formatting before feeding into model. Currently chokes frequently (OpenCV assertion failed error)
##Error messages if user enters bad URL
##Enhance UI so parsed photos return in table format with:  site url, image url, image thumbnail, image caption
##Train new model for better accuracy.

print ("Loading libraries....")
from flask import Flask, render_template, flash, request, url_for, redirect
#from wtforms import Form, StringField, TextField, TextAreaField, SubmitField, validators (for future refinements)
import requests, urllib, urllib.request #urllib sometimes results in 403 forbidden, try requests instead
from bs4 import BeautifulSoup
from gevent.wsgi import WSGIServer #won't work with default flask run app
import os, tempfile #for file manipulation
from io import BytesIO #to open requests binary content

# ### Ensure you have the correct kernel running (activate conda env) and that you set PYTHONPATH=PathToFastAIFolder
# Example `set PYTHONPATH=D:\Documents\GitHub\fastai`

#import the FastAI libraries
from fastai.imports import *
from fastai.transforms import *
from fastai.conv_learner import *
from fastai.model import *
from fastai.dataset import *
from fastai.sgdr import *
from fastai.plots import *


##Configure, train and load fastai model
print ("Updating model....")
### Some basic model configuration.  Arch and sz need to match what was used to train, as does data path
arch = resnet34
sz=224 
PATH = "D:/Documents/GitHub/SkollMachines/picparse"

### Loading and using the previously saved model
## We're going to assume you've already trained your model. You now need to set up a simple learner so you can load it in. You can't avoid this initial "dummy" training, but it should go fast. The important thing is you have to have your data available. You also need to use the same architecture as the one you used for training your model.
data = ImageClassifierData.from_paths(PATH, tfms=tfms_from_model(arch, sz)) #, bs=64) #bs is batch size if needed; assumes 1 batch
learn = ConvLearner.pretrained(arch, data, precompute=False) #leave precompute as False if you plan to load a saved model


## Also need to do a training augmentation, otherwise you'll get an error 
log_preds,y = learn.TTA()
probs = np.mean(np.exp(log_preds),0)

##load the pretrained model
learn.load('d:/Documents/GitHub/SkollMachines/picparse_model') 

print("Ready to parse!")

##The function. Taken from fastAI course.
##predicts class of image based on currently trained model
##takes image name as input (will need full path also)
def predict_it(fn):
	#fn = BytesIO(fn)
	trn_tfms, val_tfms = tfms_from_model(arch, sz) # get transformations
	im = val_tfms(open_image(fn))
	learn.precompute=False #passing in raw image, not activations
	preds = learn.predict_array(im[None]) #have to pass in None because expects different sized tensor than 3D
	
	return data.classes[np.argmax(preds)]
'''
    # preds are log probabilities of classes, argmax gives the number, which is also index of data.class. Assumes data.
    return data.classes[np.argmax(preds)] '''


##Start Flask
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