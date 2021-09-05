'''
Main Purpose: To scrape all the mpg values of car at https://fueleconomy.gov and use it in an AI competition hosted by NNPC and DSN
Creator: Muhammad Aliyu (TEAM C)
Date of Creation: Sunday August 31, 2021

At the time this webscraping algorithm is made, it can scraped all the mpg values of 5254 car from https://car45.com

The number Zero in the mpg feature refer to a missing value
'''

import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re

print("Started Running Script")

browser = webdriver.Chrome(executable_path="chromedriver.exe")
browser.maximize_window()

class Request:
    def __init__(self, url):
        self.url = url
        self.counter = 0
    def get_url(self, make, model):
        self.counter += 1
        browser.get("{0}{1}+{2}".format(self.url, make, model))
        WebDriverWait(browser, 60).until(
            EC.presence_of_element_located((By.CLASS_NAME, "total-links"))
        )
    def get_single_url_data(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        result = soup.find("td", "combinedMPG")
        return result

req = Request("https://fueleconomy.gov/feg/search.shtml?words=")
# all url for each car in the fueleconomy website
url = "https://fueleconomy.gov"
all_mpg = []
already_find_cars_model_dict = {}
# load car45 csv
car45 = pd.read_csv("car45.csv")
for i in range(len(car45)):
    make = car45.iloc[i]["Make"]
    model = car45.iloc[i]["Model"]
    # Get each page url
    try:
        if(model in already_find_cars_model_dict):
            all_mpg.append(already_find_cars_model_dict[model])
            req.counter += 1
            mpg = "{0} already exist - {1}".format(already_find_cars_model_dict[model], model)
        else:
            req.get_url(make, model)
            text = browser.find_element_by_id("results").text
            if("Found 0 results" in text):
                all_mpg.append(0)
                already_find_cars_model_dict[model] = 0
                req.counter += 1
                continue
            urls = re.findall('/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
            uri = "{0}{1}".format(url, urls[0])
            # get the car mpg from this link
            mpg = req.get_single_url_data(uri).get_text()
            mpg = ''.join([s for s in mpg.split(":") if s.isdigit()])
            all_mpg.append(mpg)
            already_find_cars_model_dict[model] = mpg
    except:
        print("Error All")
        all_mpg.append(0)
        already_find_cars_model_dict[model] = 0
        req.counter += 1
        
    print("{0} {1}".format(req.counter, mpg))

print("Total MPGs extracted:", len(all_mpg))

mpg_df = pd.DataFrame(all_mpg, columns=["MPG"])
df = pd.concat([car45, mpg_df], axis=1)
df.to_csv("car45_with_mpg.csv")
print("CSV file created")
browser.close()

    
    
    
    
    
    
    
    
    
    
    