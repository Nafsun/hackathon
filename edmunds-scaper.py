'''
Main Purpose: To scrape all many car features at https://edmunds.com and use it in an AI competition hosted by NNPC and DSN
Creator: Muhammad Aliyu (TEAM C)
Date of Creation: Saturday September 4, 2021

Scraped Features are:
    Make, Model, Engine Type, Transmission, Drive Type, Combined MPG, Total Seating, 
    Fuel Tank Capacity, Fuel Type, Base Engine Size, Horsepower, Torque, Turning Circle, 
    Front Head Room, Front Hip Room, Front Leg Room, Front Shoulder Room, Rear Head Room, 
    Rear Hip Room, Rear Leg Room, Rear Shoulder Room, Cargo Capacity, All Seats In Place, 
    Curb Weight, EPA Interior Volume, Length, Overall Width Without Mirrors, Wheel Base

The number Zero in any of the features refer to a missing value
'''

import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re
import time
import random

print("Started Running Script")

browser = webdriver.Chrome(executable_path="chromedriver.exe")
browser.maximize_window()

class Request:
    def __init__(self):
        self.all_car_info = []
        self.counter = 0
        self.reopen = 100
    def check_if_a_car_is_seen_before(self):
        for i in range(len(self.all_car_info)):
            if(self.all_car_info[i]["Model"] == self.model):
                self.all_car_info.append(self.all_car_info[i])
                return True
        return False
    def search(self, make, model):
        self.make = make
        self.model = model
        if(self.check_if_a_car_is_seen_before() == True):
            self.save_data_to_csv()
            self.counter += 1
            print("Car Seen Before: ", self.counter)
            return
        searching = browser.find_element_by_name("search-input")
        searching.click()
        searching.clear()
        searching.send_keys("{0} {1}".format(self.make, self.model))
        
        WebDriverWait(browser, 60).until(
            EC.presence_of_element_located((By.XPATH, '//span[normalize-space()="Reviews & Specs"]'))
        )
        
        browser.find_element_by_xpath('//span[normalize-space()="Reviews & Specs"]').click()
        
        # Click on See all features & specs
        WebDriverWait(browser, 60).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'See all features & specs'))
        )
        specs_link = browser.find_element_by_link_text('See all features & specs')
        specs_link.click()
        
        # here is where the car spec extraction start
        self.car_specs_container()
        
    def car_specs_container(self):
        overview = browser.find_element_by_id("Overview-section-title-content").text
        overview += '\n'
        overview += browser.find_element_by_id("DriveTrain-section-title-content").text
        overview += '\n'
        overview += browser.find_element_by_id("Fuel-section-title-content").text
        overview += '\n'
        overview += browser.find_element_by_id("Engine-section-title-content").text
        overview += '\n'
        overview += browser.find_element_by_id("Frontseats-section-title-content").text
        overview += '\n'
        overview += browser.find_element_by_id("Rearseats-section-title-content").text
        overview += '\n'
        overview += browser.find_element_by_id("Measurements-section-title-content").text
        
        self.all_car_info.append(self.extract_all_features(overview))
        
        self.counter += 1
        
        print(self.counter)
        
        self.save_data_to_csv()
        
    def save_data_to_csv(self):
        df = pd.DataFrame(self.all_car_info, columns=self.all_car_info[0].keys())
        df.to_csv("car45_with_edmunds.csv")
        print("CSV file saved")
    
    def extract_all_features(self, text):
        arr = {"Make": self.make, "Model": self.model}
        z = [["Engine Type", "Transmission"], ["Transmission", "Drive Type"], ["Drive Type", "Cylinders"], 
             ["Combined MPG", "Total Seating"], ["Total Seating", "Basic Warranty"],
             ["Fuel Tank Capacity", "Fuel Type"], ["Fuel Type", "Range In Miles (Cty/Hwy)"], 
             ["Base Engine Size", "Base Engine Type"], 
             ["Horsepower", "Torque"], ["Torque", "Turning Circle"], 
             ["Turning Circle", "Valve Timing"],
             ["Front Head Room", "Front Hip Room"], ["Front Hip Room", "Front Leg Room"], 
             ["Front Leg Room", "Front Shoulder Room"], ["Front Shoulder Room", "Rear Seat Dimensions"],
             ["Rear Head Room", "Rear Hip Room"], ["Rear Hip Room", "Rear Leg Room"], ["Rear Leg Room", "Rear Shoulder Room"],
             ["Rear Shoulder Room", "Split-Folding Rear Seatback"], ["Cargo Capacity, All Seats In Place", "Curb Weight"],
             ["Curb Weight", "EPA Interior Volume"], ["EPA Interior Volume", "Ground Clearance"], 
             ["Length", "Overall Width Without Mirrors"],
             ["Overall Width Without Mirrors", "Wheel Base"], ["Wheel Base", ""]]
        for name in z:
            a = text.find(name[0])
            b = len(name[0])
            c = None
            d = None
            if len(name[1]) != 0:
                c = text.find(name[1])
                if(a == -1 and c != -1):
                    d = "0"
                elif(c == -1 and a != -1):
                    d = "0"
                elif(a == -1 and c == -1):
                    d = "0"
                else:
                    d = text[a+b+1:c]
            else:
                d = text[a+b+1:]
            if(name[0] != "Engine Type" and name[0] != "Transmission" and name[0] != "Drive Type" and name[0] != "Fuel Type"):
                arr[name[0]] = ''.join([s for s in re.findall(r"[-+]?\d*\.\d+|\d+", d.strip()[:8])])
            else:
                arr[name[0]] = d.strip()
        return arr
        
    def waiter(self, start, end):
        time.sleep(random.randint(start, end))

df = pd.read_csv("car45.csv")
req = Request()
for i in range(len(df)):
    if req.counter >= req.reopen:
        print("Reopening Browser")
        req.reopen = req.reopen + 100
        browser.close()
        browser = webdriver.Chrome(executable_path="C:/Users/Nafsun/Desktop/chromedriver.exe")
        browser.maximize_window()
        time.sleep(10)
    try:
        browser.get("https://www.edmunds.com/")
        WebDriverWait(browser, 60).until(
            EC.presence_of_element_located((By.NAME, "search-input"))
        )
        make = df.iloc[i]["Make"]
        model = df.iloc[i]["Model"]
        req.search(make, model)
    except:
        req.all_car_info.append({'Make': req.make, 'Model': req.model, 'Engine Type': 0, 'Transmission': 0, 'Drive Type': 0, 
                          'Combined MPG': 0, 'Total Seating': 0, 'Fuel Tank Capacity': 0, 
                          'Fuel Type': 0, 'Base Engine Size': 0, 'Horsepower': 0, 'Torque': 0, 
                          'Turning Circle': 0, 'Front Head Room': 0, 
                          'Front Hip Room': 0, 'Front Leg Room': 0, 'Front Shoulder Room': 0, 
                          'Rear Head Room': 0, 'Rear Hip Room': 0, 'Rear Leg Room': 0, 
                          'Rear Shoulder Room': 0, 'Cargo Capacity, All Seats In Place': 0, 
                          'Curb Weight': 0, 'EPA Interior Volume': 0, 'Length': 0, 
                          'Overall Width Without Mirrors': 0, 'Wheel Base': 0})
        req.counter += 1
        print("Error:", req.counter)
req.save_data_to_csv()
