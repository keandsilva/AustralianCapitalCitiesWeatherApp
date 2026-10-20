import requests
import matplotlib.pyplot as plt
import customtkinter as ctk # type: ignore
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


# cities dictionary with their latitude and longitude coordinates

Cities_list = {'Sydney': {'lat': -33.87, 'long': 151.21}, 'Melbourne': {'lat': -37.82, 'long': 144.96}, 
               'Brisbane': {'lat': -27.47, 'long': 153.03}, 'Perth': {'lat': -31.95, 'long': 115.86}, 
               'Adelaide': {'lat': -34.93, 'long': 138.60}, 'Hobart': {'lat': -42.88, 'long': 147.33},
                 'Darwin': {'lat': -12.46, 'long': 130.84}, 'Canberra': {'lat': -35.28, 'long': 149.13}}

# GUI window setup

ctk.set_appearance_mode("dark")
ctk.set_window_scaling(1.5)
app = ctk.CTk()
app.title("Australian Capital Cities Weather App v3.0")
app.geometry("600x700")
# Welcome label
ctk.CTkLabel(app, text="Welcome to Kean's Australian Capital Cities Weather App v3.0", font=("Arial", 20)).pack(pady=20)

#  3 Entry Box for typing the City

city_entry = ctk.CTkEntry(app, width=450, height= 36, placeholder_text="Enter any capital city in Australia to get a glance at its weather forecast: ")
city_entry.pack(pady=10)
result_label = ctk.CTkLabel(app, text="", font=("Arial", 20))
result_label.pack(pady=10)
fig = plt.figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=app)


def city_submit():
  inputacity = city_entry.get().strip().capitalize()
  if inputacity in Cities_list:
    ax.clear()  # Clear the previous plot if it exists
    
    latitude = Cities_list[inputacity]['lat']
    longitude = Cities_list[inputacity]['long']
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
    
    
    ax.plot(hourly_temps)
    ax.set_title(f"Hourly Temperature Over 24 hrs for {inputacity}")
    ax.set_ylabel('Temp Celsius')
    ax.set_xlabel('Hour of the Day')
    ax.set_xticks(range(0, 24, 2))
    canvas.get_tk_widget().pack(pady=30) 
    

    
    canvas.draw()

  else:
    weather_info = f"City '{inputacity}' not found. Please enter a valid Australian capital city."
    result_label.configure(text=weather_info)
  
    # 5 Button mapping to above function

submit_button = ctk.CTkButton(app, width= 50, height=50, text="Submit", command=city_submit).pack(pady=10)



app.mainloop()