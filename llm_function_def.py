import os
import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
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
    This function is used to fetch current weather and the forecast using the weather 
    api and location provided by the user. You can specify the number of days for the forecast.
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

def get_current_weather(location: str) -> dict:
    '''
    This function is used to fetch current weather using the weather 
    api and location provided by the user.

    Args: 
        location (str): The location for which to fetch the weather.
    
    Returns:
        dict: The current weather data for the specified location.
    '''
    print("Fetching weather data...")
    url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": os.getenv("weather_api"),
        "q": location,
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
    

def get_aqi(location: str) -> dict:
    '''
    This function is used to fetch current weather and the AQI using the weather 
    api and location provided by the user

    Args:
        location (str): The location for which to fetch the weather and aqi information.
    
    Returns:
        dict: The current weather and AQI data for the specified location.
    '''
    print("Fetching weather data...")
    url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": os.getenv("weather_api"),
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

def call_llm(prompt: str):
    '''
    Calls the LLM
    '''

    # Function declarations for the LLM if you don't have docstrings in your functions
    # get_current_weather_function = {
    #     "name": "get_current_weather",
    #     "description": "Fetches the current weather for a specified location.",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "location": {
    #                 "type": "string",
    #                 "description": "The city or area for which to get the weather (e.g., 'London', 'Paris France').",
    #             },
    #         },
    #         "required": ["location"],
    #     },
    # }

    # get_aqi_function = {
    #     "name": "get_aqi",
    #     "description": "Fetches the air quality index for a specified location.",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "location": {
    #                 "type": "string",
    #                 "description": "The city or area for which to get the AQI (e.g., 'London', 'Paris France').",
    #             },
    #         },
    #         "required": ["location"],
    #     },
    # }

    client = genai.Client(api_key= google_api)
    # tools = types.Tool(function_declarations=[get_current_weather, get_aqi])
    # config = types.GenerateContentConfig(tools=[tools])

    # You can pass your functions directly in config for the LLM to decide which function to call.
    config = {
        "tools": [get_current_weather, get_aqi, get_weather_forecast]
    }

    chat = client.chats.create(model = "gemini-2.0-flash", config=config)
    response = chat.send_message(prompt)
    return response.text
    # response = client.models.generate_content(
    #     model="gemini-2.0-flash",
    #     contents= prompt,
    #     config=config,
    # )

    # if response.candidates[0].content.parts[0].function_call:
    #     function_call = response.candidates[0].content.parts[0].function_call
    #     print(f"Function to call: {function_call.name}")
    #     print(f"Arguments: {function_call.args}")
    # #  In a real app, you would call your function here:
    #     result = get_current_weather(**function_call.args)
    #     return result
    # else:
    #     # print("No function call found in the response.")
    #     return(response)
    
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
