import os
import shutil
import time
import requests
import argparse
from bs4 import BeautifulSoup as bSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# create arg for commandline
parser = argparse.ArgumentParser()
parser.add_argument("-k", "--keyword", type=str,
                    required=True, help="keyword for fb ads searches")
parser.add_argument("-l", "--location", type=str,
                    required=True, help="country or location ex. TW")
parser.add_argument("-i", "--max_iterations", type=int,
                    required=True, help="max_iterations counting times")
args = parser.parse_args()

print(args)

keyword = args.keyword
location = args.location
max_iterations = args.max_iterations

# url of fb ads library
url = "https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=" + location+"&q="+keyword + \
    "&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&search_type=keyword_unordered&media_type=all"

# define webdriver
options = FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
driver.get(url)

# main action

iterations = 0
while iterations < max_iterations:
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
