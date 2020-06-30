from flask import Flask, render_template, request, redirect, url_for, session
from users import check_user, add_user

app = Flask(__name__)

# Make sure to set your own secret key, and keep it secret!
# To do so, type the following commands into your Python Shell:
# >>> import os
# >>> print(os.urandom(32))
# You can make your secret keys larger or smaller by changing the parameter
# for the os.urandom function (I used 32)
app.secret_key = b'\xcc\\s_\x00oX\xe2\x13\x85|\xf1Ss\x97\x8d\xb9b\xe7%Qyp@5\xb2\xda\xfd\xf3\xc5\xa0\xfe'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged-in'):
        return redirect(url_for('dashboard'))
    if request.method == 'GET':
        # The user is requesting for the site, so we render login.html
        return render_template('login.html')
    else:
        # The request method must be POST, so the user is submitting form data
        username = request.form['username']
        password = request.form['password']
        result = check_user(username, password)
        if result:
            session['logged-in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', message=result.message)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if session.get('logged-in'):
        return redirect(url_for('dashboard'))
    if request.method == 'GET':
        # The user is requesting for the site, so we render signup.html
        return render_template('signup.html')
    else:
        # The request method must be POST, so the user is submitting form data
        username = request.form['username']
        password = request.form['password']
        result = add_user(username, password)
        if result:
            session['logged-in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('signup.html', message=result.message)

@app.route('/dashboard')
def dashboard():
    if session.get('logged-in'):
        return render_template('dashboard.html', username=session.get('username'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['logged-in'] = False
    session['username'] = None
    return redirect(url_for('home'))
