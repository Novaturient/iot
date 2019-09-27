import json
import requests
# import urllib

r = requests.get('https://www.imonnit.com/json/SensorDataMessages/YXNjcGgyMDE5OmFyY2hpYnVzMjAxOQ==?sensorID=488933&fromDate=2019/05/28&toDate=2019/05/28')

data = r.json()
print(data["Result"])
#print(json.dumps(data[1][0], indent=4))
