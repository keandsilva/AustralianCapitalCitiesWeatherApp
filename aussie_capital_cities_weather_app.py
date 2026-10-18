import requests
import matplotlib.pyplot as plt
Cities_list = {'Sydney': {'lat': -33.87, 'long': 151.21}, 'Melbourne': {'lat': -37.82, 'long': 144.96}, 
               'Brisbane': {'lat': -27.47, 'long': 153.03}, 'Perth': {'lat': -31.95, 'long': 115.86}, 
               'Adelaide': {'lat': -34.93, 'long': 138.60}, 'Hobart': {'lat': -42.88, 'long': 147.33},
                 'Darwin': {'lat': -12.46, 'long': 130.84}, 'Canberra': {'lat': -35.28, 'long': 149.13}}

while True:
  inputacity = input("Enter any capital city in Australia to get a glance at its weather forecast: ").strip().capitalize()

  if inputacity.lower() == 'exit':
    print("Exiting the program. Thank you for using my app!")
    break

  if inputacity in Cities_list:
    print('Location of ', inputacity, 'is', Cities_list[inputacity])
    location_value = Cities_list[inputacity]['lat'], Cities_list[inputacity]['long']
    url = f"https://api.open-meteo.com/v1/forecast?latitude={location_value[0]}&longitude={location_value[1]}&current=temperature_2m,precipitation&hourly=temperature_2m,precipitation&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=auto"
    response = requests.get(url)
    data = response.json()
    hourly_temps = data['hourly']['temperature_2m'][0:24]  # Get the first 24 hours of temperature data
    temperature = data['current']['temperature_2m']
    precip = data['current']['precipitation']
    print(f"Temperature: {temperature}°C")
    print(f"Precipitation: {precip} mm")
    
    plt.plot(hourly_temps)
    plt.title(f"Hourly Temperature Over 24 hrs for {inputacity}")
    plt.ylabel('Temp Celsius')
    plt.xlabel('Time')
    plt.xticks(range(0, 24, 2))  # Set x-ticks for each hour
    
    day = {'temperature_max': data['daily']['temperature_2m_max'], 'temperature_min': data['daily']['temperature_2m_min'], 'precipitation_sum': data['daily']['precipitation_sum']}
    
    for day in range(7):
      print(f"Day {day + 1}: Max Temp: {data['daily']['temperature_2m_max'][day]}°C, Min Temp: {data['daily']['temperature_2m_min'][day]}°C, Total Precipitation: {data['daily']['precipitation_sum'][day]} mm")
      
      print("--------------------------------------------------")
    print('Close the graph window to either continue searching for another city or type "exit" to quit the program.')
    plt.show()
  else:
    print("Please enter a CAPITAL city in AUSTRALIA! If you want to exit the program, type 'exit'.")