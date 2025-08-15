import os
import requests

def get_api_key():
    # Prefer environment variable, fallback to .env file in root
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if api_key:
        return api_key
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.strip().startswith("OPENWEATHER_API_KEY="):
                    return line.strip().split("=", 1)[1]
    raise RuntimeError("Missing OPENWEATHER_API_KEY (set env var or put in .env at project root)")

def fetch_weather(city: str):
    api_key = get_api_key()
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    res = requests.get(url, timeout=10)
    res.raise_for_status()
    data = res.json()
    desc = data['weather'][0]['description']
    temp_c = data['main']['temp']
    return desc, temp_c

if __name__ == "__main__":
    city = input("Enter city: ")
    try:
        desc, temp_c = fetch_weather(city)
        print(f"{city} weather: {desc}, {temp_c}°C")
    except Exception as e:
        print("Error:", e)
