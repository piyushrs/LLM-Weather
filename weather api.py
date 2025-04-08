import os
import logging
from pprint import pprint
from dotenv import load_dotenv
import requests
from requests.exceptions import RequestException, HTTPError, ConnectionError, Timeout
load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    '''
    main function for the file
    '''
    try:
        weather_api = get_api_key()
        if not weather_api:
            raise ValueError("Weather API key not found in environment variables.")
        
        loc = input("Enter your location: ")
        weather_data = get_current_weather(weather_api, loc)
        pprint(weather_data)
        forecast = get_weather_forecast(weather_api, loc, 3)
        pprint(f"Forecast for your city: \n{forecast}")

    except ValueError as ve:
        logging.error(f"Configuration error: {ve}")
    except RequestException as re:
        logging.error(f"Network error occurred: {re}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

def get_api_key():
    '''
    Gets the api key from .env file
    '''
    return os.environ.get("weather_api")

def get_current_weather(weather_api: str, location: str) -> dict:
    '''
    This function is used to fetch current weather using the weather 
    api and location provided by the user
    '''
    url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": weather_api,
        "q": location,
        "aqi": "yes"
    }
    try:
        response = requests.get(url, params, timeout = 10)
        response.raise_for_status()
        logging.info("Request to %s return status code: %s", url, response.status_code)
        return response.json()
    except HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        if response.status_code == 400:
            logging.error("Bad request. Please check the location provided.")
        return()
    except ConnectionError as conn_err:
        logging.error(f"Connection error occurred: {conn_err}")
        return()
    except Timeout as time_err:
        logging.error(f"Timeout error occurred: {time_err}")
        return()
    except RequestException as req_err:
        logging.error(f"Request error occurred: {req_err}")
        return()
    except Exception as e:
        logging.error(f"An unexpected error occurred when fetching weather data: {e}")
        return()


def get_weather_forecast(weather_api: str, location: str, days: int) -> dict:
    '''
    This function is used to fetch current weather using the weather 
    api and location provided by the user
    '''
    url = "http://api.weatherapi.com/v1/forecast.json"
    params = {
        "key": weather_api,
        "q": location,
        "aqi": "yes",
        "alerts": "yes",
        "days": 3
    }
    try:
        response = requests.get(url, params, timeout = 10)
        response.raise_for_status()
        logging.info("Request to %s return status code: %s", url, response.status_code)
        return response.json()
    except HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        if response.status_code == 400:
            logging.error("Bad request. Please check the location provided.")
        return()
    except ConnectionError as conn_err:
        logging.error(f"Connection error occurred: {conn_err}")
        return()
    except Timeout as time_err:
        logging.error(f"Timeout error occurred: {time_err}")
        return()
    except RequestException as req_err:
        logging.error(f"Request error occurred: {req_err}")
        return()
    except Exception as e:
        logging.error(f"An unexpected error occurred when fetching weather data: {e}")
        return()


if __name__ == "__main__":
    main()
