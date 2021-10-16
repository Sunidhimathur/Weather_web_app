from flask import Flask, render_template, request, flash
import requests
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'something something'
@app.route('/', methods=['GET', 'POST'])
def index():
    
    if request.method=='POST':
        city = request.form.get('city')
        url = 'http://api.weatherapi.com/v1/{}.json?key=b54c813b287c45f7af960455211509&q={}&aqi=no'
        type1 = 'current'
        data = requests.get(url.format(type1, city))
        curr = data.json()
        
        if 'error' in curr.keys():
            flash(curr['error']['message'])
            return render_template('index.html', msg=curr['error']['message'])
        
        loc = curr['location']
        cond = curr['current']
        
        details = {
            'location': f"{loc['name']}, {loc['region']}, {loc['country']}",
            'icon' : cond['condition']['icon'],
            'condition': cond['condition']['text'],
            'temp': cond["temp_c"],
            'wind': f"{cond['wind_kph']}km/hr\t{cond['wind_dir']}",
            'humidity': cond['humidity'],
            'precipitation': f"{cond['precip_mm']} mm"
        }
        
        type1 = 'forecast'
        city = city+'&days=7'
        data = requests.get(url.format(type1, city))
        forecast = data.json()
        forecast = forecast['forecast']['forecastday']
        
        forecast_days = []
        for value in forecast:
            year, month, day = list(map(int, value['date'].split('-')))
            date = datetime.datetime(year,month,day)
            date = date.strftime("%A %d %b")
            
            day = value['day']
            forecast_details = {
                'date' : date,
                'icon' : day['condition']['icon'],
                'condition': day['condition']['text'],
                'temp': f"Max : {day['maxtemp_c']}C |  Min : {day['mintemp_c'] }C  |  Avg : {day['avgtemp_c']}C",
                'rain_chance': day['daily_chance_of_rain'],
                'humidity' : day['avghumidity'],
                'uv' : day['uv']
            }
            forecast_days.append(forecast_details)
        
        return render_template('index.html', details = details, forecast_days=forecast_days)

    else:
        return render_template('index.html')
        
    
    
    
if __name__ == '__main__':
    app.run(debug=False)
