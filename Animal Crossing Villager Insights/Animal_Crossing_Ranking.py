# -*- coding: utf-8 -*-
"""
Created on Mon May 11 22:43:05 2020

@author: Joanna Khek Cuina
"""

#######################################################
##  ANIMAL CROSSING VILLAGER POPULARITY RANKING LIST ##
#######################################################
import numpy as np
from bs4 import BeautifulSoup
import pandas as pd
import requests
from urllib.request import urlretrieve
from urllib.error import HTTPError
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

# get driver
driver = webdriver.Chrome("C:\\Users\\joann\\OneDrive\\Desktop\\My Files\\Chrome File\\chromedriver")

# get url
home_url = "https://www.animalcrossingportal.com/games/new-horizons/guides/villager-popularity-list.php#/"

driver.get(home_url)

# get date of list updated
soup  = BeautifulSoup(driver.page_source, "html.parser")
latest_updated = soup.findAll('b')[6].getText().split("-")[0]
latest_updated_date = latest_updated.split("on")[1].strip()

print(latest_updated_date)

# villager rank, name, image, tier
driver.find_elements_by_css_selector("div[class*='u-grow u-flex']")[0].click()
soup  = BeautifulSoup(driver.page_source, "html.parser")

rank = soup.findAll("p", class_="c-villager-rank")
villager_rank = []
for i in range(0, len(rank)):
    villager_rank.append(rank[i].getText())

name = soup.findAll("p", class_="c-villager-name")
villager_name = []
for i in range(0, len(name)):
    villager_name.append(name[i].getText())
    
image = soup.findAll("div", class_="c-villager")
villager_image = []
for i in range(0, len(image)):
    villager_image.append(image[i].findAll("img")[0].attrs["src"])
    
villager_data = pd.DataFrame()
villager_data["Rank"] = villager_rank
villager_data["Name"] = villager_name
villager_data["Image"] = villager_image
villager_data["Updated Date"] = latest_updated_date

# get all the "1." index (represents the start of the new tier)
new_tier_index = villager_data[villager_data["Rank"] == "1"].index.tolist()

tier = []
for i in range(new_tier_index[0], new_tier_index[1]):
    tier.append("Tier 1")
    
for i in range(new_tier_index[1], new_tier_index[2]):
    tier.append("Tier 2")
    
for i in range(new_tier_index[2], new_tier_index[3]):
    tier.append("Tier 3")
    
for i in range(new_tier_index[3], new_tier_index[4]):
    tier.append("Tier 4")
    
for i in range(new_tier_index[4], new_tier_index[5]):
    tier.append("Tier 5")
    
for i in range(new_tier_index[5], len(villager_data)):
    tier.append("Tier 6")
    
villager_data["Tier"] = tier

# write to file
villager_data.to_csv("C:\\Users\\joann\\OneDrive\\Desktop\\Animal Crossing\\Dashboard (New)\Animal_Crossing_NEW\\Villager_Data_16_May_2020.csv")

# get image
for i in range(0, len(villager_data)):
    try:
        urlretrieve(villager_data["Image"][i],"C:\\Users\\joann\\OneDrive\\Desktop\\Animal Crossing\\Image\\"+ villager_data["Name"][i] + ".png")
    except FileNotFoundError as err:
        print(err) 
    except HTTPError as err:
        print(err) 
