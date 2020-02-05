import http.client
import json
import sys

def getWeather():
    header = {"user-agent" : "Mozilla"}
    conn = http.client.HTTPSConnection("api.weather.gov")
    conn.request("GET", "/gridpoints/HGX/86,75", headers=header)
    httpResponse = conn.getresponse()
    responseRAW = httpResponse.read()
    conn.close()
    weatherData = json.loads(responseRAW)
    values = weatherData['properties']['quantitativePrecipitation']['values']
    return values

def makeCall(message):
    key = sys.argv[1]
    url = 'https://maker.ifttt.com/trigger/heavy_rain_call/with/key/' + key + '?value1="Rain tomorrow"'
    print(url) #test

if __name__ == "__main__":
    makeCall(None)
    weatherValues = getWeather()
    print(weatherValues)

#     (response).properties.quantitativePrecipitation.values[]
# Each of the above is an obj: {
#     validTime: time in local time
#     value: num, mm
