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
    gender = request.form['gender']
    location = request.form['location']
    medical_needs = request.form['medical_needs']
    other_needs = request.form['other_needs']
    phone_number = request.form['phone']
    phone_number_2 = request.form['phone2']
    full_phone_number = f"{phone_number}{phone_number_2}"

    session['name'] = name
    session['email'] = email
    session['date_of_birth'] = date_of_birth
    session['country'] = country
    session['gender'] = gender
    session['phone'] = phone_number
    session['phone2'] = phone_number_2
    session['location'] = location
    session['medical_needs'] = medical_needs
    session['other_needs'] = other_needs

    if not name or not email or not date_of_birth or not country or not gender or not phone_number or not phone_number_2 or not location:
        flash('All fields are required!')
        return redirect(url_for('form'))

    if len(full_phone_number) < 7 or len(full_phone_number) > 15:
        flash('Phone number must be between 7 and 15 digits!')
        return redirect(url_for('form'))

    session.pop('name', None)
    session.pop('email', None)
    session.pop('date_of_birth', None)
    session.pop('country', None)
    session.pop('location', None)
    session.pop('gender', None)
    session.pop('phone', None)
    session.pop('phone2', None)
    session.pop('medical_needs', None)
    session.pop('other_needs', None)

    flash('Thank you for registering!')

    # Check if file exists
    if os.path.exists('registrations.json'):
        with open('registrations.json', 'r') as file:
            data = json.load(file)
    else:
        data = []

    # Add the new registration
    data.append({'name': name, 'country': country, 'date_of_birth': date_of_birth, 'email': email, 'phone_number': f"+{full_phone_number}", 'gender': gender, 'medical_needs': medical_needs, 'other_needs': other_needs})

    # Save all registrations back to the file
    with open('registrations.json', 'w') as file:
        json.dump(data, file, indent=2)

    return redirect(url_for('form'))

@app.route('/view')
def view_registrations():
    if os.path.exists('registrations.json'):
        with open('registrations.json', 'r') as file:
            data = json.load(file)
    else:
        data = []
    return render_template('view.html', registrations=data)

@app.route('/delete')
def delete_registration():
    if os.path.exists('registrations.json'):
        os.remove('registrations.json')
        data=[]

    flash('Registrations deleted successfully!')
    return render_template('view.html', registrations=data)

if __name__ == '__main__':
    app.run(debug=True)