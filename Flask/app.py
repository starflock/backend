import os
import pyrebase
import firebase_admin
from firebase_admin import db
from flask import *

app = Flask(__name__)
app.secret_key = os.urandom(24)

#Initialize Firebase
apiKey = os.environ['apiKey']
authDomain = os.environ['authDomain']
databaseURL = os.environ['databaseURL']
projectId = os.environ['projectId']
messagingSenderId = os.environ['messagingSenderId']

config = {
    "apiKey": apiKey,
    "authDomain": authDomain,
    "databaseURL": databaseURL,
    "projectId": projectId,
    "storageBucket": "",
    "messagingSenderId": messagingSenderId
}

'''
config = {
    "apiKey": "AIzaSyBWq1Xb8Xvdk5kT1TZDcMV03LthN8T_S3U",
    "authDomain": "fire-f2ac3.firebaseapp.com",
    "databaseURL": "https://fire-f2ac3.firebaseio.com/",
    "projectId": "fire-f2ac3",
    "storageBucket": "",
    "messagingSenderId": "884346479751"
}
'''
'''
firebase_admin.initialize_app(
    options={
        'databaseURL': 'https://fire-f2ac3.firebaseio.com/'
    }
)
NAME = db.reference('name')
'''

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

@app.route('/', methods=['GET', 'POST'])
def index():
    unsuccessful = 'Please check your credentials'
    successful = 'Login successful'
    if request.method == 'POST':
        email = request.form['name']
        password = request.form['pass']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            results = auth.get_account_info(user['idToken'])
            is_email_verified = results['users'][0]['emailVerified']
            if is_email_verified:
                return render_template('login.html', s=':-)')
                #return render_template('profile.html', s=user)
            else:
                auth.send_email_verification(user['idToken'])
                return render_template('login.html', us=unsuccessful)
        except:
            return render_template('login.html', us=unsuccessful)
            # Reset your email
            # auth.send_password_reset_email(email)

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        if request.method == 'POST':
            email = request.form['name']
            password = request.form['pass']
            user = auth.create_user_with_email_and_password(
                    email=email,
                    password=password)
            auth.send_email_verification(user['idToken'])
            successful = 'Thanks for registering!'
            return render_template('login.html', s=successful)
    except Exception as e:
        print e
    return render_template('register.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
	app.run()
