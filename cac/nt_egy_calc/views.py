from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import EnergyNew1
from django.db.models import Avg
from django.contrib.auth.decorators import login_required

# Constants for CO2 emissions calculations
GAS_CO2_FACTOR = 11.7  # lbs of CO2 per cubic foot of natural gas
ELECTRICITY_CO2_FACTOR = 0.92  # lbs of CO2 per kWh of electricity
MILES_CO2_FACTOR = 0.89  # lbs of CO2 per mile driven
AVERAGE_CO2 = 22568  # Scientifically backed average CO2 emissions in lbs

def home(request):
    """Render the home page."""
    return render(request, 'home.html')

def calculator(request):
    """Handle the CO2 emissions calculator logic."""
    if request.method == 'POST':
        try:
            # Get user input from the form
            square_footage = float(request.POST['square_footage'])
            gas_usage = float(request.POST['gas_usage'])
            electricity_usage = float(request.POST['electricity_usage'])
            miles_driven = float(request.POST['miles_driven'])  # New field for miles driven
        except ValueError:
            # If the input is invalid, display an error message
            return render(request, 'calc.html', {'error': 'Please enter valid numbers.'})

        # Calculate CO2 emissions from different sources
        co2_from_gas = gas_usage * GAS_CO2_FACTOR
        co2_from_electricity = electricity_usage * ELECTRICITY_CO2_FACTOR
        co2_from_miles = miles_driven * MILES_CO2_FACTOR
        net_co2 = co2_from_gas + co2_from_electricity + co2_from_miles

        # Save the calculated data to the database
        EnergyNew1.objects.create(
            square_footage=square_footage,
            gas_usage=gas_usage,
            electricity_usage=electricity_usage,
            miles_driven=miles_driven,
            net_co2=net_co2
        )

        # Compute average CO2 emissions from the database
        avg_co2_db = EnergyNew1.objects.aggregate(Avg('net_co2'))['net_co2__avg']

        # For comparison, use a scientifically backed average CO2 value
        avg_co2 = AVERAGE_CO2

        # Render the result page with CO2 data and averages
        return render(request, 'calc.html', {
            'net_co2': net_co2,
            'avg_co2': avg_co2,  # Scientifically backed average
            'avg_co2_db': avg_co2_db  # Database average (optional)
        })

    # Render the calculator form page for GET requests
    return render(request, 'calc.html')

def delete_data(request):
    """Delete all data from the EnergyNew1 model."""
    EnergyNew1.objects.all().delete()
    return redirect('calculator')

def recalculate(request):
    """Recalculate CO2 emissions for all entries in the database."""
    user_data = EnergyNew1.objects.all()

    for entry in user_data:
        # Recalculate CO2 emissions for each entry
        co2_from_gas = entry.gas_usage * GAS_CO2_FACTOR
        co2_from_electricity = entry.electricity_usage * ELECTRICITY_CO2_FACTOR
        co2_from_miles = entry.miles_driven * MILES_CO2_FACTOR
        entry.net_co2 = co2_from_gas + co2_from_electricity + co2_from_miles
        entry.save()

    return redirect('calculator')
from django.http import JsonResponse
import openai
from django.shortcuts import render

import os

# Set your OpenAI API key   
openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_chatgpt(request):
    if request.method == 'POST':
        user_question = request.POST.get('question')
        
        try:
            # Use the new chat_completions.create() method
            response = openai.ChatCompletion.create(
                model="gpt-4",  # Use "gpt-4" or the appropriate model
                messages=[
                    {"role": "system", "content": "You are a helpful assistant knowledgeable in climate change."},
                    {"role": "user", "content": user_question}
                ],
                max_tokens=1000,
                n=1,
                stop=None,
                temperature=0.7,
            )

            # Extract the response content
            chatgpt_response = response.choices[0].message['content'].strip()

            # Return the question and the AI's response as JSON
            return JsonResponse({
                'question': user_question,
                'response': chatgpt_response,
            })
        except Exception as e:
            # Handle any errors from OpenAI's API
            return JsonResponse({'error': str(e)})
        
    # Render the chat page for GET requests
    return render(request, 'chat.html')

"""
from .models import UserInput

def ask_chatgpt_dummy(request):
    if request.method == 'POST':
        user_question = request.POST.get('question')
        
        # Mocked response for testing
        chatgpt_response = "This is a mock response for the question: " + user_question

        # Save the question and response to the database
        UserInput.objects.create(question=user_question, response=chatgpt_response)

        # Get the last 5 entries (limit the stored inputs to 5)
        recent_inputs = UserInput.objects.all().order_by('-created_at')[:5]

        # If there are more than 5 entries, delete the oldest ones
        if UserInput.objects.count() > 5:
            UserInput.objects.order_by('created_at').first().delete()

        # Return the question and the AI's response as JSON
        return JsonResponse({
            'question': user_question,
            'response': chatgpt_response,
        })
    
    # Get the last 5 questions for display in the UI when rendering the chat page
    recent_inputs = UserInput.objects.all().order_by('-created_at')[:5]

    return render(request, 'chat.html', {
        'recent_inputs': recent_inputs,  # Pass the recent inputs to the template
    })

"""

"""
from django.shortcuts import render
from .utils import fetch_temperature_data
import json

def trends_view(request):
    api_key = "0455d98b7e08fe4b712075e952d09a21"
    city = {'lat': 37.7749, 'lon': -122.4194} 

    # Fetch temperature data
    temp_df = fetch_temperature_data(api_key, city)

    # Log the data for debugging
    print(temp_df.to_dict(orient='records'))  # Check if data is correct

    # Pass the data to the template
    return render(request, 'trends.html', {
        'temperature_data': json.dumps(temp_df.to_dict(orient='records')),
    })
"""
"""
from .utils import fetch_temperature_data
import json

import requests

def get_temperature_data():
    url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/San%20Francisco/2019-01-01/2024-01-01'
    params = {
        'unitGroup': 'metric',
        'key': '87CZ35X4Z6GFTRTLHGH8UPTRD',
        'include': 'days'
    }

    # Disable SSL certificate verification
    response = requests.get(url, params=params, verify=False)

    # Your existing processing logic
    data = response.json()
    return data
"""
from django.shortcuts import render
import json
from .utils import fetch_temperature_data  # Import the existing function from utils.py

from django.shortcuts import render
import pandas as pd
from .utils import fetch_temperature_data  # Adjust the import based on where your function is defined



def trends_view(request):
    # Manually provide the temperature data for the past 5 years (2019-2024)
    temperature_data = {
        '2019': [60, 62, 65, 68, 72, 75, 78, 77, 74, 68, 64, 61],
        '2020': [61, 63, 66, 69, 73, 76, 79, 78, 75, 69, 65, 62],
        '2021': [59, 61, 64, 67, 71, 74, 77, 76, 73, 67, 63, 60],
        '2022': [62, 64, 67, 70, 74, 77, 80, 79, 76, 70, 66, 63],
        '2023': [63, 65, 68, 71, 75, 78, 81, 80, 77, 71, 67, 64],
        '2024': [64, 66, 69, 72, 76, 79, 82, 81, 78, 72, 68, 65],
    }

    # CO2 data for 2011-2021 (3 separate rows for Coal, Petroleum Products, and Natural Gas)
    co2_data = {
        'years': ['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021'],
        'coal': [5.3, 4.2, 3.6, 3.8, 3.0, 3.1, 3.2, 3.2, 3.0, 2.7, 2.7],
        'petroleum': [222.4, 216.1, 216.5, 215.9, 224.3, 233.2, 239.3, 240.4, 239.8, 189.0, 208.1],
        'natural_gas': [115.0, 128.5, 129.6, 125.7, 124.2, 117.1, 114.1, 115.0, 115.5, 112.1, 113.3]
    }

    # Render the template with the temperature and CO2 data
    return render(request, 'trends.html', {
        'temperature_data': temperature_data,
        'co2_data': co2_data
    })



    # Render the template with the temperature and CO2 data


