import http.client
import json
import sys
from datetime import datetime, timedelta


RAIN_ACCUMULATION_ALERT_LEVEL_IN_MM = 2.54 # 0.1 inches

def getMonthString(num):
    ret = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    return ret[num - 1]

def getDateString(num):
    ret = ['first',
    'second', 
    'third',
    'fourth',
    'fifth', 
    'sixth', 
    'seventh', 
    'eighth',
    'ninth',
    'tenth',
    'eleventh',
    'twelfth',
    'thirteenth',
    'fourteenth', 
    'fifteenth', 
    'sixteenth',
    'seventeenth',
    'eighteenth',
    'nineteenth',
    'twentieth',
    'twenty first',
    'twenty second', 
    'twenty third', 
    'twenty fourth', 
    'twenty fifth', 
    'twenty sixth', 
    'twenty seventh', 
    'twenty eighth', 
    'twenty ninth', 
    'thirtieth', 
    'thirty first']
    return ret[num-1]
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
    conn.close()
    return httpResponse.read()


def daily():
    concern = []
    weatherValues = getWeather()
    for weather in weatherValues:
        if (weather['value'] > RAIN_ACCUMULATION_ALERT_LEVEL_IN_MM):
            concern.append(weather)
    
    reportValues = []
    if (len(concern) > 0):
        for val in concern:
            # Extract the time from the objects that come back.
            # The time listed is when the period of rain ENDS.
            # Values come back in 6-hour batches.
            # Subtract 6 hours from each value to get the start time for the rain
            readTime = datetime.strptime(val['validTime'], '%Y-%m-%dT%H:%M:%S+00:00/PT6H')
            adjustedTime = readTime - timedelta(hours=6)
            
            reportString = 'There will be --- ' + str(val['value']) \
                + ' millimeters of rain starting at ' + str(adjustedTime.hour) + \
                ' o clock on ' + getMonthString(adjustedTime.month) + ' ' + getDateString(adjustedTime.day) + ' --- ---'
            reportValues.append(reportString)
    totalReport = 'There will be heavy rain in the next few days. '
    totalReport += ''.join(reportValues)
    print(totalReport)
    #makeCall(totalReport)
    return


def hourly():
    return

if __name__ == "__main__":
    #makeCall("I can make it say whatever I want to")
    if (len(sys.argv) > 2 and sys.argv[2] == "daily"):
        daily()
    hourly()
    #weatherValues = getWeather()
    #print(weatherValues)

#     (response).properties.quantitativePrecipitation.values[]
# Each of the above is an obj: {
#     validTime: time in local time
#     value: num, mm
