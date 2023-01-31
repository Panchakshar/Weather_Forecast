import urllib.parse
import urllib.request
import json
import datetime
import pandas as pd
import numpy as np
import streamlit as st
import pickle

# Load a saved model
file = open(
    'C:\\Users\lenovo\Data_Science\Projects\Weather_Forcast\weather_forecast_model.pkl', 'rb')
model = pickle.load(file)
file.close()

st.title("Weather Forecast Webapp")
API_KEY = "VRV2BXKVKNL2SGPL35GJ8UJG9"
UNIT_GROUP = "metric"
LOCATION = st.text_input('Location')
d = st.date_input("Date")
DATE = d.strftime('%Y-%m-%d')
d15 = d - datetime.timedelta(15)
DATE15 = d15.strftime('%Y-%m-%d')
btn1 = st.button("Predict")
loc = urllib.parse.quote_plus(LOCATION)

def getWeatherForecast(date):
    requestUrl = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/" + loc + "/"
    requestUrl = requestUrl + date + "?key="+API_KEY + \
        "&unitGroup="+UNIT_GROUP+"&include=days"

    print('Weather requestUrl={requestUrl}'.format(requestUrl=requestUrl))

    try:
        req = urllib.request.urlopen(requestUrl)
    except:
        print("Could not read from:"+requestUrl)
        return []

    rawForecastData = req.read()
    req.close()
    return json.loads(rawForecastData)

def getLastData():
    df = pd.DataFrame()
    if loc:
        show_hist = st.expander(label = 'Previous 15 days History')
        with show_hist:
            start_date = d
            date_df = []
            temp_df = []
            max_temp_df = []
            min_temp_df = []
            feelslike_df = []
            for i in range(15):
                start_date = d - datetime.timedelta(i)
                date = start_date.strftime('%Y-%m-%d')                
                weatherForecast = getWeatherForecast(date)
                days = weatherForecast['days']
                for day in days:
                    date_df.append(start_date)
                    temp_df.append(day['temp'])
                    max_temp_df.append(day['tempmax'])
                    min_temp_df.append(day['tempmin'])
                    feelslike_df.append(day['feelslike'])
                    
            df['Date'] = date_df
            df['MaxTemp'] = max_temp_df
            df['MinTemp'] = min_temp_df
            df['Temp'] = temp_df
            df['Feelslike'] = feelslike_df
            df.set_index('Date',inplace=True)
            st.table(df)
    st.line_chart(df)
    
def getDashboard():
    weatherForecast = getWeatherForecast(DATE)
    days = weatherForecast['days']
    lat = weatherForecast['latitude']
    long = weatherForecast['longitude']
    col1,col2,col3,col4,col5,col6 = st.columns(6)
    for day in days:
        col1.metric("Max Temp(°C)", day['tempmax'])
        col2.metric("Min Temp(°C)", day['tempmin'])
        col3.metric("Humidity(%)",day['humidity'])
        col4.metric("Precip(mm)",day['precip'])
        col5.metric("Wind(kph)",day['windspeed'])
        col6.metric("Pressure(mb)",day['pressure'])
                
    getLastData()      
    st.map(pd.DataFrame({'lat': [lat], 'lon': [long]}))
            
def predictTemp():
    
    if btn1:
        weatherForecast = getWeatherForecast(DATE)

        days = weatherForecast['days']        
        
        for day in days:
            data = np.array([day["tempmax"], day["tempmin"], day["feelslikemax"], day["feelslikemin"], day["feelslike"],
                             day["dew"], day["humidity"], day["precip"], day["windspeed"], day["pressure"], day["cloudcover"],
                             day["visibility"], day["moonphase"]]).reshape(1, -1)
            
        pred = model.predict(data)
        
        col1,col2,col3,col4,col5 = st.columns(5)
        col3.metric("Predicted Temp(°C)", round(pred[0],2))
        getDashboard()
            
def main():
    predictTemp()       
    
if __name__ == '__main__':
    main()

