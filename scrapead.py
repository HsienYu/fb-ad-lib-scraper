import os
import shutil
import time
import datetime
import requests
import argparse
from bs4 import BeautifulSoup as bSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from colorthief import ColorThief


# create arg for commandline
parser = argparse.ArgumentParser()
parser.add_argument("-k", "--keyword", type=str,
                    required=True, help="keyword for fb ads searches")
parser.add_argument("-l", "--location", type=str,
                    required=True, help="country or location ex. TW")
parser.add_argument("-i", "--max_iterations", type=int,
                    required=True, help="max_iterations counting times")
parser.add_argument("-cq", "--colorQuality", type=int,
                    required=True, help="quality settings, 1 is the highest quality, the bigger the number, the faster the palette generation, but the greater the likelihood that colors will be missed.")
parser.add_argument("-cp", "--colorPalette", type=int,
                    required=True, help="the size of the palette, max number of colors")
args = parser.parse_args()

# print(args)

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
    # print(sel_soup.findAll('img'))
    images = []
    for i in sel_soup.findAll('img'):
        src = i['src']
        images.append(src)
    current_path = os.getcwd()
    currentDT = datetime.datetime.now()
    for img in images:
        try:
            file_name = os.path.basename(img)
            root_name = img.split("?")[0]
            result_name = os.path.basename(root_name)
            # print(result_name, ',url=', img)
            img_r = requests.get(img, stream=True)
            new_path = os.path.join(
                current_path, 'images', result_name)

            with open(new_path, 'wb') as output_file:
                output_file.write(img_r.content)

            del img_r
        except:
            pass
    iterations += 1
    time.sleep(5)
