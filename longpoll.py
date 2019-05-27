import requests
from bs4 import BeautifulSoup as sp

url = "https://www.imonnit.com/Overview/SensorHistoryData"
params = {"sensorID" : "488935"}

user= "ascph2019"
pw= "archibus2019"

r = requests.get(url,auth=(user,pw),params=params)
# soup = sp(r.content,'lxml')
# dates = soup.find_all('div',{'class':['historyDate']})
# readings = soup.find_all('div',{'class':['historyReading']})
# print(dates,readings)