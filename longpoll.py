import requests
from bs4 import BeautifulSoup as sp
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from seleniumrequests import Chrome
from config import *
import time

# Access monnit page
print("Setting up Web Driver")
chrome_options = Options()
chrome_options.add_argument("--headless")
webdriver = Chrome(r'R:\hackathon\archibus-iot-master\chromedriver.exe',options=chrome_options)
webdriver.get('https://www.imonnit.com/Account/LogonOV?ReturnUrl=/')

# Login
print("Logging in")
uname = webdriver.find_element_by_name("UserName")
pwd = webdriver.find_element_by_name("Password")
uname.send_keys(user)
pwd.send_keys(pw)
btn_xpath = '//*[@id="loginFormInside"]/div[4]/input'
login_btn = webdriver.find_element_by_xpath(btn_xpath)
login_btn.click()



# Get historical data
ids = ["488933", "488939"]#, "488935", "488937"] #Add more sensor ids as you please. comma delimited.
dictionaryOfData = {}
tables = {
    "488933" : "temperature",
    "488939" : "light",
    "488935" : "doors",
    "488937" : "motion"
}

def post_to_api(data,table):
    print("POSTing data to api")
    # django api
    apiUrl = f"http://192.168.1.2:8000/api/{table}/" #Change my IP here
    auth = ("admin","admin123")

    for item in data:
        dic = {"dateRead":item[0],"reading":item[1]}

        try:
            r=requests.post(apiUrl,auth=auth,json=dic) # POST method
        except:
            print("Already exists..maybe?")

def get_data(tables):
    # Get data
    print("Get data from sensors")
    for ID in tables:
        url = f"https://www.imonnit.com/Overview/SensorHistoryData?sensorID={ID}"
        print(f"Getting data from {tables[ID]} ({ID})...")
        r = webdriver.request('GET',url)
        soup = sp(r.content)
        dates = soup.find_all('div',{"class":["historyDate"]})
        values = soup.find_all('div',{"class":["historyReading"]})
        
        # Get text only
        formatDate = list(map(lambda x: x.text,dates))
        formatValue = list(map(lambda x: x.text,values))

        
        a=list(zip(formatDate,formatValue))[:10]
        if ID == "488935":
            print(a)
    #     print(a)
    #     # Save to dictionary using id as key and a (array) as value
        dictionaryOfData[ID] = a

        # POST
        post_to_api(a, tables[ID])

if __name__ == '__main__':
    while True:
        get_data(tables)
        print("Done. Sleeping for 10 minutes")
        time.sleep(600) # sleep for 10 min
