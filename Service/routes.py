# -*- coding: utf-8 -*-
import os
from Service import app
from flask import render_template, flash, redirect, request, url_for
from werkzeug.utils import secure_filename
from Service.forms import LinkForm
import json
from jsonschema import validate

ALLOWED_EXTENSIONS = {'json'}


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def route():
	return redirect('/home')

@app.route('/home', methods=['GET', 'POST'])
def home():
	return render_template('home.html', title='Home')

@app.route('/go')
def go():
	return redirect('/verify')

@app.route('/verify', methods=['GET', 'POST'])
def link():
	form = LinkForm()
	path = 'Service/schemas.json'
	with open(path, 'r') as f:
		schema = json.loads(f.read())
	#with open('Service/samples.json', 'r') as f:
		
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			redirect('/verify')
		file = request.files['file']
		# if user does not select file, browser also
		# submit an empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			#file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			#return redirect(url_for('uploaded_file', filename=filename))
		samples = json.loads(file.read())
		for sample in samples:
			try:
				validate(instance=sample, schema=schema)
				flash('Ok \n')
			except:
				flash('Error \n')
		return redirect('/index')
	return render_template('verify.html', title='Enter your json:', form=form)


@app.route('/index')
def index():
    return render_template('index.html', title='Results')
