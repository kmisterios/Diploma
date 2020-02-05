# -*- coding: utf-8 -*-
from Service import app
from flask import render_template, flash, redirect, request
from Service.forms import LinkForm
import json
from jsonschema import validate

@app.route('/')
def route():
	return redirect('/home')

@app.route('/home', methods=['GET', 'POST'])
def home():
	return render_template('home.html', title='Home')

@app.route('/go')
def go():
	return redirect('/links')

@app.route('/links', methods=['GET', 'POST'])
def link():
	form = LinkForm()
	path = 'Service/schemas.json'
	with open(path, 'r') as f:
		schema = json.loads(f.read())
	with open('Service/samples.json', 'r') as f:
		samples = json.loads(f.read())
	if form.validate_on_submit():
		for sample in samples:
			try:
				validate(instance=sample, schema=schema)
				flash('Ok \n')
			except:
				flash('Error \n')
		return redirect('/index')
	return render_template('links.html', title='Enter your json:', form=form)


@app.route('/index')
def index():
    return render_template('index.html', title='Results')
