# Start up imports
import sys
import requests
import matplotlib.pyplot as plt
import customtkinter as ctk # type: ignore
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from io import BytesIO

from PIL import Image



# GUI window setup

ctk.set_appearance_mode("dark")
ctk.set_window_scaling(1.5)
app = ctk.CTk()
app.title("Australian Wide Weather App v6.0")
app.geometry("750x500")
scroll_container = ctk.CTkScrollableFrame(app, width=750, height=500)
scroll_container.pack(fill="both", expand=True,)
# Image banner for the app
image_url = "https://img.magnific.com/free-photo/dramatic-storm-clouds-water-with-breaking-light_84443-85606.jpg?semt=ais_hybrid&w=740&q=80"
image = requests.get(image_url)
image_data = BytesIO(image.content)
my_image = Image.open(image_data)

ctk_img = ctk.CTkImage(light_image=my_image, dark_image=my_image, size=(1200, 240))
image_label = ctk.CTkLabel(scroll_container, text="", image=ctk_img)
image_label.pack( pady=10)
# Welcome label
ctk.CTkLabel(scroll_container, text="Welcome to Kean's Australia Wide Weather App v6.0 \n\n Type into the search bar the weather of any Australian suburb. ", font=("Arial", 20)).pack(pady=20)
ctk.CTkLabel(scroll_container, text="If you want to exit the program, type 'exit'. ", font=("Arial", 14)).pack(pady=20)
input_frame = ctk.CTkFrame(scroll_container, fg_color="transparent")
input_frame.pack(pady=10)


#  Entry Box for typing the City

city_entry = ctk.CTkEntry(input_frame, width=450, height= 36, placeholder_text="Enter any suburb in Australia to get a glance at its weather forecast: ")
city_entry.pack(pady=10, side="left", padx=10)

# Setting up the result label and the matplotlib figure for plotting and displaying of weather data to user
result_label = ctk.CTkLabel(scroll_container, text="", font=("Arial", 18))
result_label.pack(pady=10)
fig = plt.figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=scroll_container)
# Custom scroll function to make sure speed of scrolling is consistent across different desktop platforms
def custom_scroll(event):
    if sys.platform == "darwin":  # macOS trackpads/mice
       
        scroll_amount = int(-1 * (event.delta * 0.1)) 
    else:  # Windows/Linux
        
        scroll_amount = int(-1 * (event.delta / 360))
        
    scroll_container._parent_canvas.yview_scroll(scroll_amount, "units")

# 3. Bind it globally to the container
scroll_container.bind_all("<MouseWheel>", custom_scroll)



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

submit_button = ctk.CTkButton(input_frame, width= 75, height= 36, text="Submit", command=city_submit)
submit_button.pack(side='right', padx=10)



app.mainloop()
