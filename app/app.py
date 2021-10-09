import requests
import datetime
from flask import Flask, render_template, request, redirect, render_template

app = Flask(__name__)

@app.route('/')
def getremainingtime():
    time = requests.get('https://api.keybit.ir/time/')

    nowstr = time.json().get('time24').get('full').get('en')
    now = datetime.datetime.strptime(nowstr, '%H:%M:%S').time()
    '''this function return a string that contain the remaining hours and minutes of your fast'''
    try:
        if request.args.get('citycode'):
            citycode = request.args.get('citycode')
            citycode = int(citycode)
        elif request.form.get('citycode'):
            citycode = request.form.get('citycode')
            citycode = int(citycode)
        else:
            return render_template('home.html',data={'status':'error','time':now})   
    except:
        return render_template('home.html',data={'status':'error','time':now})
    try:
        '''using aviny.com api to get maghreb and sobh azan time'''
        oghat = requests.get(f'https://prayer.aviny.com/api/prayertimes/{citycode}')
    except:
        return 'An error occurred during connecting to "Aviny.com" API.'
    if oghat.ok:
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

if __name__ == "__main__":
    app.run("localhost", 5000, debug=True)
