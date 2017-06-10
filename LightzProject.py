from threading import Thread
from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
from DbClass import DbClass
import os
import RPi.GPIO as GPIO
from threading import Thread
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
pinList = [40, 38, 37, 36, 35, 33, 32, 31]
db = DbClass()
status = db.getStatus()
statusList = list(sum(status, ()))

def application():
    for i in range (0,8):
        GPIO.setup(pinList[i], GPIO.OUT)

        if statusList[i] == 1:
            GPIO.output(pinList[i], GPIO.LOW)
        else:
            GPIO.output(pinList[i], GPIO.HIGH)

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
            button = request.form['button']
            db = DbClass()
            if button == 'login':
                session['username'] = request.form['username']
                pwd = db.getUser(request.form['username'])
                if pwd:
                    if request.form['password'] != pwd[0]:
                        error = "Error: Invalid credentials. Please try again."
                    else:
                        session['logged_in'] = True
                        return redirect(url_for('overzicht'))
                else:
                    error = "Error: Invalid credentials. Please try again."
            else:
                username = request.form['username']
                password = request.form['password']
                error = db.register(username, password)
        return render_template("login.html", error=error)

    @app.route('/logout')
    @login_required
    def logout():
        session.pop('logged_in', None)
        return redirect(url_for('login'))

    @app.route('/controlpanel', methods=['GET', 'POST'])
    @login_required
    def controlpanel():

        db = DbClass()
        statusen = db.getStatus()
        statusList = list(sum(statusen, ()))
        if request.method == 'POST':
            button = request.form['button']
            if button:
                if button == 'wasplaats_uit':
                    id = 1
                    status = 2 #uit
                    GPIO.output(pinList[0], GPIO.HIGH)
                elif button == 'wasplaats_aan':
                    id = 1
                    status = 1 #aan
                    GPIO.output(pinList[0], GPIO.LOW)

                elif button == 'badkamer_uit':
                    id = 2
                    status = 2
                    GPIO.output(pinList[1], GPIO.HIGH)
                elif button == 'badkamer_aan':
                    id = 2
                    status = 1
                    GPIO.output(pinList[1], GPIO.LOW)

                elif button == 'garage_uit':
                    id = 3
                    status = 2
                    GPIO.output(pinList[2], GPIO.HIGH)
                elif button == 'garage_aan':
                    id = 3
                    status = 1
                    GPIO.output(pinList[2], GPIO.LOW)

                elif button == 'keuken_uit':
                    id = 4
                    status = 2
                    GPIO.output(pinList[3], GPIO.HIGH)
                elif button == 'keuken_aan':
                    id = 4
                    status = 1
                    GPIO.output(pinList[3], GPIO.LOW)

                elif button == 'inkom_uit':
                    id = 5
                    status = 2
                    GPIO.output(pinList[4], GPIO.HIGH)
                elif button == 'inkom_aan':
                    id = 5
                    status = 1
                    GPIO.output(pinList[4], GPIO.LOW)

                elif button == 'living-tafel_uit':
                    id = 6
                    status = 2
                    GPIO.output(pinList[5], GPIO.HIGH)
                elif button == 'living-tafel_aan':
                    id = 6
                    status = 1
                    GPIO.output(pinList[5], GPIO.LOW)

                elif button == 'living_uit':
                    id = 7
                    status = 2
                    GPIO.output(pinList[6], GPIO.HIGH)
                elif button == 'living_aan':
                    id = 7
                    status = 1
                    GPIO.output(pinList[6], GPIO.LOW)
            db = DbClass()
            db.updateStatus(id,status)
            return redirect(url_for('controlpanel'))

        return render_template('controlpanel.html', status = statusList)

    @app.route('/overzicht')
    @login_required
    def overzicht():
        username = session['username']

        db = DbClass()
        status = db.getStatus()
        statusList = list(sum(status, ()))

        return render_template('overzicht.html', username=username, status=statusList)



    @app.route('/timer')
    @login_required
    def timer():
        return render_template('timer.html')

    return app

def sensor():
    while True:
        GPIO.setup(40, GPIO.IN)
        GPIO.setup(32, GPIO.OUT)
        i = GPIO.input(40)
        if i == 0:
            GPIO.output(32, 1)
        elif i == 1:
            GPIO.output(32,0)
            time.sleep(5)

def main():
    t1 = Thread(target=application)
    t2 = Thread(target=sensor)
    t1.start()
    t2.start()
    application().run(host=host, port=port, debug=True, use_reloader=False)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    host = "0.0.0.0"
    main()
