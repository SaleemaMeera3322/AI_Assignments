# AI_Assignments

This repository contains Python solutions for various AI and data enrichment assignments.

## Contents

- **Assignment1.py**  
  Reads a CSV of city expenses, enriches each row using public APIs (geocoding, weather, FX rate), and outputs a JSON file.

- **Assignment2.py**  
  Provides a Flask API endpoint `/get_weather/:city` that returns the current weather for a given city using OpenWeather API.

## Usage

1. Clone the repository.
2. Install required packages:
   ```
   pip install -r requirements.txt
   ```
3. For Assignment1, place your `expenses.csv` in the repo folder and run:
   ```
   python Assignment1.py
   ```
4. For Assignment2, set your OpenWeather API key in your environment or directly in the code, then run:
   ```
   python Assignment2.py
   ```
   Access the API at `http://localhost:5000/get_weather/<city>`

## Requirements

- Python 3.10+
- requests
- flask
- python-dotenv (if using .env files)

## Notes

- Some APIs require free API keys. See code comments for details.
- Output files are saved in the repository folder.
