#from YouTube:  https://www.youtube.com/watch?v=zRwy8gtgJ1A
#uses Bootstrap CDN for CSS and JavaScript:  https://www.bootstrapcdn.com/
from flask import Flask, render_template, flash, request, url_for, redirect
from wtforms import Form, StringField, TextField, TextAreaField, SubmitField, validators
import requests
from bs4 import BeautifulSoup
import webbrowser
import urllib.parse
###To do:  put results in image grid; parse pictures for nonpro stuff
app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def index():
		errors = []
		images =[]
		if request.method == 'POST':
			try:
				urls = request.form['urls'].split(",")
				for url in urls:
					r = requests.get(url)
					data = r.text
					soup = BeautifulSoup(data, "html5lib")
					for img in soup.findAll('img'):
						src = img.get('src')
						src = urllib.parse.urljoin(url, src) #used to get full path when sites give relative paths.
						images.append(src)
						#print(images)
					'''for img in images:
						webbrowser.open_new_tab(img)'''
					#print(r.text)
					#webbrowser.open_new_tab(url)
					#print(images)
					
			except:
				errors.append("Invalid URL.  Please try again.")
		return render_template('index.html') #, errors=errors, results=images)


@app.route('/about')
def about():
	return render_template('about.html')

#Not sure this is needed anymore
'''class SubmissionForm(Form):
	site = StringField('URL', [validators.URL(require_tld=True, message="Please enter a valid URL.")])

@app.route('/parser', methods=['GET','POST'])
def parseForm():
	form = SubmissionForm(request.form)
	if request.method == 'POST' and form.validate():
		return render_template('parser.html', form=form)
	else: 
		return render_template('index.html')
	if request.method == 'POST':
		site = request.form['website']
		return render_template('success.html')
	
	return render_template('index.html')'''

	
		

	

if __name__ == '__main__':
	app.run(debug=True) #put debug to avoid restarting server each time during testing