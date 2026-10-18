import requests
Cities_list = {'Sydney': {'lat': -33.87, 'long': 151.21}, 'Melbourne': {'lat': -37.82, 'long': 144.96}, 
               'Brisbane': {'lat': -27.47, 'long': 153.03}, 'Perth': {'lat': -31.95, 'long': 115.86}, 
               'Adelaide': {'lat': -34.93, 'long': 138.60}, 'Hobart': {'lat': -42.88, 'long': 147.33},
                 'Darwin': {'lat': -12.46, 'long': 130.84}, 'Canberra': {'lat': -35.28, 'long': 149.13}}
while True:
  inputacity = input("Enter any capital city in Australia to look at its weather: ").strip().capitalize()

  if inputacity.lower() == 'exit':
    print("Exiting the program. Thank you for using the weather app!")
    break

  if inputacity in Cities_list:
    print('Location of ', inputacity, 'is', Cities_list[inputacity])
    location_value = Cities_list[inputacity]['lat'], Cities_list[inputacity]['long']
    url = f"https://api.open-meteo.com/v1/forecast?latitude={location_value[0]}&longitude={location_value[1]}&current=temperature_2m,precipitation"
    response = requests.get(url)
    data = response.json()
    temperature = data['current']['temperature_2m']
    precip = data['current']['precipitation']
    print(f"Temperature: {temperature}°C")
    print(f"Precipitation: {precip} mm")
  else:
    print("Please enter a CAPITAL city in AUSTRALIA! If you want to exit the program, type 'exit'.")
