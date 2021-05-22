import re
import paho.mqtt.client as mqtt

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

OPENHAB = 'openhabianpi'

def getData():
  url = "https://pandemieende.at/"

  chrome_options = Options()
  chrome_options.add_argument("--headless")

  driver = webdriver.Chrome("/usr/bin/chromedriver", chrome_options=chrome_options)
  try:
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


client = mqtt.Client()
client.connect(OPENHAB, 1883, 60)
client.loop_start()

client.publish('meta/misc/pandemieende', getData() , 1)

client.loop_stop()
client.disconnect()

