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
from generator import  error1, error2, error3, error4, error5, noErrors
import random

ALLOWED_EXTENSIONS = {'json'}



def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def route():
	return redirect('/home')

@app.route('/home', methods=['GET', 'POST'])
def home():
	form = LinkForm()
	n = random.randint(50,100)
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
		if type_of_error == 0:
			noErrors(n)
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
			except:
				num_err += 1
				flash('Error in schema\n')
		# if there are errors in schemas, it's no reason to continue tests
		if num_err > 0 :
			return redirect('/index')
		else:
			flash('No errors in schemas\n')
		# let's try change point detection
		result_num = cpd_count(samples, schema, "number")
		result_len_str = cpd_count(samples, schema, "string")
		result_len_arr = cpd_count(samples, schema, "array")
		result_item_count = cpd_count(samples, schema, "item")
		for result in result_num:
			if len(result) == 2:
				flash(result[-1] + ': No anomaly \n')
			else:
				flash(result[-1] + ': Anomaly \n')
		for result in result_len_str:
			if len(result) == 2:
				flash(result[-1] + ': No anomaly \n')
			else:
				flash(result[-1] + ': Anomaly \n')
		for result in result_len_arr:
			if len(result) == 2:
				flash(result[-1] + ': No anomaly \n')
			else:
				flash(result[-1] + ': Anomaly \n')
		if len(result_item_count) == 2:
			flash(result[-1] + ': No anomaly \n')
		else:
			flash(result[-1] + ': Anomaly \n')
		return redirect('/index')
	return render_template('verify.html', title='Enter your json:')


@app.route('/index')
def index():
    return render_template('index.html', title='Results')
