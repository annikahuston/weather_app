
'''
Name: Annika Huston
'''
from bs4 import BeautifulSoup
import requests
from datetime import datetime, date, timedelta
import matplotlib.pyplot as plt

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

def get_weather(city):
    #current weather
    current = []
    city_weather = city + ' weather'
    #retrieve city weather data from google
    res = requests.get(f'https://www.google.com/search?q={city_weather}&oq={city_weather}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8', headers=headers)
    res_html = res.text
    soup = BeautifulSoup(res_html, 'html.parser')
    loc = soup.select('#wob_loc')[0].getText().strip()
    day_time = soup.select('#wob_dts')[0].getText().strip()
    temp = soup.select('#wob_tm')[0].getText().strip()
    prec = soup.select('#wob_pp')[0].getText().strip()
    humidity = soup.select('#wob_hm')[0].getText().strip()
    current.extend([loc, day_time, temp, prec, humidity])
    

    #future weather
    future = []
    days = soup.find("div", attrs={"id": "wob_dp"})
    for day in days.findAll("div", attrs={"class": "wob_df"}):
        # extract the name of the day
        day_name = day.findAll("div")[0].attrs['aria-label']
        # get weathe
        weather = day.find("img").attrs["alt"]
        temp = day.findAll("span", {"class": "wob_t"})
        max_t = temp[0].text
        min_t = temp[2].text
        future.append([day_name, weather, max_t, min_t])
        
    return current, future

def column(matrix, i):
    return [row[i] for row in matrix]

def data_analysis(future):
    #Using meteostat to access open weather and climate data
    start = date.today()
    end = start + timedelta(days=7)
    #Calculate future average
    future_avg = sum([(int(future[i][2]) + int(future[i][3]))/2 for i in range(8)])/8

    rain = False
    r_count = 0
    snow = False
    s_count = 0
    for weath in column(future, 1):
        if 'snow' in weath:
            snow = True
            s_count += 1
        if 'rain' in weath or 'showers' in weath:
            rain = True
            r_count += 1
    
        
    return(future_avg, rain, r_count, snow, s_count)

    
def main():
    city = input('Enter a city name to get weather report: ')
    current, future = get_weather(city)
    print("\nCurrent Weather:")
    print(f'Location->\t{current[0]}')
    print(f'Day and Time->\t{current[1]}')
    print(f'Tempurature->\t{current[2]}')
    print(f'Precipitation->\t{current[3]}')
    print(f'Humidity->\t{current[4]}\n')
    print("==============================================")
    print("Weekly Forecast")
    for i in range(8):
        if i < 7:
            print(f'{"Day->":15}{future[i][0]}')
            print(f'{"Weather->":15}{future[i][1]}')
            print(f'{"Low Temp->":15}{future[i][3]}')
            print(f'{"High Temp->":15}{future[i][2]}')
            print('______________________________________________')
        else:
            print(f'{"Day->":15}{future[i][0]}')
            print(f'{"Weather->":15}{future[i][1]}')
            print(f'{"Low Temp->":15}{future[i][3]}')
            print(f'{"High Temp->":15}{future[i][2]}')
            print('==============================================\n')

    print("Weekly Analysis")
    f_avg, rain, r_ct, snow, s_ct = data_analysis(future)
    if f_avg >95:
        print("Stay inside this week! Average Tempurature is ", f_avg, " degrees Farenheit")
    elif f_avg >75:
        print("Get ready for some warm weather this week. Average Tempurature is ", f_avg, " degrees Farenheit")
    elif f_avg > 40:
        print("A little chilly this week. A light jacket is needed. Average Tempurature is ", f_avg, " degrees Farenheit")
    else:
        print("BRRRRRR chilly week! Average Tempurature is ", f_avg, " degrees Farenheit")

    if rain:
        print("Be sure to bring a rain jacket. There's ", r_ct, " rain day(s) this week")
    if snow:
        print("Put your chains on and layer up. There's ", s_ct, " snow day(s) this week")

main()
