# Simple Weather Fetcher

Fetches current weather for a city using OpenWeather.

**Setup (run from the *project root*, not inside `weather/`):**
1. (Recommended) create & activate a virtual env
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies from the root `requirements.txt`
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file at the project root (same folder as `requirements.txt`) with:
   ```
   OPENWEATHER_API_KEY=your_key_here
   ```

**Run:**
```bash
python weather/weather.py
```

---

# In weather/weather.py

def fetch_weather(city: str):
    api_key = get_api_key()
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        res = requests.get(url, timeout=10)
        if res.status_code == 401:
            # Common causes: key not active yet, wrong key, or account/email not verified
            raise RuntimeError(
                "OpenWeather rejected the request (401 Unauthorized). "
                "Double-check that your API key is correct, your account/email is verified, "
                "and that the key is active on your dashboard."
            )
        res.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Network/API error: {e}") from e

    data = res.json()
    desc = data['weather'][0]['description']
    temp_c = data['main']['temp']
    return desc, temp_c

---

if __name__ == "__main__":
    try:
        city = input("Enter city name: ")
        desc, temp = fetch_weather(city)
        print(f"Weather in {city}: {desc}, {temp}°C")
    except Exception as e:
        print("Error:", e)
