import http.client
import json

if __name__ == "__main__":
    header = {"user-agent" : "Mozilla"}
    conn = http.client.HTTPSConnection("api.weather.gov")
    conn.request("GET", "/gridpoints/HGX/86,75", headers=header)
    httpResponse = conn.getresponse()
    responseRAW = httpResponse.read()
    conn.close()
    weatherData = json.loads(responseRAW)
    values = weatherData['properties']['quantitativePrecipitation']['values']
    for v in values:
        print(v)

#     (response).properties.quantitativePrecipitation.values[]
# Each of the above is an obj: {
#     validTime: time in local time
#     value: num, mm
