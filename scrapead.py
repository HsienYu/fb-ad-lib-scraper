import os
import shutil
import time
import asyncio
import datetime
import requests
import argparse
import json
from bs4 import BeautifulSoup as bSoup
from colorthief import ColorThief
from colormap import rgb2hex
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
# parser.add_argument("-m", "--manual_control", type=bool,
#                     required=True, help="switch mannual  or automode")
# parser.add_argument("-cq", "--colorQuality", type=int,
#                     required=True, help="quality settings, 1 is the highest quality, the bigger the number, the faster the palette generation, but the greater the likelihood that colors will be missed.")
# parser.add_argument("-cp", "--colorPalette", type=int,
#                     required=True, help="the size of the palette, max number of colors")
args = parser.parse_args()

# print(args)

keyword = args.keyword
location = args.location
max_iterations = args.max_iterations
# manual_control = args.manual_control

# url of fb ads library
url = "https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=" + location+"&q="+keyword + \
    "&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&search_type=keyword_unordered&media_type=all"

# define webdriver
# if manual_control is True:
#     driver = webdriver.Firefox()
# else:
#     options = FirefoxOptions()
#     options.add_argument("--headless")
#     driver = webdriver.Firefox(options=options)
driver = webdriver.Firefox()
driver.get(url)


# main action

iterations = 0


def scroll(driver, timeout):
    scroll_pause_time = timeout
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # If heights are the same it will exit the function
            break
        last_height = new_height


# def appendList(entry):
#     with open("data.json", mode='r', encoding='utf-8') as f:
#         feeds = json.load(f)
#         print(feeds)

#     with open("data.json", mode='w', encoding='utf-8') as feedsjson:
#         feeds.append(entry)
#         print(json.dump(feeds, feedsjson))


def detect_color(filePath, cp):
    color_thief = ColorThief(filePath)
    # dominant_color = color_thief.get_color(quality=cq)
    palette_color = color_thief.get_palette(color_count=5)
    c_arr = []
    for c in palette_color:
        c_arr.append(rgbTohex(c))

    return c_arr


def rgbTohex(c):
    hex_color = rgb2hex(c[0], c[1], c[2])
    rm_char = hex_color.replace("#", "")
    result = rm_char.lower()

    return result


while iterations < max_iterations:
    # if manual_control is True:
    #     pass
    # else:
    #     scroll(driver, 3)
    #     print('fetching as many as possible contents in 10s each, this may takes a while!')
    scroll(driver, 3)
    print("fetching as many as possible contents in 10s each, this may takes a while!")

    html = driver.execute_script("return document.documentElement.outerHTML")
    sel_soup = bSoup(html, 'html.parser')
    # print(sel_soup.findAll('img'))
    images = []
    for i in sel_soup.findAll('img'):
        src = i['src']
        # images.append(src)
        # quick remove low resolutiona & wrong image by string find
        if src.find("s60x60") != -1 or src.find("p100x100") != -1 or src.find("KYEwFe_bozl") != -1 or src.find("hsts-pixel") != -1:
            pass
        else:
            # print(src)
            images.append(src)

    current_path = os.getcwd()
    currentDT = datetime.datetime.now()
    currentDate = currentDT.strftime("%Y/%m/%d")

    for img in images:
        try:
            file_name = os.path.basename(img)
            root_name = img.split("?")[0]
            result_name = os.path.basename(root_name)
            print(result_name, ',url=', img)
            img_r = requests.get(img, stream=True)
            new_path = os.path.join(
                current_path, 'images', result_name)
            dict = {'keyword': keyword, 'url': img,
                    'filePath': new_path, 'date': currentDate}
            with open(new_path, 'wb') as output_file:
                output_file.write(img_r.content)
                detectedColor = detect_color(dict["filePath"], 5)
                dict['color'] = detectedColor
                print(dict)

            del img_r
        except:
            pass
    iterations += 1
    time.sleep(5)
