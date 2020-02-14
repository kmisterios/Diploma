# -*- coding: utf-8 -*-
import os
from Service import app
from flask import render_template, flash, redirect, request, url_for
from werkzeug.utils import secure_filename
from Service.forms import LinkForm
import json
from jsonschema import validate
import numpy as np
from cpd import cpd_count
from generator import  error1, error2, error3, error4, error5

ALLOWED_EXTENSIONS = {'json'}



def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def route():
	return redirect('/home')

@app.route('/home', methods=['GET', 'POST'])
def home():
	form = LinkForm()
	n = 30
	if request.method == 'POST':
		type_of_error = int(form.link.data)
		if type_of_error == 1:
			error1(n)
		if type_of_error == 2:
			error2(n)
		if type_of_error == 3:
			error3(n)
		if type_of_error == 4:
			error4(n)
		if type_of_error == 5:
			error5(n)
		return redirect('/verify')
	return render_template('home.html', title='Home', form = form)

@app.route('/go')
def go():
	return redirect('/verify')

@app.route('/verify', methods=['GET', 'POST'])
def link():
	path = 'Service/schemas.json'
	with open(path, 'r') as f:
		schema = json.loads(f.read())
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
			return redirect('/verify')
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
		samples = json.loads(file.read())
		num_err = 0
		for sample in samples:
			try:
				validate(instance=sample, schema=schema)
				flash('Ok \n')
			except:
				num_err += 1
				flash('Error \n')
		# if there are errors in schemas, it's no reason to continue tests
		if num_err > 0 :
			return redirect('/index')
		# let's try change point detection
		result_num, type_num = cpd_count(samples, schema, "number")
		result_len_str = cpd_count(samples, schema, "string")
		result_len_arr = cpd_count(samples, schema, "array")
		result_item_count = cpd_count(samples, schema, "item")
		for result, ttype in np.array([result_num, type_num]).T:
			if (ttype == np.float64 and len(result) == 1) or (ttype == np.int64 and len(result)- int(result[-1]/5)
			 + int(result[-1] % 5 in {1,2}) == 1):
				flash('No anomaly \n')
			else:
				flash('Anomaly \n')
		for result in result_len_str:
			#print(len(result)- int(result[-1]/5) + int(my_bkps[-1] % 5 in {1,2}), result)
			if len(result)- int(result[-1]/5) + int(result[-1] % 5 in {1,2}) == 1:
				flash('No anomaly \n')
			else:
				flash('Anomaly \n')
		for result in result_len_arr:
			if len(result)- int(result[-1]/5) + int(result[-1] % 5 in {1,2}) == 1:
				flash('No anomaly \n')
			else:
				flash('Anomaly \n')
		if len(result_item_count) - int(result_item_count[-1] / 5) + int(result_item_count[-1] % 5 in {1, 2}) == 1:
			flash('No anomaly \n')
		else:
			flash('Anomaly \n')
		return redirect('/index')
	return render_template('verify.html', title='Enter your json:')


@app.route('/index')
def index():
    return render_template('index.html', title='Results')
