# app/views.py
from flask import render_template

from app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result/<filename>')
def result(filename):
    return render_template('result.html', filename=filename)
