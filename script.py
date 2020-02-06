import http.client
import json
import sys

def getWeather():
    header = {"user-agent" : "Mozilla"}
    conn = http.client.HTTPSConnection("api.weather.gov")
    values = None
    try:
        conn.request("GET", "/gridpoints/HGX/86,75", headers=header)
        httpResponse = conn.getresponse()
        responseRAW = httpResponse.read()
        conn.close()
        weatherData = json.loads(responseRAW)
        values = weatherData['properties']['quantitativePrecipitation']['values']
    except:
        conn.close()

    return values

def makeCall(message):
    key = sys.argv[1]

    body = {
        'value1' : message
    }
    encodedBody = json.dumps(body).encode('utf-8')
    header = {
        "Content-Type" : "application/json; charset=utf-8",
        "Content-Length" : len(encodedBody)
    }
    conn = http.client.HTTPSConnection("maker.ifttt.com")
    conn.request("POST", '/trigger/heavy_rain_call/with/key/' + key,
        encodedBody,
        headers=header)
    httpResponse = conn.getresponse()
    print(httpResponse)
    conn.close()

if __name__ == "__main__":
    makeCall("I can make it say whatever I want to")
    #weatherValues = getWeather()
    #print(weatherValues)

#     (response).properties.quantitativePrecipitation.values[]
# Each of the above is an obj: {
#     validTime: time in local time
#     value: num, mm
