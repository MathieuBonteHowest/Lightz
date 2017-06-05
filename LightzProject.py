from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
from DbClass import DbClass

app = Flask(__name__)

app.secret_key = "nieuwe key"

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

        pwd = db.getUser(request.form['username'])

        if request.form['password'] != pwd[0]:
            error = "Invalid credentials. Please try again."
        else:
            session['logged_in'] = True
            flash('You were just logged in!')
            return redirect(url_for('controlpanel'))
    return render_template("login.html", error=error)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were just logged out!')
    return redirect(url_for('login'))

@app.route('/controlpanel')
@login_required
def controlpanel():
    return render_template('controlpanel.html')


if __name__ == '__main__':
    app.run(debug=True)
