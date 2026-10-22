# Start up imports

import requests
import matplotlib.pyplot as plt
import customtkinter as ctk # type: ignore
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure




# GUI window setup

ctk.set_appearance_mode("dark")
ctk.set_window_scaling(1.5)
app = ctk.CTk()
app.title("Australian Wide Weather App v5.0")
app.geometry("600x700")
# Welcome label
ctk.CTkLabel(app, text="Welcome to Kean's Australia Wide Weather App v5.0 \n\n Type into the search bar the weather of any Australian suburb. ", font=("Arial", 20)).pack(pady=20)
ctk.CTkLabel(app, text="If you want to exit the program, type 'exit'. ", font=("Arial", 14)).pack(pady=20)

#  Entry Box for typing the City

city_entry = ctk.CTkEntry(app, width=450, height= 36, placeholder_text="Enter any suburb in Australia to get a glance at its weather forecast: ")
city_entry.pack(pady=10)

# Setting up the result label and the matplotlib figure for plotting and displaying of weather data to user
result_label = ctk.CTkLabel(app, text="", font=("Arial", 18))
result_label.pack(pady=10)
fig = plt.figure(figsize=(5, 3), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=app)



# defining the function when users hits the submit button. This function will fetch the weather data for the entered city and update the GUI accordingly.
def city_submit():
  inputacity = city_entry.get().strip().capitalize()

  geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={inputacity}&count=1&language=en&format=json&countryCode=AU"
  geo_response = requests.get(geo_url)
  geo_data = geo_response.json()

  if "results" in geo_data and len(geo_data["results"]) > 0:

    longitude = geo_data["results"][0]["longitude"]
    latitude = geo_data["results"][0]["latitude"]
    official_name = geo_data["results"][0].get("name", inputacity)

    
    ax.clear()  # Clear the previous plot if it exists
    

    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,precipitation&hourly=temperature_2m&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=auto"
    response = requests.get(url)
    data = response.json()

    hourly_temps = data['hourly']['temperature_2m'][:24]  # Get the first 24 hours of temperature data
    temperature = data['current']['temperature_2m']
    precip = data['current']['precipitation']

    weather_info = f"Current temperature in {inputacity}: {temperature}°C\nCurrent precipitation in {inputacity}: {precip} mm"
    weather_info += "\n\n7 day forecast:\n"
    for day in range(7):
          weather_info += f"Day {day + 1}: Max Temp: {data['daily']['temperature_2m_max'][day]}°C, Min Temp: {data['daily']['temperature_2m_min'][day]}°C, Precipitation: {data['daily']['precipitation_sum'][day]} mm\n"

          
    result_label.configure(text=weather_info)

    # Plotting the hourly temperature data onto the matplotlib figure
    
    
    ax.plot(hourly_temps)
    ax.set_title(f"Hourly Temperature Over 24 hrs for {inputacity}")
    ax.set_ylabel('Temp Celsius')
    ax.set_xlabel('Hour of the Day')
    ax.set_xticks(range(0, 24, 2))
    canvas.get_tk_widget().pack(pady=30) 
    canvas.draw()

    # Additional weather advice for umbrella and outfits based on precipitation and temperature
    precip = data['current']['precipitation']
    precipitation_daily = data['daily']['precipitation_sum'][0]
    if float(precip) >= 0.2 or float(precipitation_daily) >= 2:
        weather_info += f"\nUmbrella Recomended!"
    else:
        weather_info += f"\n No Umbrella Needed!"

    temperature = data['current']['temperature_2m']
    if float(temperature) <= 16:
        weather_info += f"\n\n COLD weather.\n Wear a Jacket and some long pants!"

    elif float(temperature) > 16 and float(temperature) <= 24:
        weather_info += f"\n\n MODERATE weather. \n Wear a T-shirt and pants or a light jacket and shorts!"

    elif float(temperature) > 24:
        weather_info += f"\n\n HOT weather. \n Wear a T-shirt and shorts!"
    result_label.configure(text=weather_info)
# A way to exit the program from the text box
  elif inputacity == "Exit":
    app.destroy()
    


  else:
    weather_info = f"City '{inputacity}' not found. Please enter a valid Australian suburb."
    result_label.configure(text=weather_info)
  
    # 5 Button mapping to above function

submit_button = ctk.CTkButton(app, width= 75, height=40, text="Submit", command=city_submit).pack(padx=10)



app.mainloop()
