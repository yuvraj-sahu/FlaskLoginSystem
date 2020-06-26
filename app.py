from flask import Flask, render_template, request
from users import check_user, add_user

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # The user is requesting for the site, so we render login.html
        return render_template('login.html')
    else:
        # The request method must be POST, so the user is submitting form data
        result = check_user(request.form['username'], request.form['password'])
        if result:
            return render_template('dashboard.html')
        else:
            return render_template('login.html', message=result.message)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        # The user is requesting for the site, so we render signup.html
        return render_template('signup.html')
    else:
        # The request method must be POST, so the user is submitting form data
        result = add_user(request.form['username'], request.form['password'])
        if result:
            return render_template('dashboard.html')
        else:
            return render_template('signup.html', message=result.message)
