"""# In `utils.py` file within the same app directory as views.py
import requests
import datetime
import pandas as pd

def fetch_temperature_data(api_key, city):
    base_url = f"http://api.openweathermap.org/data/3.0/onecall/timemachine"
    today = datetime.datetime.now()
    five_years_ago = today - datetime.timedelta(days=5 * 365)

    temperature_data = []

    for i in range(5 * 365, 0, -30):
        day = today - datetime.timedelta(days=i)
        unix_timestamp = int(day.timestamp())
        url = f"{base_url}?lat={city['lat']}&lon={city['lon']}&dt={unix_timestamp}&appid={api_key}"
        response = requests.get(url)
        data = response.json()
        if 'current' in data:
            temp = data['current']['temp'] - 273.15  # Convert from Kelvin to Celsius
            temperature_data.append({'date': day.strftime('%Y-%m-%d'), 'temp': temp})
    
    return pd.DataFrame(temperature_data)

# You'd also add functions like `fetch_air_quality_data` and `fetch_co2_data` here.

import requests
import pandas as pd

def fetch_temperature_data(api_key, city):
    start_date = '2019-01-01'
    end_date = '2024-01-01'
    
    # Generate monthly dates between start_date and end_date
    date_range = pd.date_range(start=start_date, end=end_date, freq='M')  # Generates monthly data
    
    all_data = []
    
    for date in date_range:
        # API call for each date in the range
        url = f"https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={city['lat']}&lon={city['lon']}&dt={int(date.timestamp())}&appid={api_key}&units=metric"
        response = requests.get(url)
        
        # Check if API call was successful
        if response.status_code == 200:
            data = response.json()
            # Check if 'current' key is in the response and contains 'temp'
            if 'current' in data and 'temp' in data['current']:
                temp = data['current']['temp']
                all_data.append({'date': date.strftime('%Y-%m-%d'), 'temp': temp})
            else:
                all_data.append({'date': date.strftime('%Y-%m-%d'), 'temp': None})
        else:
            # If the API request fails, append None for the temperature
            all_data.append({'date': date.strftime('%Y-%m-%d'), 'temp': None})

    # Convert all_data list to pandas DataFrame
    return pd.DataFrame(all_data)
"""





import requests
import pandas as pd

# Base URL for the Visual Crossing API
BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

# Your API key for Visual Crossing
API_KEY = "87CZ35X4Z6GFTRTLHGH8UPTRD"  # Replace this with your actual API key

def fetch_temperature_data(location, start_date, end_date):
    """
    Fetches temperature data from the Visual Crossing API for a given location and date range.
    
    Parameters:
    location (str): The location to fetch weather data for.
    start_date (str): The start date of the range in 'YYYY-MM-DD' format.
    end_date (str): The end date of the range in 'YYYY-MM-DD' format.
    
    Returns:
    pd.DataFrame: A pandas DataFrame containing the date and temperature data.
    """
    # Build the full API request URL
    url = f"{BASE_URL}/{location}/{start_date}/{end_date}?unitGroup=metric&key={API_KEY}&include=days"

    try:
        # Send the GET request to the Visual Crossing API
        response = requests.get(url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            weather_data = response.json()
            print("API response received:", weather_data)  # Print for debugging
            
            # Check if the 'days' key exists in the response
            if 'days' in weather_data:
                days = weather_data['days']
                
                # Extract date and temperature data
                date_list = [day['datetime'] for day in days]
                temp_list = [day['temp'] for day in days]
                
                # Create a pandas DataFrame with the data
                temp_df = pd.DataFrame({
                    'date': date_list,
                    'temp': temp_list
                })
                
                print("Temperature data fetched successfully.")  # Debugging statement
                return temp_df
            else:
                print("No 'days' data found in the response.")
                return pd.DataFrame()  # Return empty DataFrame if no data available
        else:
            # Print the error status code and response text for debugging
            print(f"Error fetching data: {response.status_code} - {response.text}")
            return pd.DataFrame()

    except Exception as e:
        # Print any exception that occurs during the API call
        print(f"An error occurred: {e}")
        return pd.DataFrame()
