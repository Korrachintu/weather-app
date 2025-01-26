from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    error = None

    if request.method == "POST":
        city = request.form.get("city")
        if not city:
            error = "Please enter a city name."
        else:
            api_key = "4f00a21d28200ea7d5efdb727ef2ba7a"  # Replace with your OpenWeatherMap API key
            api_url = "https://api.openweathermap.org/data/2.5/weather"
            params = {"q": city, "appid": api_key, "units": "metric"}
            try:
                response = requests.get(api_url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    weather_data = {
                        "city": data["name"],
                        "temperature": data["main"]["temp"],
                        "description": data["weather"][0]["description"].capitalize(),
                        "humidity": data["main"]["humidity"],
                        "wind_speed": data["wind"]["speed"],
                    }
                elif response.status_code == 404:
                    error = "City not found. Please check the name."
                else:
                    error = "Unable to fetch weather data."
            except Exception as e:
                error = "Error connecting to the weather service."

    return render_template("index.html", weather_data=weather_data, error=error)

if __name__ == "__main__":
    app.run(debug=True)
