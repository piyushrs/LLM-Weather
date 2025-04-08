*Disclaimer: This README is a WIP*
## Steps for getting weather API
* Sign up on [weatherapi](https://www.weatherapi.com/)
* Generate an API token

## Steps for getting the Google API token
* Go to [Google AI Studio](https://aistudio.google.com/) and sign in with your google account.
* Click on `Get API Key` to get generate your API key.
* Don't share your API key if you have entered your financial information on Google AI Studio for a higher tier API.

## Create a `.env` file in your directory and it should follow this pattern:
```
weather_api=<your_api_token>
google_api=<your_google_api_token>
```

## How to run this project?

* You can run the `llm_function_def.py`(name is temporary) in your native terminal after you place the `.env` file in same directory as this file.
* If you want to test the weather functions/ add new functions from the API, you can test them in `weather api.py` file.
