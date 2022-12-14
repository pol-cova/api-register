# Import flask, and the packages needed for run the app
from flask import Flask,redirect,render_template,url_for,request
# Import this library needed for handling a config files and get the needed resources
from configparser import ConfigParser

# Import libraries to generate random serial-key
import random
import string

# Import necesary configuration files 
config = ConfigParser()
config.read('./config/config.cfg')
SECRET_KEY = config.get('app', 'secret_key')


# Import necesary configuration files for db
configDB = ConfigParser()
configDB.read('./config/db.config.cfg')


# Basic configuration for flask aplication
app = Flask(__name__)
# Import from config the main app secret key
app.secret_key = SECRET_KEY

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
            source = string.ascii_letters + string.digits
            # This function generate a random serial code for user (in the moment this key is saved in the DB)
            user_serial_key = ''.join((random.choice(source) for i in range(8)))
            return render_template('success.html', name = name, email = email, serial = user_serial_key)
    return render_template('403.html')

# This is the function to start the main app
if __name__ == '__main__':
    app.run(debug=True)