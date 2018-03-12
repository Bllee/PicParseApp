#from YouTube:  https://www.youtube.com/watch?v=zRwy8gtgJ1A
#uses Bootstrap CDN for CSS and JavaScript:  https://www.bootstrapcdn.com/
#This is the local copy.  The PythonAnywhere copy is called flask_app.py
##To Do List
##Fix refresh issue so old data clears
##Fix url grab to handle all picture formats (ignoring javescript pages for now because: demo!)
##User entry error handling.
##Import parsing code with model and configure (I'm dreading this)
##Enhance UI so parsed photos return in table format with:  site url, image url, image thumbnail, image caption

from flask import Flask, render_template, flash, request, url_for, redirect
#from wtforms import Form, StringField, TextField, TextAreaField, SubmitField, validators (for future refinements)
import requests
from bs4 import BeautifulSoup
import urllib.parse

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
		errors = []
		images =[]
		if request.method == 'POST':
			urls = request.form['urls'].split(",")
			for url in urls:
				r = requests.get(url)
				data = r.text
				soup = BeautifulSoup(data, "html5lib")
				for img in soup.findAll('img'):
					src = img.get('src')
					src = urllib.parse.urljoin(url, src) #used to get full path when sites give relative paths.
					images.append(src)
			return render_template('parser.html', results=images, sites=urls)
		return render_template('index.html')
	


@app.route('/about')
def about():
	return render_template('about.html')
	
@app.route('/parser')
def parser():
	return render_template('parser.html')

	

	

if __name__ == '__main__':
	app.run(debug=True) #put debug to avoid restarting server each time during testing