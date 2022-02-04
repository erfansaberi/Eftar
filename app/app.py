import requests
import datetime
import jdatetime
from flask import Flask, render_template, request, redirect, render_template

app = Flask(__name__)

@app.route('/')
def getremainingtime():
    '''this function return a string that contain the remaining hours and minutes of your fast'''
    try:
        if request.args.get('citycode'):
            citycode = request.args.get('citycode')
            citycode = int(citycode)
        elif request.form.get('citycode'):
            citycode = request.form.get('citycode')
            citycode = int(citycode)
        else:
            return render_template('home.html',data={'status':'error'})   
    except:
        return render_template('home.html',data={'status':'error'})
    try:
        '''using aviny.com api to get maghreb and sobh azan time'''
        oghat = requests.get(f'https://prayer.aviny.com/api/prayertimes/{citycode}')
    except:
        return 'An error occurred during connecting to "Aviny.com" API.'
    if oghat.ok:
        now = datetime.datetime.strptime(oghat.json().get('Today').split(' - ')[1], '%I:%M %p').time()
        maghreb = oghat.json().get('Maghreb')
        sobh = oghat.json().get('Imsaak')
        shahr = oghat.json().get('CityName')
        if not shahr:
            return render_template('home.html',data={'status':'cityNotFound'})
        '''convert maghreb and sobh to datetime type'''
        maghrebtime = datetime.datetime.strptime(maghreb, '%H:%M:%S').time()
        sobhtime = datetime.datetime.strptime(sobh, '%H:%M:%S').time()
        if now > maghrebtime:
            return render_template('home.html',data={'status':'eftar','shahr':shahr,'time':now})
        if now < sobhtime:
            return render_template('home.html',data={'status':'notstarted','sobh':sobh,'shahr':shahr,'time':now})
        
        '''calculate remaining time'''
        remaininghour = maghrebtime.hour - now.hour
        remainingminute = maghrebtime.minute - now.minute
        if remainingminute < 0:
            remaininghour -= 1
            remainingminute = 60 + remainingminute
        remainingtimestr = f'{remaininghour} Hours and {remainingminute} Minutes'
        return render_template('home.html',data={'status':'remaining','maghreb':maghreb,'hour':remaininghour,'minute':remainingminute,'shahr':shahr,'time':now})

    else:
        return 'An error occurred during connecting to "Aviny.com" API.'