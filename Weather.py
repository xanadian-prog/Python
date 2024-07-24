import requests
import time
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# OpenWeatherMap API key
API_KEY = 'aa8eb011e79242fcb10be528aa88c52c'  # This is the OpenWeatherMap API key I got after registering on the website.
CITY = 'London'
COUNTRY = 'uk'
URL = f'http://api.openweathermap.org/data/2.5/weather?q={CITY},{COUNTRY}&appid={API_KEY}&units=metric'

def fetch_weather():
    try:
        response = requests.get(URL)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()
        
        weather_info = {
            'City': data['name'],
            'Country': data['sys']['country'],
            'Temperature (C)': data['main']['temp'],
            'Weather': data['weather'][0]['description'],
            'Humidity (%)': data['main']['humidity'],
            'Wind Speed (m/s)': data['wind']['speed'],
            'Date and Time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        return weather_info
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def log_weather_to_excel(weather_info):
    if weather_info:
        # Create a DataFrame from the weather_info dictionary
        new_data = pd.DataFrame([weather_info])
        
        try:
            # Try to read the existing Excel file
            existing_data = pd.read_excel('weather_log.xlsx')
            
            # Append the new data to the existing data
            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        except FileNotFoundError:
            # If the file does not exist, the updated_data will just be the new_data
            updated_data = new_data
        
        # Save the updated data to the Excel file
        updated_data.to_excel('weather_log.xlsx', index=False)
        print("Weather information has been logged to weather_log.xlsx")

if __name__ == "__main__":
    weather_info = fetch_weather()
    log_weather_to_excel(weather_info)

#Wait for 2 seconds before plotting the data. This will ensure that the data is actually logged in the excel file.
print("Waiting for 2 seconds...")
time.sleep(2)  # Wait for 5 seconds
print("Done waiting!")


# Load the data from the Excel file
data = pd.read_excel('weather_log.xlsx')

# Assuming the first column is for the x-axis and the second column is for the y-axis
# And the first row contains the column labels
x_label = data.columns[2]
y_label = data.columns[4]

# Extract the data for plotting
x_data = data[x_label]
y_data = data[y_label]

# Separate the last row data
x_last = x_data.iloc[-1]
y_last = y_data.iloc[-1]

# Create the scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(x_data, y_data, color='blue', edgecolors='w', s=100)
# Plot the last row data points in red
plt.scatter(x_last, y_last, color='red', edgecolors='w', s=100, label='Last Data Point')
plt.xlabel(x_label)
plt.ylabel(y_label)
plt.title('Scatter Plot of Temperature Vs Relative Humidity in London')
plt.grid(True)
plt.show()
    
