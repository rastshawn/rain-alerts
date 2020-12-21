import http.client
import json
import sys
import configparser
from datetime import datetime, timedelta


RAIN_ACCUMULATION_ALERT_LEVEL_IN_MM = 2.54 # 0.1 inches

config = configparser.ConfigParser()
config.read('config.ini')

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
        weatherData = json.loads(responseRAW.decode('utf-8'))
        values = weatherData['properties']['quantitativePrecipitation']['values']
    except:
        conn.close()

    return values

def printToGroupMe(message):
    bot_id = config['DEFAULT']['bot_id']
    conn = http.client.HTTPSConnection("api.groupme.com")
    endp = '/v3/bots/post'
    headers = {'Content-type': 'application/json'}
    payload = {'text': message, 'bot_id':bot_id}
    json_data = json.dumps(payload)
    conn.request('POST', endp, json_data, headers)
    return

def makeCall(message):
    key = config['DEFAULT']['ifttt_key']

    body = {
        'value1' : message
    }
    encodedBody = json.dumps(body).encode('utf-8')
    header = {
        "Content-Type" : "application/json; charset=utf-8",
        "Content-Length" : len(encodedBody)
    }
    try:
        conn = http.client.HTTPSConnection("maker.ifttt.com")
        conn.request("POST", '/trigger/heavy_rain_call/with/key/' + key,
            encodedBody,
            headers=header)
        httpResponse = conn.getresponse()
        conn.close()
        responseRAW = httpResponse.read()
        response = responseRAW.decode('utf-8')
        print(response)
        return response
    except Exception as e:
        postToGroupMe(e)
        conn.close()
        return

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
        printToGroupMe(totalReport)
        makeCall(totalReport)
    else:
        printToGroupMe('No serious rain.')
    return


if __name__ == "__main__":
    daily()

#     (response).properties.quantitativePrecipitation.values[]
# Each of the above is an obj: {
#     validTime: time in local time
#     value: num, mm
