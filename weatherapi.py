import requests
from datetime import datetime
import api

API_ROOT = 'https://api.openweathermap.org'
API_CITY = '/data/2.5/weather?q='

def fetch_city(query):
    return requests.get(API_ROOT + API_CITY + query + api.API_KEY).json()
   # requests.get: Returns a status code, 200 means success, 404 means not found, equal to .status_code
   # .text: To get the JSON-formatted data
   # .json(): To change it from JSON text into a Python dictionary
   # Response variable have a copy of the weather data as a dictionary

# To convert the timestamp to a human-readable time (local time)
def convert_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp)

def display_weather(response):
    # Access the data in the dictionary
    city = response['name']
    weather = response['weather'][0]['main']
    temperature = (response['main']['temp'] - 273.15)
    humidity = response['main']['humidity']
    wind_speed = response['wind']['speed']
    sunrise_time = convert_timestamp(response['sys']['sunrise']).strftime('%H:%M')
    sunset_time = convert_timestamp(response['sys']['sunset']).strftime('%H:%M')
    date = convert_timestamp(response['dt']).strftime('%d-%m-%Y')
    # Print the weather report
    print(f"""
    Weather for {city} on {date}: 
    {weather}.
    Temperature: {temperature:.2f} celsius.
    Humidity: {humidity}%.
    Wind speed: {wind_speed} m/s.
    Sunrise is at: {sunrise_time} AM.
    Sunset is at: {sunset_time} PM.
    """)

def weather_dialog():
    try:
        where = ''
        while not where:
            where = input("Where in the world are you? ")
        response = fetch_city(where)
        if response['cod'] == '404':
                print("City not found. Please try again.")
                weather_dialog()
        else:
                display_weather(response)
    except requests.exceptions.ConnectionError:
        print("Couldn't connect to server! Is the network up?")

if __name__ == '__main__':
    weather_dialog()