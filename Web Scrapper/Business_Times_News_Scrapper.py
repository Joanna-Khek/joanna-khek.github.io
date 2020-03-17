# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 11:46:10 2020

@author: Joanna Khek Cuina
"""

import numpy as np
from bs4 import BeautifulSoup
import pandas as pd
import requests
from urllib.request import urlopen
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time 
import csv
import os
import itertools
import sys
import json

# adjust CHROME settings
downloadPath = r'C:\Users\joann\OneDrive\Desktop\My Files\Work\Newspaper Extractions\The Business Times\\'
chrome_options = webdriver.ChromeOptions()
appState = {
"recentDestinations": [
    {
        "id": "Save as PDF",
        "origin": "local",
        "account": "",
    }
],
"selectedDestinationId": "Save as PDF",
"version": 2
}

profile = {'printing.print_preview_sticky_settings.appState':json.dumps(appState),'savefile.default_directory':downloadPath}
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('prefs', profile)
chrome_options.add_argument('--kiosk-printing')
chrome_options.add_argument("--start-maximized")

# get driver
driver = webdriver.Chrome("C:\\Users\\joann\\OneDrive\\Desktop\\My Files\\Chrome File\\chromedriver", chrome_options=chrome_options)

# url
home_url = "https://www.businesstimes.com.sg/"

# open chrome
driver.get(home_url)
time.sleep(10)

# logging in
driver.find_elements_by_css_selector("li[class*='header-home-group login-link']")[0].click()
inputElement = driver.find_element_by_name("IDToken1")
inputElement.send_keys('#username here')
inputElement = driver.find_element_by_name("IDToken2")
inputElement.send_keys('#password here')
driver.find_elements_by_css_selector("button[type*='button'][id='btnLogin']")[0].click() 
time.sleep(2)

# all news
today_url = 'https://www.businesstimes.com.sg/todays-paper'
driver.get(today_url)
time.sleep(2)

try:
    #accept cookies
    driver.find_elements_by_css_selector("button[class*='optanon-allow-all accept-cookies-button']")[0].click() 
    time.sleep(1)
    print("Accepted cookies")
     
except:
    print("Unable to accept cookies")
    
soup  = BeautifulSoup(driver.page_source, "html.parser")

# get all links
search_links = []
for i in range(0, len(soup.findAll("div", class_="cps-region-inner")[0].findAll("h3"))):
    for j in range(0, len(soup.findAll("div", class_="cps-region-inner")[0].findAll("h3")[i].findAll("a"))):
        search_links.append(soup.findAll("div", class_="cps-region-inner")[0].findAll("h3")[i].findAll("a")[j]["href"])

df_title = []
df_text = []

count = 1
for i in range(0, len(search_links)):
    print("Download {}/{}".format(count, len(search_links)))
    driver.get("https://www.businesstimes.com.sg" + search_links[i])
    time.sleep(5)
    soup  = BeautifulSoup(driver.page_source, "html.parser")
    # handle cookies
    try:
        #accept cookies
        driver.find_elements_by_css_selector("button[class*='optanon-allow-all accept-cookies-button']")[0].click() 
        time.sleep(1)
        print("Accepted cookies")
     
    except:
        print("No cookies")
    
    time.sleep(5)
    try:
        df_title.append(soup.findAll("div", property="schema:name")[0].getText())
    except:
        df_title.append("Unable to find Title")
        
    text = []
    print("Extracting Article Text")
    try:
        for i in range(0, len(soup.findAll("div", class_="field field-name-body field-type-text-with-summary field-label-hidden")[0].findAll("p"))):
            text.append(soup.findAll("div", class_="field field-name-body field-type-text-with-summary field-label-hidden")[0].findAll("p")[i].getText())
    except:
        for i in range(0, len(soup.findAll("div", class_="body")[0].findAll("p"))):
            text.append(soup.findAll("div", class_="body")[0].findAll("p")[i].getText())
    df_text.append(text)
    driver.execute_script('window.print();')
    time.sleep(2)
    count = count + 1
    
# save to dataframe
df = pd.DataFrame()
df["title"] = df_title
df["text"] = df_text
df.to_csv("C:\\Users\\joann\\OneDrive\\Desktop\\Newspaper Similarity\\data\\data_bt_16_march.csv")
