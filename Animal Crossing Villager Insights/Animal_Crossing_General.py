# -*- coding: utf-8 -*-
"""
Created on Tue May 12 09:53:42 2020

@author: Joanna Khek Cuina
"""

#############################################
##  ANIMAL CROSSING VILLAGERS PERSONALITY  ##
#############################################
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
from selenium.webdriver.common.action_chains import ActionChains
import time 
import csv
import os
import itertools
import sys
import json

# get driver
driver = webdriver.Chrome("C:\\Users\\joann\\OneDrive\\Desktop\\My Files\\Chrome File\\chromedriver")

# get url
home_url = "https://animalcrossing.fandom.com/wiki/Villager_list_(New_Horizons)"

driver.get(home_url)

# villagers general information
time.sleep(2)
soup  = BeautifulSoup(driver.page_source, "html.parser")

table_body = soup.find("table", class_="roundy sortable jquery-tablesorter")
rows = table_body.find_all("tr")

name = []
personality = []
species = []
birthday = []
catchphrase = []
for i in range(1, len(rows)):
    cols = rows[i].find_all('td')
    cols = [x.text.strip() for x in cols]
    name.append(cols[0])
    personality.append(cols[2])
    species.append(cols[3])
    birthday.append(cols[4])
    catchphrase.append(cols[5])
    
image = []
for i in range(1, len(rows)):
    cols = rows[i].find_all("a", class_="image image-thumbnail")
    image.append(cols[0].find_all("img")[0].attrs["src"])

# create dataframe
villager_general = pd.DataFrame()
villager_general["name"] = name
villager_general["image"] = image
villager_general["personality"] = personality
villager_general["species"] = species
villager_general["birthday"] = birthday
villager_general["catchphrase"] = catchphrase
    
villager_general["name"] = villager_general["name"].replace("JacobNAJakeyPAL", "Jacob")
villager_general["name"] = villager_general["name"].replace("SporkNACracklePAL", "Spork")

# go into the villagers 
soup  = BeautifulSoup(driver.page_source, "html.parser")
image_url = []
gender = []
personality = []
species = []
birthday = []
initial_phrase = []
initial_clothes = []
home_request = []
skill = []
goal = []
coffee = []
style = []
favorite_song= []
appearances = []


for i in range(0, len(villager_general)):
    target = driver.find_element_by_link_text(villager_general["name"][i])
    driver.execute_script('arguments[0].scrollIntoView(true);', target)
    #x_cord = target.location_once_scrolled_into_view["x"]
    driver.execute_script("scrollBy(0,-200);")
    time.sleep(1)
    driver.find_elements_by_css_selector("b")[i+1].click()
    time.sleep(1)
    soup  = BeautifulSoup(driver.page_source, "html.parser")
    image = soup.find_all("a", class_="image image-thumbnail")[0].find_all("img")[0].attrs["src"]
    # image
    image_url.append(image)
    details = soup.find_all("div", class_="pi-item pi-data pi-item-spacing pi-border-color")
    
    print(villager_general["name"][i])
    print(len(details))
    
    temp_gender = []
    temp_personality = []
    temp_species = []
    temp_birthday = []
    temp_initial_phrase = []
    temp_initial_clothes = []
    temp_home_request = []
    temp_skill = []
    temp_goal = []
    temp_coffee = []
    temp_style = []
    temp_favorite_song= []
    temp_appearances = []
        
    for i in range(0, len(details)):

        attribute = soup.find_all("div", class_="pi-item pi-data pi-item-spacing pi-border-color")[i]
        
        if (attribute.attrs["data-source"] == "Gender"):
             temp_gender.append(attribute.find_all("div", class_="pi-data-value pi-font")[0].getText())
             
        elif (attribute.attrs["data-source"] == "Personality"):
            temp_personality.append(attribute.find_all("div", class_="pi-data-value pi-font")[0].getText())
            
        elif (attribute.attrs["data-source"] == "Species"):
            temp_species.append(attribute.find_all("div", class_="pi-data-value pi-font")[0].getText())
            
        elif (attribute.attrs["data-source"] == "Birthday"):
            temp_birthday.append(attribute.find_all("div", class_="pi-data-value pi-font")[0].getText())
            
        elif (attribute.attrs["data-source"] == "Initial Phrase"):
            temp_initial_phrase.append(attribute.find_all("div", class_="pi-data-value pi-font")[0].getText())
            
        elif (attribute.attrs["data-source"] == "Initial Clothes"):
            temp_initial_clothes.append(attribute.find_all("div", class_="pi-data-value pi-font")[0].getText())
            
        elif (attribute.attrs["data-source"] == "Request"):
            temp_home_request.append(attribute.find_all("div", class_="pi-data-value pi-font")[0].getText())
            
        elif (attribute.attrs["data-source"] == "Skill"):
            temp_skill.append(attribute.find_all("div", class_="pi-data-value pi-font")[0].getText())
            
        elif (attribute.attrs["data-source"] == "Goal"):
            temp_goal.append(attribute.find_all("div", class_="pi-data-value pi-font")[0].getText())
            
        elif (attribute.attrs["data-source"] == "Coffee"):
            temp_coffee.append(attribute.find_all("div", class_="pi-data-value pi-font")[0].getText())
            
        elif (attribute.attrs["data-source"] == "Style"):
            temp_style.append(attribute.find_all("div", class_="pi-data-value pi-font")[0].getText())
            
        elif (attribute.attrs["data-source"] == "Song"):
            temp_favorite_song.append(attribute.find_all("div", class_="pi-data-value pi-font")[0].getText())
            
        elif (attribute.attrs["data-source"] == "Games"):
            temp_appearances.append(attribute.find_all("div", class_="pi-data-value pi-font")[0].getText())
        
        else:
            print(attribute.attrs["data-source"])
        
    # check which one is missing
    lst_lst = [temp_gender, temp_personality, temp_species, temp_birthday, temp_initial_phrase,
           temp_initial_clothes, temp_home_request, temp_skill, temp_goal, temp_coffee, temp_style,
           temp_favorite_song, temp_appearances]
    
    for i in lst_lst:
        if len(i) == 0:
            i.append("Unknown")
            
    gender.append(temp_gender)
    personality.append(temp_personality)
    species.append(temp_species)
    birthday.append(temp_birthday)
    initial_phrase.append(temp_initial_phrase)
    initial_clothes.append(temp_initial_clothes)
    home_request.append(temp_home_request)
    skill.append(temp_skill)
    goal.append(temp_goal)
    coffee.append(temp_coffee)
    style.append(temp_style)
    favorite_song.append(temp_favorite_song)
    appearances.append(temp_appearances)
        
    time.sleep(2)
    driver.execute_script("window.history.go(-1)")
    time.sleep(2)
    


# create dataframe to store data
final = pd.DataFrame()
final["Name"] = villager_general["name"]
final["Image"] = image_url
final["Gender"] = [val for sublist in gender for val in sublist]
final["Personality"] = [val for sublist in personality for val in sublist]
final["Species"] = [val for sublist in species for val in sublist]
final["Birthday"]= [val for sublist in birthday for val in sublist]
final["Birthday"] = final["Birthday"].apply(lambda x: x.replace("April 1st (WW, CF)April 2nd (NL, HHD, NH) (Aries)", "April 2nd (Aries)"))
final["Birthday"] = final["Birthday"].apply(lambda x: x.replace("Unknown (Pisces)AFe+January 26 (Aquarius)NL", "January 26 (Aquarius)"))

horoscope = final["Birthday"].apply(lambda x: re.findall('\(.*?\)',x))
# get empty horoscope
index = []
for i in range(0, len(horoscope)):
    if not horoscope[i]:
        index.append(i)
        
horoscope[index] = list("N")
clean_horoscope = list(chain(*horoscope))
final["Horoscope"] = clean_horoscope

final["Initial_Phrase"] = villager_general["catchphrase"]
final["Initial Clothes"] = [val for sublist in initial_clothes for val in sublist]
final["Home_Request"] = [val for sublist in home_request for val in sublist]
final["Skill"] = [val for sublist in skill for val in sublist]
final["Goal"] = [val for sublist in goal for val in sublist]
final["Coffee"] = [val for sublist in coffee for val in sublist]
final["Style"] = [val for sublist in style for val in sublist]
final["Favorite_Song"] = [val for sublist in favorite_song for val in sublist]
final["Appearances"] = [val for sublist in appearances for val in sublist]

# write to file
final.to_csv("C:\\Users\\joann\\OneDrive\\Desktop\\Animal Crossing\\Data\\Villager_Complete.csv")

# download images
for i in range(0, len(final)):
    try:
        urlretrieve(final["Image"][i],"C:\\Users\\joann\\OneDrive\\Desktop\\Animal Crossing\\Image_Large\\"+ final["Name"][i] + ".png")
    except FileNotFoundError as err:
        print(err) 
    except HTTPError as err:
        print(err) 
        