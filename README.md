# hackathon
TEAM C

<h1>Artificial Intelligence Hackathon hosted by Data Science Nigeria and NNPC Chevron</h1>

For running the 2 script listed below, you need a chromedriver for the current version of
chrome in your PC.

1. car45-mpg-extractor.py
2. edmunds-scaper.py


Open this notebook for more information: car45_model_and_analysis.ipynb

Main Purpose: This notebook contains a model that is built to predict the CO2 emission of a vechile given some it features as input. It also contains an analysis of which features are the most important in predicting CO2 emission using Ordinary Least Square, Feature Permutation Analysis, F_Regression, Random Forest Feature Importance, CatBoost Model. The data used to train this model was scraped from **https://www.car45.com, https://edmunds.com and https://fueleconomy.gov**. The scraping algorithms can be found in the current folder where this notebook reside.

Creator: **Muhammad Aliyu (TEAM C)**

Date of Creation: **Saturday September 4, 2021**

The Features used in building the model are: ***Make, Model, Price, Engine Type, Transmission, Drive Type, Combined MPG, Total Seating, Fuel Tank Capacity, Fuel Type, Base Engine Size, Horsepower, Torque, Turning Circle, Front Head Room, Front Hip Room, Front Leg Room, Front Shoulder Room, Rear Head Room, Rear Hip Room, Rear Leg Room, Rear Shoulder Room, Cargo Capacity All Seats In Place, Curb Weight, EPA Interior Volume, Length, Overall Width Without Mirrors, Wheel Base***

The number Zero in any of the features refer to a missing value

Run the following scripts in the order they appear to scrape the data before running this notebook

1. car45.py
2. car45-mpg-extractor.py
3. edmunds-scaper.py
