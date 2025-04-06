import os
import logging
from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()

# Modify this
# schedule_meeting_function = {
#     "name": "schedule_meeting",
#     "description": "Schedules a meeting with specified attendees at a given time and date.",
#     "parameters": {
#         "type": "object",
#         "properties": {
#             "attendees": {
#                 "type": "array",
#                 "items": {"type": "string"},
#                 "description": "List of people attending the meeting.",
#             },
#             "date": {
#                 "type": "string",
#                 "description": "Date of the meeting (e.g., '2024-07-29')",
#             },
#             "time": {
#                 "type": "string",
#                 "description": "Time of the meeting (e.g., '15:00')",
#             },
#             "topic": {
#                 "type": "string",
#                 "description": "The subject or topic of the meeting.",
#             },
#         },
#         "required": ["attendees", "date", "time", "topic"],
#     },
# }

def llm_function():
    get_current_weather_function = {
        "name": "get_current_weather",
        "description": "Fetches the current weather for a specified location.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city or area for which to get the weather (e.g., 'London', 'Paris France').",
                },
            },
            "required": ["location"],
        },
    }
    return get_current_weather_function

# Configure the client and tools
# client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
# tools = types.Tool(function_declarations=[get_current_weather_function])
# config = types.GenerateContentConfig(tools=[tools])

# Send request with function declarations
# response = client.models.generate_content(
#     model="gemini-2.0-flash",
#     # contents="Schedule a meeting with Bob and Alice for 03/14/2025 at 10:00 AM about the Q3 planning.",
#     contents = "What is the weather in Paris?",
#     config=config,
# )

# Check for a function call
# if response.candidates[0].content.parts[0].function_call:
#     function_call = response.candidates[0].content.parts[0].function_call
#     print(f"Function to call: {function_call.name}")
#     print(f"Arguments: {function_call.args}")
#     #  In a real app, you would call your function here:
#     #  result = schedule_meeting(**function_call.args)
# else:
#     print("No function call found in the response.")
#     print(response.text)

def call_llm(api_key: str, location: str = "Paris"):
    '''
    Calls the LLM
    '''
    get_current_weather_function = llm_function()
    client = genai.Client(api_key= api_key)
    tools = types.Tool(function_declarations=[get_current_weather_function])
    config = types.GenerateContentConfig(tools=[tools])

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"What is the weather in {location}?",
        config=config,
    )

    if response.candidates[0].content.parts[0].function_call:
        function_call = response.candidates[0].content.parts[0].function_call
        print(f"Function to call: {function_call.name}")
        print(f"Arguments: {function_call.args}")
    #  In a real app, you would call your function here:
    #  result = schedule_meeting(**function_call.args)
    else:
        print("No function call found in the response.")
        return(response.text)
    
def get_api_key():
    '''
    Gets the api key from .env file
    '''
    return os.getenv("google_api")
    
def main():
    '''
    main function for the file
    '''
    try:
        api_key = get_api_key()
    except ValueError as ve:
        logging.error(f"Configuration error: {ve}") 
    
    location = input("Enter your location: ")
    print(call_llm(api_key, location))


if __name__ == "__main__":
    main()
