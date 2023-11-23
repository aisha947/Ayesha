# app.py
from flask import Flask, request, jsonify
import requests
from datetime import datetime, timedelta
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

app = Flask(__name__)

# Function to fetch historical weather data from OpenWeatherMap API
def fetch_weather_data(api_key, lat, lon, start_timestamp):
    base_url = 'http://api.openweathermap.org/data/2.5/onecall/timemachine'
    params = {
        'lat': lat,
        'lon': lon,
        'dt': start_timestamp,
        'appid': api_key
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    # Check if 'hourly' is present in the response
    hourly_data = data.get('hourly')
    if hourly_data is None:
        raise ValueError('Hourly data not found in the response')

    return hourly_data

# Replace 'your_openweathermap_api_key' with your actual API key
api_key = '175426c427529e38551ea0bb8af7f2e5'
lat = 40.7128  # Example latitude (New York)
lon = -74.0060  # Example longitude (New York)
start_date = datetime.now() - timedelta(days=15)
start_timestamp = int(start_date.timestamp())

try:
    historical_data = fetch_weather_data(api_key, lat, lon, start_timestamp)
    df = pd.DataFrame(historical_data)

    # Your linear regression model initialization
    model = LinearRegression()
    X = df.index.values.reshape(-1, 1)
    y = df['temp'].values  # Assuming temperature is the target variable
    model.fit(X, y)
except Exception as e:
    print(f"Error during initialization: {e}")

@app.route('/train', methods=['POST'])
def train():
    try:
        # Assuming you receive training data in the request
        # You may need to adjust this based on your actual data format
        training_data = request.json['data']

        # Train your model with the provided training data
        # For simplicity, let's assume training data is a list of temperatures
        X_train = np.arange(len(training_data)).reshape(-1, 1)
        y_train = np.array(training_data)
        model.fit(X_train, y_train)

        return jsonify({'message': 'Model trained successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict', methods=['POST'])
def api_predict():
    try:
        # Get the date for prediction from the API request
        input_date = int(request.json['date'])  # Assuming the date is represented as an index
        input_date = np.array([[input_date]])

        # Make prediction
        prediction = model.predict(input_date)

        return jsonify({'prediction': prediction[0]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

