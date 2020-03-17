# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 14:02:12 2020

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
downloadPath = r'C:\Users\joann\OneDrive\Desktop\My Files\Work\Newspaper Extractions\The Straits Times\\'
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

# get url
home_url = "https://www.straitstimes.com/print-edition"

# home page
driver.get(home_url)
time.sleep(2)
# logging in
driver.find_elements_by_css_selector("a[class*='mysph_login']")[0].click()
inputElement = driver.find_element_by_name("IDToken1")
inputElement.send_keys('#username here')
inputElement = driver.find_element_by_name("IDToken2")
inputElement.send_keys('#password here')
driver.find_elements_by_css_selector("button[type*='button'][id='btnLogin']")[0].click() 
time.sleep(2)

try:
    # accept cookies
    driver.find_elements_by_css_selector("button[class*='optanon-allow-all accept-cookies-button']")[0].click() 
    print("Accepted cookies")
except:
    print("No cookies detected")
    
soup  = BeautifulSoup(driver.page_source, "html.parser")
search_link_1 = soup.findAll('a', class_="block-link")
search_link_2 = soup.findAll("span", class_="story-headline")
search_link = [search_link_1, search_link_2]
        
count = 1
df_title = []
df_text = []
for links in search_link:    
    for i in range(0, len(links)):
        try:
            driver.get("https://www.straitstimes.com" + links[i]["href"])
            time.sleep(2)
            print("Downloading {}/{}".format(count, len(links)))
            soup  = BeautifulSoup(driver.page_source, "html.parser")
        except:
            driver.get("https://www.straitstimes.com" + links[i].findAll("a")[0]["href"])
            time.sleep(2)
            print("Downloading {}/{}".format(count, len(links)))
            soup  = BeautifulSoup(driver.page_source, "html.parser")
        try:
            # accept cookies
            driver.find_elements_by_css_selector("button[class*='optanon-allow-all accept-cookies-button']")[0].click() 
            print("Accepted cookies")
        except:
            print("No Cookies Detected")
    
        title = soup.findAll("h1", class_="headline node-title")[0].getText()
        print(title)
        
        # check whether it is under OPINION. Exclude it
        soup  = BeautifulSoup(driver.page_source, "html.parser")
        try:
            category = soup.findAll("li", class_="subcat-parent-link")[-1].getText()
            print(category)
        except:
            print("Unable to find category")
            category = "No Category"

        if (category != "Opinion") and (category != "Forum") and (category != "Lifestyle"):
            if "must-reads for today" in title:
                print("Detected Summary Artcile")
                count = count + 1
                
            else:
                print("Extracting Article Text")
                sub_text = []
                df_title.append(title)
                try:
                    for i in range(0,len(soup.findAll("div", itemprop="articleBody")[0].findAll("p"))):
                        sub_text.append(soup.findAll("div", itemprop="articleBody")[0].findAll("p")[i].getText())
                except:
                    for i in range(0, len(soup.findAll("div", property="content:encoded")[0].findAll("p"))):
                        sub_text.append(soup.findAll("div", property="content:encoded")[0].findAll("p")[i].getText())
                df_text.append(sub_text)
                driver.execute_script('window.print();')
                time.sleep(5)
                count = count + 1
                print("Completed")
        else:
            print("Skipping Opinion Articles")
            count = count + 1
            
# create dataframe to store the title and text
df = pd.DataFrame()
df["title"] = df_title
df["text"] = df_text
df.to_csv("C:\\Users\\joann\\OneDrive\\Desktop\\Newspaper Similarity\\data\\data_st_16_march.csv")
