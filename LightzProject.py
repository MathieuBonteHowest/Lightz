from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
from DbClass import DbClass
import os

app = Flask(__name__)

app.secret_key = "MHkGBcKLloYeSp4FDaCsftFTesfDea7w"

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        db = DbClass()
        session['username'] = request.form['username']
        pwd = db.getUser(request.form['username'])
        if pwd:
            if request.form['password'] != pwd[0]:
                error = "Invalid credentials. Please try again."
            else:
                session['logged_in'] = True
                return redirect(url_for('overzicht'))
        else:
            error = "Invalid credentials. Please try again."
    return render_template("login.html", error=error)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/controlpanel')
@login_required
def controlpanel():
    return render_template('controlpanel.html')

@app.route('/overzicht')
def overzicht():
    username = session['username']
    return render_template('overzicht.html', username=username)

@app.route('/timer')
def timer():
    return render_template('timer.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    host = "0.0.0.0"
    app.run(host=host, port=port, debug=True)
