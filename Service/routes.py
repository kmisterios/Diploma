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
TP, FN, FP = 0, 0, 0
error = 'no'

def allowed_file(filename):
	global ALLOWED_EXTENSIONS
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def route():
	return redirect('/home')

@app.route('/home', methods=['GET', 'POST'])
def home():
	global error
	form = LinkForm()
	n = random.randint(10,20)
	if request.method == 'POST':
		type_of_error = int(form.link.data)
		if type_of_error == 1:
			error = 'name'
			error1(n)
		if type_of_error == 2:
			error = 'customer name'
			error2(n)
		if type_of_error == 3:
			error = 'price'
			error3(n)
		if type_of_error == 4:
			error = 'phone number'
			error4(n)
		if type_of_error == 5:
			error = 'item'
			error5(n)
		if type_of_error == 0:
			error = 'no'
			noErrors(n)
		return redirect('/verify')
	return render_template('home.html', title='Home', form = form)

@app.route('/go')
def go():
	return redirect('/verify')

@app.route('/verify', methods=['GET', 'POST'])
def link():
	global error, FN, FP, TP
	path = 'Service/schemas.json'
	path1 = 'collections.json'
	with open(path, 'r') as f:
		schema = json.loads(f.read())
	with open(path1, 'r') as f:
		samples = json.loads(f.read())
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
		new_samples = json.loads(file.read())
		print('Collection length: ', len(samples))
		samples = samples + new_samples
		#print(new_samples)
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
		num_err = 0
		for result in result_num:
			if len(result) == 2:
				if result[-1] == error:
					FP += 1
				else:
					TP += 1
				flash(result[-1] + ': No anomaly \n')
			else:
				if result[-1] != error:
					FN += 1
					print(result[-1])
				num_err += 1
				flash(result[-1] + ': Anomaly \n')
		for result in result_len_str:
			if len(result) == 2:
				if result[-1] == error:
					FP += 1
				else:
					TP += 1
				flash(result[-1] + ': No anomaly \n')
			else:
				if result[-1] != error:
					FN += 1
					#print(result[-1])
				num_err += 1
				flash(result[-1] + ': Anomaly \n')
		for result in result_len_arr:
			if len(result) == 2:
				if result[-1] == error:
					FP += 1
				else:
					TP += 1
				flash(result[-1] + ': No anomaly \n')
			else:
				if result[-1] != error:
					FN += 1
					print(result[-1])
				num_err += 1
				flash(result[-1] + ': Anomaly \n')
		if len(result_item_count) == 2:
			if result_item_count[-1] == error:
				FP += 1
			else:
				TP += 1
			flash(result_item_count[-1] + ': No anomaly \n')
		else:
			if result_item_count[-1] != error:
				FN += 1
				print(result_item_count[-1])
			num_err += 1
			flash(result_item_count[-1] + ': Anomaly \n')
		if num_err == 0:
			with open(path1, 'w') as f:
				json.dump(samples, f)
		print('True positives: ', TP)
		print('False positives', FP)
		print('False negatives: ', FN)
		if (TP + FP > 0) or (TP + FN > 0):
			precision = TP / (TP + FP)
			recall = TP/ (TP + FN)
			f1_score = 2 * precision * recall / (precision + recall)
			flash('f1-score: ' + str(f1_score * 100) + '%')
		return redirect('/index')
	return render_template('verify.html', title='Enter your json:')


@app.route('/index')
def index():
    return render_template('index.html', title='Results')
