import re
import time
import paho.mqtt.client as mqtt

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

OPENHAB = 'openhabianpi'

# Data capture and upload interval in seconds. Every hour.
INTERVAL = 60

def getData():
  try:
    url = "https://pandemieende.at/"

    chrome_options = Options()  
    chrome_options.add_argument("--headless")  

    driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", chrome_options=chrome_options)
    driver.get(url)
    p_element = driver.find_element_by_id(id_='tage')

    regex = r'Noch ([\d]+) Tage'

    matches = re.search(regex, p_element.text)

    if matches:
      if matches.groups():
        data = matches.group(1);
        print ("{group}".format(group = data))

    return data.replace('.', '')
  finally:
    driver.close()


next_reading = time.time()
client = mqtt.Client()
client.connect(OPENHAB, 1883, 60)
client.loop_start()


try:
  while True:
    client.publish('meta/misc/pandemieende', getData() , 1)

    next_reading += INTERVAL
    sleep_time = next_reading-time.time()
    if sleep_time > 0:
      time.sleep(sleep_time)
except KeyboardInterrupt:
  pass

client.loop_stop()
client.disconnect()

