from selenium import webdriver
from datetime import datetime
from pyperclip import paste
from selenium.webdriver.chrome.options import Options
import pyautogui
import time
import bs4
import urllib.request
import urllib.parse
import re
import os
import mouse

options = Options()
homepath = os.path.expanduser('~')
options.add_argument("--allow-profiles-outside-user-dir")
options.add_argument("user-data-dir=" + homepath + "\\AppData\\Local\\Google\\Chrome\\User Data")
options.add_argument("--profile-directory=Profile 1")
options.add_argument("--disable-gpu")
options.add_argument("--disable-notifications")
driver=webdriver.Chrome()
url = 'https://slovnik.seznam.cz/preklad/rusky_cesky/'
csv_file = open('CZ ' + datetime.now().strftime("%d.%m") + '.txt', 'a+', newline='', encoding="utf-8")

def copy_clipboard():
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(.1)
    word = paste()
    driver.get(url + word)
    print(word)
    # Get and parse html
    quoted = urllib.parse.quote(word) # for cz symbols
    get = urllib.request.urlopen(url + quoted) # get url
    html_page = get.read()
    soup = bs4.BeautifulSoup(html_page, 'lxml')
    infinitive = soup.h1.span.text
    translate = soup.li.span.text
    # Checking and writing in file
    csv = (infinitive + ',' + translate)
    csv = re.sub(r', ', r'/', csv)
    csv = re.sub(r',(\(.*[^А-я]\)) ', r' \1,', csv)
    with open('CZ ' + datetime.now().strftime("%d.%m") + '.txt', 'r', encoding="utf-8") as file:
        check = csv in file.read()
    if check == True:
        print("(repeat)")
        return
    print(csv)
    csv_file.write(csv + '\n')
    csv_file.flush()
    return

mouse.on_double_click(copy_clipboard)
input()
