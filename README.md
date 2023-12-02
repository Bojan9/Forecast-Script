# Weather Forecast E-mail Script

Python script that fetches weather data for specified locations, compiles a daily weather forecast, and sends the information via email. The forecast includes current temperature, temperature in a few hours, tomorrow's temperature, along with additional details such as weather description, wind speed, humidity, and a weather icon.

This README provides instructions on how to install, configure, and run the script and/or schedule the script on Windows, Linux, and macOS.

## Requirements

- Python 3.x
- requests library (`pip install requests`)
- configparser library (`pip install configparser`)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Bojan9/Forecast-Script.git
```

2. Navigate to the project directory:

```bash
cd weather-forecast
```

3. Install required dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

- Add your OpenWeatherMap API key, email credentials, and location coordinates in the `config.ini` file.

## Usage

### Run the script

On Windows:

```bash
python weather_script.py
```

On Linux/Mac:

```bash
python3 weather_script.py
```

### Schedule the script

To schedule the script to run daily at 9 am, you can use a task scheduler:

**Windows Task Scheduler:**

- Open Task Scheduler.
- Create a new task.
- Set the trigger to daily at 9 am.
- Set the action to start a program and provide the path to the Python executable and the script.

**Linux/Mac cron job:**

- Open the crontab file:

```bash
crontab -e
```

- Add the following line to schedule the script daily at 9 am:

```bash
0 9 * * * /usr/bin/python3 /path/to/weather_script.py
```

## License

Feel free to use this script without any obligations
