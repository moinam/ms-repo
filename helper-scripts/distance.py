import requests

url = "https://maps.googleapis.com/maps/api/distancematrix/json"

params={
  "origins": '74376-Gemmrigheim',
  "destinations": '74379-Ingersheim|74382-Neckarwestheim|74385-Pleidelsheim|74388-Talheim|74389-Cleebronn',
  "key": "API_KEY_HERE"
}
headers = {}

response = requests.request("GET", url, headers=headers, params=params)

print(response.text)

f = open("times.json", "a")
f.write(response.text)
f.close()
