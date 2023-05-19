import requests
import json

send_url = "http://api.ipstack.com/check?access_key=a8d32cb61d8d0c874b8f2e5a373cbe9b"
geo_req = requests.get(send_url)
geo_json = json.loads(geo_req.text)
latitude = geo_json['latitude']
longitude = geo_json['longitude']
city = geo_json['city']

print(geo_req.text)