# Imports for code
from flask import Flask, request, render_template, redirect, url_for, flash, session
import json
import os

# Creates Flask application
app = Flask(__name__)

# Secures website data
app.secret_key = 'DarthVader10_'

# Defines the route for the homepage
@app.route('/')
def index():
    # Goes to index.html and applies this html code to this page
    return render_template('index.html')

# Defines the route for the form
@app.route('/form')
def form():
    # Goes to form.html and applies this html code to this page
    return render_template('form.html')

# Processes the form data when the user submits the form
@app.route('/submit', methods=['POST'])
def submit():
    # Obtains the data submitted by the user in the form fields
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

    # This saves the submitted data into a session, this can be used to remember this data temporarily
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

    # Checks to see if any of these fields are empty
    if not name or not email or not date_of_birth or not country or not gender or not phone_number or not phone_number_2 or not location:
        flash('All fields are required!')
        return redirect(url_for('form'))

    # Checks to see if the length of the phone number is between 7 and 15 digits.
    if len(full_phone_number) < 7 or len(full_phone_number) > 15:
        flash('Phone number must be between 7 and 15 digits!')
        return redirect(url_for('form'))

    # Checks to see if the date of birth is after 1900
    if int(date_of_birth[:4]) < 1900:
        flash('Date of birth must be after 1900!')
        return redirect(url_for('form'))

    # This deletes the data which was saved in the session
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

    # This flashes a message at the top of the page to show confirmation of the registration
    flash('Thank you for registering!')

    # Check if file exists
    if os.path.exists('registrations.json'):
        with open('registrations.json', 'r') as file:
            # If it does exist, then the data is saved in a variable called data
            data = json.load(file)
    else:
        # If not, then the variable data is set to be an empty list.
        data = []

    # Add the new registration
    data.append({'name': name, 'country': country, 'date_of_birth': date_of_birth, 'email': email, 'phone_number': f"+{full_phone_number}", 'gender': gender, 'medical_needs': medical_needs, 'other_needs': other_needs})

    # Save all registrations back to the file
    with open('registrations.json', 'w') as file:
        json.dump(data, file, indent=2)

    # Returns the user to the form page
    return redirect(url_for('form'))

# Defines the route for the view page
@app.route('/view')
def view_registrations():
    # Checks if any data exists
    # Puts the data into a list
    if os.path.exists('registrations.json'):
        with open('registrations.json', 'r') as file:
            data = json.load(file)
    else:
        data = []
    # Makes the view webpage with the html code in view.html
    # Sends the data received from the user to the html code
    return render_template('view.html', registrations=data)

# Deletes the form data when a button is pressed by the user.
@app.route('/delete')
def delete_registration():
    # If any data exists, the json file is deleted and the variable data is set to an empty list
    if os.path.exists('registrations.json'):
        os.remove('registrations.json')
        data=[]

    # Shows a confirmation message to show data has been deleted.
    flash('Registrations deleted successfully!')
    # Returns user to the view page
    return render_template('view.html', registrations=data)

# If the code is being run from the python file, then the webpage gets created
if __name__ == '__main__':
    app.run(debug=True)