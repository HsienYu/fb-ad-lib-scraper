import os
import shutil
import time
import requests
from bs4 import BeautifulSoup as bSoup
from selenium import webdriver

url = "https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=TW&q=nike&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&search_type=keyword_unordered&media_type=all"

# driver = webdriver.Chrome(executable_path="//")
driver = webdriver.Firefox()
driver.get(url)

iterations = 0
while iterations < 10:
    html = driver.execute_script("return document.documentElement.outerHTML")
    sel_soup = bSoup(html, 'html.parser')
    print(sel_soup.findAll('img'))
    images = []
    for i in sel_soup.findAll('img'):
        src = i['src']
        images.append(src)
    print(images)
    current_path = os.getcwd()
    for img in images:
        try:
            file_name = os.path.basename(img)
            img_r = requests.get(img, stream=True)
            new_path = os.path.join(current_path, 'images', file_name)
            with open(new_path, 'wb') as output_file:
                shutil.copyfilobj(img_r.raw, output_file)
            del img_r
        except:
            pass
    iterations += 1
    time.sleep(5)
