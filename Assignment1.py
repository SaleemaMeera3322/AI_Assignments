import requests, csv, json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
access_key = os.getenv("access_key")

def get_geocode(city, country_code):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&country={country_code}&count=1"
    resp = requests.get(url, timeout=10)
    data = resp.json()
    if "results" in data and len(data["results"]) > 0:
        return data["results"][0]["latitude"], data["results"][0]["longitude"]
    return None, None

def get_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    resp = requests.get(url, timeout=10)
    data = resp.json()
    if "current_weather" in data:
        temp = data["current_weather"].get("temperature")
        wind_speed = data["current_weather"].get("windspeed")
        return temp, wind_speed
    return None, None

def get_fx_rate(from_currency, amount):
    url = f"https://api.exchangerate.host/convert?from={from_currency}&to=USD&amount={amount}&access_key={access_key}"
    resp = requests.get(url, timeout=10)
    data = resp.json()
    fx_rate = None
    amount_usd = None
    if "result" in data:
        amount_usd = data["result"]
    if "info" in data and "quote" in data["info"]:
        fx_rate = data["info"]["quote"]
    else:
        print(f"FX API warning: 'quote' missing for {from_currency}. Full response: {data}")
    return fx_rate, amount_usd

def main():
    enriched_data = []

    with open("expenses.csv", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            city = row["city"]
            country_code = row["country_code"]
            local_currency = row["local_currency"]
            amount_local = float(row["amount"])

            lat, lon = get_geocode(city, country_code)
            if lat is None or lon is None:
                print(f"Geocode not found for {city}, skipping...")
                continue

            temperature, wind_speed = get_weather(lat, lon)
            fx_rate, amount_usd = get_fx_rate(local_currency, amount_local)

            enriched_data.append({
                "city": city,
                "country_code": country_code,
                "local_currency": local_currency,
                "amount_local": amount_local,
                "fx_rate_to_usd": fx_rate,
                "amount_usd": amount_usd,
                "latitude": lat,
                "longitude": lon,
                "temperature_c": temperature,
                "wind_speed_mps": wind_speed,
                "retrieved_at": datetime.utcnow().isoformat() + "Z"
            })


    with open("enriched_expenses.json", "w") as jsonfile:
        json.dump(enriched_data, jsonfile, indent=2)

    print("enriched_expenses.json saved")

if __name__ == "__main__":
    main()