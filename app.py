# Import flask, and the packages needed for run the app
from flask import Flask,redirect,render_template,url_for,request, jsonify
# Import this library needed for handling a config files and get the needed resources
from configparser import ConfigParser
# Import library for connect db
from pymongo import MongoClient 

# Import libraries to generate random serial-key
import random
import string

# Import libraries to api function
import datetime

# Import necesary configuration files 
config = ConfigParser()
config.read('./config/config.cfg')
SECRET_KEY = config.get('app', 'secret_key')


# Import necesary configuration files for db
configDB = ConfigParser()
configDB.read('./config/db.config.cfg')
db_client = configDB.get('db-uri', 'client')

# Basic configuration for flask aplication
app = Flask(__name__)
# Import from config the main app secret key
app.secret_key = SECRET_KEY

# Define DB connection
client = MongoClient(db_client)
db = client.get_database('new_users')
db_users = db.get_collection('new_users')

# Main route -> this route render the register form in html to register users
@app.route('/')
def index():
    return render_template('index.html')

# Registe route -> this route handling data from main route and register user
@app.route('/api/register?/deepblur', methods=['GET', 'POST'])
def api_register():
    # This is the condicional preposition for validate if the user is sending data
    if request.method == 'POST':
        # This is the data that api get from html form
        name = request.form['name']
        email = request.form['email']
        # This condicional propositon validate if form doesn't be empty, in the case the form be empty return an error (403)
        if name != '' and email !='':
            found_email = db_users.find_one({"email" : email })
            if found_email:
                return render_template("010.html")
            else:
                source = string.ascii_letters + string.digits
                # This function generate a random serial code for user (in the moment this key is saved in the DB)
                user_serial_key = ''.join((random.choice(source) for i in range(8)))
                # This function register user into a db
                new_user = {'name': name, 'email': email, 'serial-code': user_serial_key}
                db_users.insert_one(new_user)
                return render_template('success.html', name = name, email = email, serial = user_serial_key)
    return render_template('403.html')

# Support routes-> this route is for recieve request from users
# Main route
@app.route('/deepblur/web-service/support')
def support():
    return render_template('support.html')
# Route to handling errors report
@app.route('/deepblur/web-services/support/request/status', methods = ['GET', 'POST'])
def request_support():
    if request.method == 'POST':
        name = request.form['name']
        error = request.form['error']
        if name != '' and error != '':
            date_for_request = datetime.datetime.now()
            support_email = 'pm.interactive.games@gmail.com'
            support_advice = 'Hello, We stay tuned into your comments, and sorry for your error, if the error persist please contact us for email :) !'
            support_status = 'We recived your request!'
            support_request_status = "Working on solving your bug! "
            data = {
                "Support message": support_advice,
                "Support email": support_email,
                "Name": name,
                "Error or bug": error,
                "Date of report": date_for_request,
                "Support report": support_status,
                "Actual status of report": support_request_status
            }
            return jsonify(data)

# This is the function to start the main app
if __name__ == '__main__':
    app.run(debug=True)