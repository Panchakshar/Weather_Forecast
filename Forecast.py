import urllib.parse
import urllib.request
import json
import numpy as np
import streamlit as st
import pickle

# Load a saved model
file = open(
    'C:\\Users\lenovo\Data_Science\Projects\Weather_Forcast\weather_forecast_model.pkl', 'rb')
model = pickle.load(file)
file.close()

def predictTemp():
    API_KEY = "VRV2BXKVKNL2SGPL35GJ8UJG9"
    UNIT_GROUP = "metric"
    LOCATION = st.text_input('Location')
    d = st.date_input("Date")
    DATE = d.strftime('%Y-%m-%d')
    btn1 = st.button("Predict")
    loc = urllib.parse.quote_plus(LOCATION)
    if btn1:
        def getWeatherForecast():
            requestUrl = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/" + loc + "/"
            requestUrl = requestUrl + DATE + "?key="+API_KEY + \
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
        weatherForecast = getWeatherForecast()

        days = weatherForecast['days']
        
        for day in days:
            st.write('Date: {datetime}'.format(datetime=day['datetime']))
            st.write('Tempmax: {tempmax}'.format(tempmax=day["tempmax"]))
            st.write('Tempmin: {tempmin}'.format(tempmin=day["tempmin"]))
            st.write('Description: {description}'.format(description=day["description"]))
            
        data = np.array([day["tempmax"], day["tempmin"], day["feelslikemax"], day["feelslikemin"], day["feelslike"],
                                       day["dew"], day["humidity"], day["precip"], day["windspeed"], day["pressure"], day["cloudcover"],
                                       day["visibility"], day["moonphase"]]).reshape(1, -1)
            
        pred = model.predict(data)
        
        st.write("Predicted Temp: ",pred[0])

def main():
    st.title("Weather Forecast Webapp")
    predictTemp()
    
    
if __name__ == '__main__':
    main()

