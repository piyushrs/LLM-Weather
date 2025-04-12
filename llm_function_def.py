import os
import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
import logging
from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()

try:
    google_api = os.getenv("google_api")
except ValueError as ve:
    logging.error(f"Configuration error: {ve}")

def get_weather_forecast(location: str, days: int) -> dict:
    '''
    This function can be used to get the forecast, current weather and the aqi of the location that the user has provided.
    You need to input the number of days for the forecast as the user has provided.
    If the number of days are not provided by the user, you can provide a default value of 1 day.
    Always output this in a markdown table format.
    Args:
        location (str): The location for which to fetch the weather forecast.
        days (int): The number of days for the forecast.
    Returns:
        dict: The weather forecast data for the specified location.
    '''
    url = "http://api.weatherapi.com/v1/forecast.json"
    params = {
        "key": os.getenv("weather_api"),
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

# def get_current_weather(location: str) -> dict:
#     '''
#     This function is used to fetch current weather using the weather 
#     api and location provided by the user.

#     Args: 
#         location (str): The location for which to fetch the weather.
    
#     Returns:
#         dict: The current weather data for the specified location.
#     '''
#     print("Fetching weather data...")
#     url = "http://api.weatherapi.com/v1/current.json"
#     params = {
#         "key": os.getenv("weather_api"),
#         "q": location,
#     }
#     try:
#         response = requests.get(url, params, timeout = 10)
#         response.raise_for_status()
#         logging.info("Request to %s return status code: %s", url, response.status_code)
#         return response.json()
#     except HTTPError as http_err:
#         logging.error(f"HTTP error occurred: {http_err}")
#         if response.status_code == 400:
#             logging.error("Bad request. Please check the location provided.")
#         return()
#     except ConnectionError as conn_err:
#         logging.error(f"Connection error occurred: {conn_err}")
#         return()
#     except Timeout as time_err:
#         logging.error(f"Timeout error occurred: {time_err}")
#         return()
#     except RequestException as req_err:
#         logging.error(f"Request error occurred: {req_err}")
#         return()
#     except Exception as e:
#         logging.error(f"An unexpected error occurred when fetching weather data: {e}")
#         return()
    

# def get_aqi(location: str) -> dict:
#     '''
#     This function is used to fetch current weather and the AQI using the weather 
#     api and location provided by the user

#     Args:
#         location (str): The location for which to fetch the weather and aqi information.
    
#     Returns:
#         dict: The current weather and AQI data for the specified location.
#     '''
#     print("Fetching weather data...")
#     url = "http://api.weatherapi.com/v1/current.json"
#     params = {
#         "key": os.getenv("weather_api"),
#         "q": location,
#         "aqi": "yes"
#     }
#     try:
#         response = requests.get(url, params, timeout = 10)
#         response.raise_for_status()
#         logging.info("Request to %s return status code: %s", url, response.status_code)
#         return response.json()
#     except HTTPError as http_err:
#         logging.error(f"HTTP error occurred: {http_err}")
#         if response.status_code == 400:
#             logging.error("Bad request. Please check the location provided.")
#         return()
#     except ConnectionError as conn_err:
#         logging.error(f"Connection error occurred: {conn_err}")
#         return()
#     except Timeout as time_err:
#         logging.error(f"Timeout error occurred: {time_err}")
#         return()
#     except RequestException as req_err:
#         logging.error(f"Request error occurred: {req_err}")
#         return()
#     except Exception as e:
#         logging.error(f"An unexpected error occurred when fetching weather data: {e}")
#         return()

def call_llm(prompt: str):
    '''
    Calls the LLM
    '''

    client = genai.Client(api_key= google_api)

    google_search_tool = Tool(
        google_search = GoogleSearch()
    )   

    # You can pass your functions directly in config for the LLM to decide which function to call.
    # config = {
    #     "tools": [get_weather_forecast, google_search_tool]
    # }
    config=types.GenerateContentConfig(
        tools=[types.Tool(
            google_search=types.GoogleSearchRetrieval(
                dynamic_retrieval_config=types.DynamicRetrievalConfig(
                    dynamic_threshold=0.6))
        )]
    )
    chat = client.chats.create(model = "gemini-2.0-flash", config = config)
    response = chat.send_message(prompt)
    return response.text
    
def main():
    '''
    main function for the file
    '''
    while True:
        prompt = input("Enter your prompt: ")
        if prompt.lower() == "exit" or prompt.lower() == "quit" or prompt.lower() == "bye":
            break
        result = call_llm(prompt)
        print(result)
        # for chunk in result:
        #     print(chunk.text, end = "")

if __name__ == "__main__":
    main()
