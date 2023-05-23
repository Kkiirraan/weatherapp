from flask import Flask,redirect,render_template,jsonify,url_for,request
import requests,json

api_key='230ac56204b139a61162fc18a9d5cc63'
app=Flask(__name__)


def keltocelcius(kelvin):
    celcius= round(kelvin - 273.15)
    return celcius

@app.route('/',methods=['GET','POST'])
def index():    
    return render_template('index.html')

@app.route('/check',methods=['GET','POST'])
def check():
  if request.method == 'POST':
    data = request.get_json()
    print(data)
    city=data['city']
    
    if not city:
        return "not get data"
    try:
      weather_data=requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}',timeout=5)
      if weather_data.json()['cod']=='404':
           print('No city found')
      else:    
           weather=weather_data.json()['weather'][0]['main']
           temp=round(weather_data.json()['main']['temp'])
           celcius=keltocelcius(temp)
           print(temp)
           print(weather)
           print(weather_data.json())
           response = {'weather': f'The weather in {city} is :{weather}','temp':f'The temperature in {city} is:{celcius}\u00B0'}
           return jsonify(response)
    except requests.exceptions.Timeout:
           response={'connection':'Network Error'}
           return jsonify(response)
    except requests.exceptions.RequestException as e:
        response={'connection':'unable to connect'} 
        return jsonify(response)
    
    
if __name__=='__main__':
    app.run(debug=True)