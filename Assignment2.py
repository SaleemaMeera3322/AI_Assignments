from fastapi import FastAPI, HTTPException
import requests
import os
from dotenv import load_dotenv
import uvicorn

load_dotenv()
app = FastAPI()

openweatherapi_key = os.getenv("openweatherapi_key") 
api_provider = os.getenv("api_provider")


@app.get("/get_user_details")
def get_user_details(username: str):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="GitHub user not found")
    if response.status_code == 403:
        data = response.json()
        if "API rate limit exceeded" in data.get("message", ""):
            raise HTTPException(status_code=429, detail="GitHub API rate limit exceeded")
        raise HTTPException(status_code=403, detail="Forbidden access")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="server error")
    
    user = response.json()
    return {
        "login": user.get("login"),
        "name": user.get("name"),
        "public_repos": user.get("public_repos"),
        "followers": user.get("followers"),
        "following": user.get("following"),
    }

@app.get("/get_weather/{city}")
def get_weather(city: str):
    url_1 = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={openweatherapi_key}"
    response_1 = requests.get(url_1)
    data_1 = response_1.json()

    if not data_1:
        raise HTTPException(status_code=404, detail="City not found")

    lat = data_1[0]['lat']
    lon = data_1[0]['lon']

    url_2 = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={openweatherapi_key}&units=metric"
    response_2 = requests.get(url_2)
    data_2 = response_2.json()

    return {
        "city": data_2.get("name"),
        "temperature": data_2.get("main", {}).get("temp"),
        "weather_description": data_2.get("weather", [{}])[0].get("description")
    }


if __name__ == "__main__":
    uvicorn.run("Assignment2:app", host="127.0.0.1", port=8001, reload=True)