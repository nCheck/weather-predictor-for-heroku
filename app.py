import flask
import os
from flask import jsonify, request
from flask import flash, redirect, url_for, session
from joblib import load
from flask_cors import CORS, cross_origin
import requests, json
import pandas as pd
import requests



model = load('random_forest.joblib')






app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = 'super secret key'
cors = CORS(app, resources={r"/*": {"origins": "*"}})






"""
Index(['Temperature (C)', 'Humidity', 'Wind Speed (km/h)',
       'Wind Bearing (degrees)', 'Visibility (km)', 'Pressure (millibars)',
       'Summary'],
"""


@app.route('/test', methods=['GET','POST'])
def test():
    print("loaded")
    URL = "http://api.openweathermap.org/data/2.5/weather?lat=19&lon=72&units=metric&appid=0eab9f6fc9a3f1ab2bb6212e5f4fceb0"
    r = requests.get(url = URL) 
    data = r.json()

    # mainData = data.get( 'main' , False )
    # windData = data.get( 'wind' , False )
    # use this approach if app crashes

    humidity = data['main']['humidity']
    pressure = data['main']['pressure']
    temperature = data['main']['temp']
    wind_deg = data['wind']['deg']
    wind_speed = data['wind']['speed']
    visibility = data.get( 'visibility' , 10000 ) / 1000

    print(data['weather'])
    print(data['main'])

    print( visibility , humidity, pressure, temperature, wind_deg, wind_speed) 
    return jsonify( data )





y_values=['Foggy','foggy','Overcast','overcast','cloudy','Cloudy','clear','Clear','rain','Rain','windy','Windy','breezy','Breezy','drizzle','Drizzle','Dry','dry']
classes_dict={'FOGGY':1,'OVERCAST':2,'CLOUDY':3,'CLEAR':4,'RAIN':5,'WINDY':6,'BREEZY':7,'DRIZZLE':8,'DRY':9}


@app.route('/predict', methods=['POST'])
def predict():

    # print( json.dumps( request.json['data'] ) )

    try :
        print("hi")
        data = request.json['coords']
        print(data)
        lat = data['latitude']
        lon = data['longitude']
        print(lat , lon)
        # print(data)
        URL = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid=0eab9f6fc9a3f1ab2bb6212e5f4fceb0"
        r = requests.get(url = URL) 
        data = r.json()
        # print(data)

        summary = data['weather'][0]['main']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        temperature = data['main']['temp']
        wind_deg = data['wind']['deg']
        wind_speed = data['wind']['speed']
        visibility = data.get( 'visibility' , 10000 ) / 1000 # prevent crashing

        inputData = [ temperature, humidity, wind_speed, wind_deg, visibility, pressure, classes_dict.get(summary, 4) ]

        prediction = model.predict( [ inputData ] )[0]
        print( prediction ) 

        return jsonify( { "result" : prediction , "status"  : True } )

    except:
        return jsonify( { "result" : "error" , "status"  : False } )      

# Index(['Temperature (C)', 'Humidity', 'Wind Speed (km/h)',
#        'Wind Bearing (degrees)', 'Visibility (km)', 'Pressure (millibars)',
#        'Summary'],



@app.route('/', methods=['GET'])
def home():
    print("loaded")
    return "Welcome to My API"




port = int(os.environ.get("PORT", 5005))
app.run(debug=True, use_reloader=True, port=port)
