#!/usr/bin/env python
# coding: utf-8

# ## What we want
# * Temperature (F) vs. Latitude
# * Humidity (%) vs. Latitude
# * Cloudiness (%) vs. Latitude
# * Wind Speed (mph) vs. Latitude
# 
# ## Notes
# ### API response from weather API
# ```
# {"coord":
# {"lon":145.77,"lat":-16.92},
# "weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04n"}],
# "base":"cmc stations",
# "main":{"temp":293.25,"pressure":1019,"humidity":83,"temp_min":289.82,"temp_max":295.37},
# "wind":{"speed":5.1,"deg":150},
# "clouds":{"all":75},
# "rain":{"3h":3},
# "dt":1435658272,
# "sys":{"type":1,"id":8166,"message":0.0166,"country":"AU","sunrise":1435610796,"sunset":1435650870},
# "id":2172797,
# "name":"Cairns",
# "cod":200}
# ```
# 

# # WeatherPy
# ----
# 
# ### Analysis
# * As expected, the weather becomes significantly warmer as one approaches the equator (0 Deg. Latitude). More interestingly, however, is the fact that the southern hemisphere tends to be warmer this time of year than the northern hemisphere. This may be due to the tilt of the earth.
# * There is no strong relationship between latitude and cloudiness. However, it is interesting to see that a strong band of cities sits at 0, 80, and 100% cloudiness.
# * There is no strong relationship between latitude and wind speed. However, in northern hemispheres there is a flurry of cities with over 20 mph of wind.
# 
# ---
# 
# #### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[62]:


# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time

# Import API key
from api_keys import api_key

# Incorporated citipy to determine city based on latitude and longitude
from citipy import citipy

# Output File (CSV)
output_data_file = "output_data/cities.csv"

# Range of latitudes and longitudes
lat_range = (-90, 90)
lng_range = (-180, 180)


# ## Generate Cities List

# In[63]:


# List for holding lat_lngs and cities
lat_lngs = []
cities = []

# Create a set of random lat and lng combinations
lats = np.random.uniform(low=-90.000, high=90.000, size=1500)
lngs = np.random.uniform(low=-180.000, high=180.000, size=1500)
lat_lngs = zip(lats, lngs)

# Identify nearest city for each lat, lng combination
for lat_lng in lat_lngs:
    city = citipy.nearest_city(lat_lng[0], lat_lng[1]).city_name
    
    # If the city is unique, then add it to a our cities list
    if city not in cities:
        cities.append(city)

# Print the city count to confirm sufficient count
len(cities)


# ### Perform API Calls
# * Perform a weather check on each city using a series of successive API calls.
# * Include a print log of each city as it'sbeing processed (with the city number and city name).
# 

# In[64]:


def get_city_data(city_name):
    encoded_city_name = city_name.replace(" ", "+")
    url = f"http://api.openweathermap.org/data/2.5/weather?appid={api_key}&q={encoded_city_name}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    else:
        return response.json()
    


# In[67]:


print('Beginning Data Retrieval')     
print('-----------------------------')
responses = []
for index, city in enumerate(cities):
    print(f"Processing Record {index} | {city}")
    result = get_city_data(city)
    if result is None:
        print('City not found. Skipping...')
    else:
        responses.append(result)
print('-----------------------------')
print('Data Retrieval Complete')      
print('-----------------------------')

print("Finished, total count = ", len(responses))


# In[68]:


# Put all the data we're interseted in into a data frame
df = pd.DataFrame(columns=["City", "Cloudiness", "Country", "Date", 
                           "Humidity", "Lat", "Lng", "Max Temp", 
                           "Wind Speed"])

def get_row_from_response(response):
    city = response['name']
    cloudiness = response['clouds']['all']
    country = response['sys']['country']
    date = response['dt']
    humidity = response['main']['humidity']
    lat = response['coord']['lat']
    lng = response['coord']['lon']
    max_temp = response['main']['temp_max']
    wind_speed = response['wind']['speed']
    
    return {"City" : city, "Cloudiness": cloudiness, 
            "Country" : country, "Date": date, 
            "Humidity": humidity, "Lat": lat, 
            "Lng": lng, "Max Temp": max_temp, 
            "Wind Speed": wind_speed}

print('-----------------------------')
print('Adding responses to data frame')      
print('-----------------------------')
for response in responses:
    df = df.append(get_row_from_response(response), ignore_index=True)

print("Finished, df size = ", len(df))


# ### Convert Raw Data to DataFrame
# * Export the city data into a .csv.
# * Display the DataFrame

# In[69]:


print('Exporting to csv...')
df.to_csv(output_data_file)
print('Finished exporting')


# In[70]:


print(df.count())


# In[71]:


df.head()


# ### Plotting the Data
# * Use proper labeling of the plots using plot titles (including date of analysis) and axes labels.
# * Save the plotted figures as .pngs.

# #### Latitude vs. Temperature Plot

# In[72]:


df2 = pd.read_csv("output_data/cities.csv", sep=",")
ax = df2.plot.scatter(x="Lat", y="Max Temp")
ax.set(xlabel='Latitude', ylabel='Max Temperature (F)')
plt.show()


# #### Latitude vs. Humidity Plot

# In[73]:


ax2 = df2.plot.scatter(x='Lat', y='Humidity')
ax2.set(xlabel='Latitude', ylabel='Humidity (%)')
plt.show()


# #### Latitude vs. Cloudiness Plot

# In[74]:


ax3 = df2.plot.scatter(x='Lat', y='Cloudiness')
ax3.set(xlabel='Latitude', ylabel='Cloudiness (%)')
plt.show()


# #### Latitude vs. Wind Speed Plot

# In[75]:


ax4 = df2.plot.scatter(x='Lat', y='Wind Speed')
ax4.set(xlabel='Latitude', ylabel='Wind Speed (mph)')
plt.show()


# In[ ]:




