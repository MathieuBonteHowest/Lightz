from flask import Flask, render_template, redirect, url_for, request, session
from functools import wraps
from DbClass import DbClass
import os
import RPi.GPIO as GPIO
from threading import Thread
import threading
from datetime import datetime
import time

def application():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    pinList = [40, 38, 37, 36, 35, 33, 32, 31]
    db = DbClass()
    status = db.getStatus()
    statusList = list(sum(status, ()))

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
                pwd = db.getUser(request.form['username'], request.form['password'])
                if pwd:
                    if True != pwd:
                        error = "Error: Ongeldige login. Probeer het opnieuw."
                    else:
                        session['logged_in'] = True
                        return redirect(url_for('overzicht'))
                else:
                    error = "Error: Ongeldige login. Probeer het opnieuw."
            else:
                username = request.form['username']
                password = request.form['password']
                code = request.form['code']
                error = db.register(username, password, code)
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

                elif button == 'alles_uit':
                    id = 100
                    status = 2
                    GPIO.output(40, GPIO.HIGH)
                    GPIO.output(38, GPIO.HIGH)
                    GPIO.output(37, GPIO.HIGH)
                    GPIO.output(36, GPIO.HIGH)
                    GPIO.output(35, GPIO.HIGH)
                    GPIO.output(33, GPIO.HIGH)
                    GPIO.output(32, GPIO.HIGH)

                elif button == 'alles_aan':
                    id = 100
                    status = 1
                    GPIO.output(40, GPIO.LOW)
                    GPIO.output(38, GPIO.LOW)
                    GPIO.output(37, GPIO.LOW)
                    GPIO.output(36, GPIO.LOW)
                    GPIO.output(35, GPIO.LOW)
                    GPIO.output(33, GPIO.LOW)
                    GPIO.output(32, GPIO.LOW)

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

    @app.route('/timer', methods=['GET', 'POST'])
    @login_required
    def timer():
        error = ''
        if request.method == 'POST':
            button = request.form['button']
            db = DbClass()
            if button == "opslaan timer":
                uur = request.form['uur_start_timer']
                minuten = request.form['minuten_start_timer']
                if (uur.isdigit()) and (minuten.isdigit()):
                    if (int(uur) > 23) or (int(minuten) > 59):
                        error = "Error: Foute gegevens."
                    else:
                        licht_timer = int(request.form['timer_licht'])
                        uur_timer = int(uur)
                        minuten_timer = int(minuten)

                        #hour = *3600
                        #minutes = *60
                        delay = (uur_timer * 3600) + (minuten_timer * 60)

                        if licht_timer == 1:
                            GPIO.output(40, GPIO.LOW)
                            threading.Timer(delay, timer_off, args=(1,40,)).start()

                        elif licht_timer == 2:
                            GPIO.output(38, GPIO.LOW)
                            threading.Timer(delay, timer_off, args=(2, 38,)).start()

                        elif licht_timer == 3:
                            GPIO.output(37, GPIO.LOW)
                            threading.Timer(delay, timer_off, args=(3, 37,)).start()

                        elif licht_timer == 4:
                            GPIO.output(36, GPIO.LOW)
                            threading.Timer(delay, timer_off, args=(4, 36,)).start()

                        elif licht_timer == 5:
                            GPIO.output(35, GPIO.LOW)
                            threading.Timer(delay, timer_off, args=(5, 35,)).start()

                        elif licht_timer == 6:
                            GPIO.output(33, GPIO.LOW)
                            threading.Timer(delay, timer_off, args=(6, 33,)).start()

                        elif licht_timer == 7:
                            GPIO.output(32, GPIO.LOW)
                            threading.Timer(delay, timer_off, args=(7, 32,)).start()

                        db.updateStatus(licht_timer, 1)
                        error = "Succesvol opgeslagen."
                else:
                    error = "Error: Foute gegevens."

            else:
                uur_start = request.form['uur_start_periode']
                minuten_start = request.form['minuten_start_periode']
                uur_einde = request.form['uur_einde_periode']
                minuten_einde = request.form['minuten_einde_periode']

                if (uur_start.isdigit()) and (minuten_start.isdigit()) and (uur_einde.isdigit()) and (minuten_einde.isdigit()):
                    if (int(uur_start) > 23) or (int(minuten_start) > 59) or (int(uur_einde) > 23) or (int(minuten_einde) > 59):
                        error = "Error: Foute gegevens."
                    else:
                        now = datetime.now()
                        now_format = format(now, '%H:%M:%S')

                        licht_periode = int(request.form['periode_licht'])
                        begin_uur = int(uur_start)
                        begin_minuut = int(minuten_start)
                        eind_uur = int(uur_einde)
                        eind_minuut = int(minuten_einde)

                        date_hour = str(now_format)[0:2]
                        date_min = str(now_format)[3:5]
                        date_sec = str(now_format)[6:]

                        delay_hour_begin = (begin_uur - int(date_hour)) * 3600
                        delay_min_begin = (begin_minuut - int(date_min) -1) * 60
                        delay_sec_begin = (60- int(date_sec))

                        delay_hour_einde = (eind_uur - int(date_hour)) * 3600
                        delay_min_einde = (eind_minuut - int(date_min) -1) * 60
                        delay_sec_einde = (60- int(date_sec))

                        delay_begin = delay_hour_begin + delay_min_begin + delay_sec_begin
                        delay_einde = delay_hour_einde + delay_min_einde +delay_sec_einde

                        if licht_periode == 1:
                            threading.Timer(delay_begin, periode_on, args=(1,40, delay_einde,)).start()
                        elif licht_periode == 2:
                            threading.Timer(delay_begin, periode_on, args=(2,38, delay_einde,)).start()
                        elif licht_periode == 3:
                            threading.Timer(delay_begin, periode_on, args=(3,37, delay_einde,)).start()
                        elif licht_periode == 4:
                            threading.Timer(delay_begin, periode_on, args=(4,36, delay_einde,)).start()
                        elif licht_periode == 5:
                            threading.Timer(delay_begin, periode_on, args=(5,35, delay_einde,)).start()
                        elif licht_periode == 6:
                            threading.Timer(delay_begin, periode_on, args=(6,33, delay_einde,)).start()
                        elif licht_periode == 7:
                            threading.Timer(delay_begin, periode_on, args=(7,32, delay_einde,)).start()
                        error = "Succesvol opgeslagen."
                else:
                    error = "Error: Foute gegevens."


        return render_template('timer.html', error=error)

    return app

def sensor():
    while True:
        GPIO.setup(12, GPIO.IN)
        i = GPIO.input(12)
        db = DbClass()
        db2 = DbClass()
        if i == 0:
            GPIO.output(31, 1)
            db.updateStatus(8, 2)
        elif i == 1:
            GPIO.output(31,0)
            db.updateStatus(8, 1)
            db2.insertSensorValue(1)
            time.sleep(60)
        time.sleep(0.5)

def timer_off(id, light):
    db = DbClass()
    GPIO.output(light, GPIO.HIGH)
    db.updateStatus(id, 2)

def periode_on(id, light, delay_einde):
    db =DbClass()
    GPIO.output(light, GPIO.LOW)
    db.updateStatus(id, 1)
    threading.Timer(delay_einde, periode_off, args=(id, light,))

def periode_off(id, light):
    db = DbClass()
    GPIO.output(light, GPIO.HIGH)
    db.updateStatus(id, 2)

def main():
    t1 = Thread(target=application)
    t2 = Thread(target=sensor)

    t1.daemon = True
    t2.daemon = True
    t1.start()
    t2.start()
    application().run(host=host, port=port, debug=True, use_reloader=False)

if __name__ == '__main__':
    try:
        port = int(os.environ.get("PORT", 8080))
        host = "0.0.0.0"
        main()
    except Exception as err:
        print(err)