from flask import Flask, render_template, request
import sys
import requests
import os
import datetime
import time


app = Flask(__name__)
# API_KEY = os.environ.get('WEATHER_API_KEY')
API_KEY = '4b1d3b381d9370cb1209f53b25b46f83'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return add()
    return render_template('index.html')


def add():
    city_name = request.form['city_name'].lower()

    r = requests.get('https://api.openweathermap.org/data/2.5/weather', params={
        'q': city_name, 'appid': API_KEY, 'units': 'metric'}).json()


    for k, v in r.items():
        print(k, ':', v)

    city_name = r['name'].upper()
    temp = r['main']['temp']
    state = r['weather'][0]['main']

    city_time = datetime.datetime.utcfromtimestamp(time.time() + r['timezone']).time()
    sunrise = datetime.datetime.utcfromtimestamp(r['sys']['sunrise'] + r['timezone']).time()
    sunset = datetime.datetime.utcfromtimestamp(r['sys']['sunset'] + r['timezone']).time()
    afternoon = datetime.time(hour=12)

    if sunrise <= city_time < afternoon:
        day_period = 'day'
    elif afternoon <= city_time < sunset:
        day_period = 'evening-morning'
    else:
        day_period = 'night'

    weather_dict = {'city_name': city_name, 'day_night': day_period, 'temp': temp,
                    'state': state}
    return render_template('index.html', weather=weather_dict)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
