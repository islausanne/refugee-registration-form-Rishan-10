from flask import Flask, request, render_template, redirect, url_for, flash, session
import re

app = Flask(__name__)
app.secret_key = 'DarthVader10_'

EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

name = ""
email = ""
age = 0

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
    age = int(request.form['age'])
    message = request.form['message']

    session['name'] = name
    session['email'] = email
    session['message'] = message
    session['age'] = age

    if not name or not email or not message or not age:
        flash('All fields are required!')
        return redirect(url_for('form'))

    if not re.match(EMAIL_REGEX, email):
        flash('Please enter a valid email address.')
        return redirect(url_for('form'))

    if len(message) < 10:
        flash('Message must be at least 10 characters long.')
        return redirect(url_for('form'))

    if age < 0:
        flash('Age must be greater than zero.')
        return redirect(url_for('form'))

    session.pop('name', None)
    session.pop('email', None)
    session.pop('message', None)
    session.pop('age', None)

    flash(f"Thank you, {name}. Your email address is {email}. You are {age} years old. Your message has been submitted.")
    return redirect(url_for('form'))

if __name__ == '__main__':
    app.run(debug=True)