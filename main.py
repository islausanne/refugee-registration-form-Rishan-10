from flask import Flask, request, render_template, redirect, url_for, flash, session
import json
import os
import datetime

app = Flask(__name__)
app.secret_key = 'DarthVader10_'

name = ""
email = ""
date_of_birth = ""
country = ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/")
def home():
    return "Welcome to the homepage!"

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    global name, email, age
    name = request.form['name']
    email = request.form['email']
    date_of_birth = request.form['date_of_birth']
    country = request.form['country']
    message = request.form['message']
    gender = request.form['gender']

    session['name'] = name
    session['email'] = email
    session['message'] = message
    session['date_of_birth'] = date_of_birth
    session['country'] = country
    session['gender'] = gender

    if not name or not email or not date_of_birth or not country or not gender:
        flash('All fields are required!')
        return redirect(url_for('form'))

    session.pop('name', None)
    session.pop('email', None)
    session.pop('message', None)
    session.pop('date_of_birth', None)
    session.pop('country', None)

    flash('Thank you for registering!')
    return redirect(url_for('form'))

if __name__ == '__main__':
    app.run(debug=True)