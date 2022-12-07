from flask import Flask,redirect,render_template,url_for,request
from configparser import ConfigParser
# Import necesary configuration files 
config = ConfigParser()
config.read('./config/config.cfg')
SECRET_KEY = config.get('app', 'secret_key')

app = Flask(__name__)
app.secret_key = SECRET_KEY

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/register?/deepblur', methods=['GET', 'POST'])
def api_register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        return render_template('success.html', name = name, email = email)
    else:
        return render_template('403.html')



if __name__ == '__main__':
    app.run(debug=True)