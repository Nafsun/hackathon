'''
Main Purpose: To scrape all the car data at https://car45.com and use it in an AI competition hosted by NNPC and DSN
Creator: Muhammad Aliyu (TEAM C)
Date of Creation: Sunday August 29, 2021

At the time this webscraping algorithm is made, it scraped 5254 car data from https://car45.com

Scaped Car Features: 
    Make    Model  Year  Mileage (KM)  Location    Transmission  Selling Condition  Colour  Price    Used Location
    Toyota  Camry  2012  44106         C45, Lagos  Automatic     Registered         RED     3034000  Nigerian used

The number Zero in any feature refer to a missing value
'''
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

print("Started Running Script")

# returns all keys or values of a (nested) iterable.
def iterate_all(iterable, returned="value"):
    if isinstance(iterable, dict):
        for key, value in iterable.items():
            if returned == "key":
                yield key
            elif returned == "value":
                if not (isinstance(value, dict) or isinstance(value, list)):
                    yield value
            else:
                raise ValueError("'returned' keyword only accepts 'key' or 'value'.")
            for ret in iterate_all(value, returned=returned):
                yield ret
    elif isinstance(iterable, list):
        for el in iterable:
            for ret in iterate_all(el, returned=returned):
                yield ret

class Request:
    def __init__(self, url):
        self.url = url
        self.counter = 1
    def get_url(self):
        r = requests.get("{0}{1}".format(self.url, self.counter))
        print(self.counter)
        self.counter += 1
        return r
    def get_single_url_data(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        il = soup.find("ul", "information_list")
        price = soup.find("h4", "price_title d-inline-block")
        used_location = soup.find("button", "btn btn-secondary")
        return il, price, used_location

req = Request("https://buy.cars45.com/cars?page=")
# all url for each car in the cars45 website
all_hrefs = []
# exit the running while loop once we reach the end of the page
exiting = False
while True:
    # Get each page url
    try:
        r = req.get_url()
        if(r.status_code == 200):
            # parse html
            soup = BeautifulSoup(r.text, 'html.parser')
            # check if no information is found in this page
            for i in soup.find_all("p"):
                if(i.get_text() == "No record found"):
                    exiting = True
                    break
            if(exiting):
                break
            # find all classes with the name: product_box
            pb_array = soup.find_all("div", "product_box")
            # Get all the <a> in each product_box class tags and add it to our car list
            for i in pb_array:
                all_hrefs.append(i.find("a").get('href'))
    except:
        print("Error All")

print("Length of Individual Cars Array: {0}".format(len(all_hrefs)))

# all data for csv
all_data_csv = []
# counting the number of cars
counting_cars = 0
# Starting single URL scraping for each car link
for i in all_hrefs:
    try:
        gs, price, used_location = req.get_single_url_data(i)
        # car price
        p = str(price.get_text()).split()[1]
        price = ''.join([s for s in p.split(",") if s.isdigit()])
        #used location i.e. Nigeria or Foriegn
        used_location = str(used_location.get_text()).strip()
        # car details
        info_array = str(gs.get_text()).split(" ")
        # Add only the data that is relevant to car information to this array
        car_data = []
        for i in info_array:
            if(i != ""):
                car_data.append(i)
        # Clean a car real data and store it in an array
        real_data = []
        len_car_data = len(car_data)
        # strip all \n from the array
        new_car_data = []
        for i in range(len_car_data):
            new_car_data.append(car_data[i].strip('\n'))
        car_data = new_car_data
        for i in range(len_car_data):
            if(i != len_car_data-1):
                if(car_data[i] == "Make"):
                    real_data.append({"Make": car_data[i+1]})
                    if("Model" not in car_data):
                        real_data.append({"Model": 0})
                elif(car_data[i] == "Model"):
                    real_data.append({"Model": car_data[i+1]})
                    if("Year" not in car_data):
                        real_data.append({"Year": 0})
                elif(car_data[i] == "Year"):
                    real_data.append({"Year": car_data[i+1]})
                    if("Mileage" not in car_data):
                        real_data.append({"Mileage": 0})
                elif(car_data[i] == "Mileage"):
                    real_data.append({"Mileage": car_data[i+1]})
                    if("Location" not in car_data):
                        real_data.append({"Location": 0})
                elif(car_data[i] == "Location"):
                    real_data.append({"Location": "{0}, {1}".format(car_data[i+1], car_data[i+3])})
                    if("Transmission" not in car_data):
                        real_data.append({"Transmission": 0})
                elif(car_data[i] == "Transmission"):
                    real_data.append({"Transmission": car_data[i+1]})
                    if("Selling" not in car_data):
                        real_data.append({"Selling Condition": 0})
                elif(car_data[i] == "Selling"):
                    real_data.append({"Selling Condition": car_data[i+2]})
                    if("Colour" not in car_data):
                        real_data.append({"Colour": 0})
                elif(car_data[i] == "Colour"):
                    real_data.append({"Colour": car_data[i+1]})
        single_data = list(iterate_all(real_data))
        if(len(single_data) < 8):
            single_data = single_data + list(np.zeros(8 - len(single_data))) + [price, used_location]
        else:
            single_data = single_data + [price, used_location]
        print(counting_cars, single_data)
        counting_cars += 1
        all_data_csv.append(single_data)
    except:
        print("Error Single")

# Save data to a csv file
column = ["Make", "Model", "Year", "Mileage (KM)", "Location", "Transmission", "Selling Condition", "Colour", "Price", "Used Location"]
df = pd.DataFrame(all_data_csv, columns=column)
print(df)
df.to_csv("car45.csv")