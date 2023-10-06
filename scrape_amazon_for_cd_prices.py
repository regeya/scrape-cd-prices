#!!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from stem import Signal
from stem.control import Controller
import re
ua = UserAgent()
user_agent = ua.random

options = Options()
#options.add_argument('--headless')
#options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--proxy-server=socks5://localhost:9050')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--disable-extensions")
options.add_argument(f'user-agent={user_agent}')
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])

#chrome_driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
#driver = webdriver.Chrome(ChromeDriverManager().install())
driver = webdriver.Chrome(options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.implicitly_wait(10)

from bs4 import BeautifulSoup
from six.moves import urllib
import requests, csv, random, time
 
#File = open("out.csv", "a")

TOR_PWD="5mcydnat"

def change_ip_address(password):
    """Change IP address over Tor connection
    :type password: str
    :param password: Tor authentication password
    """
    print("Changing ip address...")
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password=password)
        controller.signal(Signal.NEWNYM)

def open_amazon_page(my_url):
    driver.get(my_url)
    time.sleep(1)
    try:
        price = driver.find_element('xpath', './/span[@class="a-offscreen"]').get_attribute('textContent')
    except:
        price = "N/A"
    textbody = driver.find_element('xpath','//*[@id="detailBullets_feature_div"]').get_attribute('textContent')
    print(textbody)
    releaseDateRegex = re.compile(r'Available\s+\:\s+.*(\d\d\d\d)',re.MULTILINE + re.DOTALL)
    releaseDate = releaseDateRegex.search(textbody)
    print(releaseDate)
    print(releaseDate.group(1))
    return price
    
    
def find_first_google_link(my_terms):
    driver.get('https://duckduckgo.com/')
    search_box = driver.find_element('name','q')
    search_box.send_keys(my_terms)
    search_box.submit()
    time.sleep(2)
    links = driver.find_elements('xpath','//*/div[2]/h2/a')
#
#    //*[@id="ra-1"]/div[2]/h2/a

    print(links)
    #links = driver.find_elements('xpath', '//*/div[@id="search"]/div/div/div[1]/div/div/div[1]/div/a')
    link = links[0]
    result = link.get_attribute('href')
    return result

with open("/mnt/shared/paste_albums_list.csv", "w") as outfile:
    writer = csv.writer(outfile)
    with open('/home/shane/Downloads/albums_list.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
        random.shuffle(rows)
        for row in rows:
            change_ip_address(TOR_PWD)
            mytitle = row[0]
            myartist = row[1]
            mylink = find_first_google_link(f"site:amazon.com cd {myartist} {mytitle}")
            print(mylink)
            myprice = open_amazon_page(mylink)
            print(f"{myartist} - {mytitle} {myprice}")
            time.sleep(random.uniform(2,8))
            writer.writerow(["Living", "", myartist, mytitle, 1, 10, "", myprice, "", "store", "cash"])



