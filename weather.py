import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from configparser import ConfigParser

def k_to_c(temp):
    return temp - 273.15

def get_weather(api_key, lat, lon):
    endpoint = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(endpoint)
    data = response.json()
    return data

def get_weather_icon(icon_code):
    return f"https://openweathermap.org/img/w/{icon_code}.png"

def extract_temperature_info(data):
    try:
        temperature_info = []

        for hours in [0, 1, 2, 3, 8]:
            weather = data['list'][hours]
            temp = round(k_to_c(weather['main']['temp']))
            time_info = datetime.utcfromtimestamp(weather['dt']).strftime('%m.%d %H:%M')
            description = weather['weather'][0]['description']
            wind_speed = weather['wind']['speed']
            humidity = weather['main']['humidity']
            icon_code = weather['weather'][0]['icon']

            if hours == 0:
                info = f"<div style='display: flex;'><div style='flex: 1;'><b>Current Temperature ({time_info}):</b> {temp} C<br><b>Description:</b> {description}<br><b>Wind Speed:</b> {wind_speed} m/s<br><b>Humidity:</b> {humidity}%</div><div style='flex: 1; text-align: right;'><img src='{get_weather_icon(icon_code)}' alt='Weather Icon' style='width: 70px;'></div></div>"
            elif hours == 8:
                info = f"<div style='display: flex;'><div style='flex: 1;'><b>Tomorrow's Temperature ({time_info}):</b> {temp} C<br><b>Description:</b> {description}<br><b>Wind Speed:</b> {wind_speed} m/s<br><b>Humidity:</b> {humidity}%</div><div style='flex: 1; text-align: right;'><img src='{get_weather_icon(icon_code)}' alt='Weather Icon' style='width: 70px;'></div></div>"
            else:
                info = f"<div style='display: flex;'><div style='flex: 1;'><b>Temperature in {hours * 3} hours ({time_info}):</b> {temp} C<br><b>Description:</b> {description}<br><b>Wind Speed:</b> {wind_speed} m/s<br><b>Humidity:</b> {humidity}%</div><div style='flex: 1; text-align: right;'><img src='{get_weather_icon(icon_code)}' alt='Weather Icon' style='width: 70px;'></div></div>"

            temperature_info.append(info)

        return '<br><br>'.join(temperature_info)

    except KeyError as e:
        print(f"KeyError: {e}")
        print("Unexpected API response structure. Please check the API response.")
        return "Error retrieving temperature information."

def send_email(subject, body, sender, receiver, password):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject

    # Add HTML part to the email body
    msg.attach(MIMEText(body, 'html'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)

if __name__ == "__main__":
    config = ConfigParser()
    config.read('config.ini')

    api_key = config.get('WeatherSettings', 'api_key')
    sender_email = config.get('WeatherSettings', 'sender_email')
    receiver_email = config.get('WeatherSettings', 'receiver_email')
    password = config.get('WeatherSettings', 'password')

    locations = {}

    for city, coordinates in config.items('Locations'):
        lat, lon = map(float, coordinates.split(','))
        locations[city] = {'lat': lat, 'lon': lon}

    email_body = ""

    for location, coordinates in locations.items():
        data = get_weather(api_key, coordinates['lat'], coordinates['lon'])
        weather_info = extract_temperature_info(data)
        email_body += f"<h2>Weather Forecast for {location.capitalize()}</h2><p>{weather_info}</p>"

    send_email("Weather Forecast", email_body, sender_email, receiver_email, password)
