# import standard libraries
import json
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from tqdm import tqdm
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import numpy as np
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
import warnings
# import third party libraries
import objectpath
import pandas as pd

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen 
from selenium import webdriver


webdriver_location = "C:/Users/troll/Downloads/chromedriver-win64/chromedriver.exe"
# initiate webdriver

chrome_driver_path = "C:/Users/troll/Downloads/chromedriver-win64/chromedriver.exe"  # Replace with the path to your ChromeDriver executable
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)

driver = webdriver.Chrome(
    service=Service(chrome_driver_path),
    options=chrome_options
)

url_stats = "https://www.timeshighereducation.com/world-university-rankings/2015/world-ranking#!/length/100/sort_by/rank/sort_order/asc/cols/stats"
url_scores = 'https://www.timeshighereducation.com/world-university-rankings/2015/world-ranking#!/length/100/sort_by/rank/sort_order/asc/cols/scores'

# create two webdriver objects, one for each of the two adresses 
stats_browser = webdriver.Chrome()
scores_browser = webdriver.Chrome()

# use the webdriver to request the ranking webpage
stats_browser.get(url_stats)

# collect the webpage HTML after its loading
stats_page_html = stats_browser.page_source

# parse the HTML using BeautifulSoup
stats_page_soup = soup(stats_page_html, 'html.parser')

# collect HTML objects 
rank_obj = stats_page_soup.findAll("td", {"class":"rank sorting_1 sorting_2"})
names_obj = stats_page_soup.findAll("td", {"class":"name namesearch"})
stats_number_students_obj = stats_page_soup.findAll("td", {"class":"stats stats_number_students"})
stats_student_staff_ratio_obj = stats_page_soup.findAll("td", {"class":"stats stats_student_staff_ratio"})
stats_pc_intl_students_obj = stats_page_soup.findAll("td", {"class":"stats stats_pc_intl_students"})
stats_female_male_ratio_obj = stats_page_soup.findAll("td", {"class":"stats stats_female_male_ratio"})

# close the browser
stats_browser.close() 

# use the webdriver to request the scores webpage
scores_browser.get(url_scores)

# collect the webpage HTML after its loading
scores_page_html = scores_browser.page_source
scores_page_soup = soup(scores_page_html, 'html.parser')

# parse the HTML using BeautifulSoup
overall_score_obj = scores_page_soup.findAll("td", {"class":"scores overall-score"})
teaching_score_obj = scores_page_soup.findAll("td", {"class":"scores teaching-score"})
research_score_obj = scores_page_soup.findAll("td", {"class":"scores research-score"})
citations_score_obj = scores_page_soup.findAll("td", {"class":"scores citations-score"})
industry_income_score_obj = scores_page_soup.findAll("td", {"class":"scores industry_income-score"})
international_outlook_score_obj = scores_page_soup.findAll("td", {"class":"scores international_outlook-score"})

# close the browser
scores_browser.close() 

rank, names, number_students, student_staff_ratio, intl_students, female_male_ratio, web_address =  [], [], [], [], [], [], []
overall_score, teaching_score, research_score, citations_score, industry_income_score, international_outlook_score = [], [], [], [], [], []
for i in range(len(names_obj)):
    web_address.append('https://www.timeshighereducation.com' + names_obj[i].a.get('href'))
    rank.append(rank_obj[i].text)
    
    names.append(names_obj[i].a.text)
    number_students.append(stats_number_students_obj[i].text)
    student_staff_ratio.append(stats_student_staff_ratio_obj[i].text)
    intl_students.append(stats_pc_intl_students_obj[i].text)
    female_male_ratio.append(stats_female_male_ratio_obj[i].text[:2])
    
    overall_score.append(overall_score_obj[i].text)
    teaching_score.append(teaching_score_obj[i].text)
    research_score.append(research_score_obj[i].text)
    citations_score.append(citations_score_obj[i].text)
    industry_income_score.append(industry_income_score_obj[i].text)
    international_outlook_score.append(international_outlook_score_obj[i].text)

full_address_list, streetAddress_list, addressLocality_list, addressRegion_list, postalCode_list, addressCountry_list  = [], [], [], [], [], []
country_count = {}  # Initialize an empty dictionary to store country counts

for web in web_address:
    page = urlopen(web)
    page_html = soup(page, 'html.parser')
    location = page_html.findAll('script', {'type':"application/ld+json"})
    jt = json.loads(location[0].text)
    jsonnn_tree = objectpath.Tree(jt)
    streetAddress_list.append(list(jsonnn_tree.execute('$..streetAddress'))[0])
    addressLocality_list.append(list(jsonnn_tree.execute('$..addressLocality'))[0])
    addressRegion_list.append(list(jsonnn_tree.execute('$..addressRegion'))[0])
    postalCode_list.append(list(jsonnn_tree.execute('$..postalCode'))[0])
    full_address = page_html.findAll('div', {'class':"institution-info__contact-detail institution-info__contact-detail--address"})[0].text.strip()
    address_parts = full_address.split(',')
    country = address_parts[-1].strip()
    full_address_list.append(full_address)
    addressCountry_list.append(country)

        # Count the occurrences of each country
    if country in country_count:
        country_count[country] += 1
    else:
        country_count[country] = 1


    print ('{} out of {}'.format(len(full_address_list), len (web_address)), country)

df = pd.DataFrame({
    'rank' : rank,
    'name' : names,
    'number_students' : number_students,
    'student_staff_ratio' : student_staff_ratio,
    'intl_students' : intl_students,
    'female_male_ratio' : female_male_ratio,
    'overall_score' : overall_score,
    'teaching_score' : teaching_score,
    'research_score' : research_score,
    'citations_score' : citations_score,
    'industry_income_score' : industry_income_score,
    'international_outlook_score' : international_outlook_score,
    'address' : full_address_list, 
    'street_address' : streetAddress_list,
    'locality_address' : addressLocality_list,
    'region_address' : addressRegion_list,
    'postcode_address' : postalCode_list,
    'country_address' : addressCountry_list
})


df['intl_students'] = df['intl_students'].str.replace(pat='%', repl='')
df['rank'] = df['rank'].str.replace(pat='\–\d*|\+', repl='', regex=True)
df['overall_score'] = df['overall_score'].str.replace(pat='.*\–', repl='', regex=True)
df['number_students'] = df['number_students'].str.replace(pat=',', repl='', regex=True)
df = df.replace('n/a*', np.nan, regex=True)

df.to_csv('uni_2022.csv', encoding='utf-8', index=False)
# Print the country tally
print("Country Tally:")
for country, count in country_count.items():
    print(f"{country}: {count} occurrences")

import os
import csv

# ... (previous code here)

# Collect the country counts and their respective years
year = input("Enter the year: ")
country_counts = {year: country_count}

# File path for the CSV
csv_filename = "amount_in_1002.csv"

# Function to update the CSV data with the new year and counts
def update_csv_data(year, country_counts, csv_filename):
    if not os.path.isfile(csv_filename):
        # If the CSV file doesn't exist, create a new one.
        with open(csv_filename, mode='w', newline='') as file:
            fieldnames = ['Year'] + list(country_counts[year].keys())
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

    # Read the existing data from the CSV file
    existing_data = {}
    with open(csv_filename, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            existing_data[row['Year']] = row

    # Update the existing data with the new counts
    if year not in existing_data:
        existing_data[year] = {'Year': year}
    existing_data[year].update(country_counts[year])

    # Write the updated data back to the CSV file
    with open(csv_filename, mode='w', newline='') as file:
        fieldnames = ['Year'] + list(existing_data[year].keys())
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in existing_data.values():
            writer.writerow(row)

update_csv_data(year, country_counts, csv_filename)

# ... (remaining code, as before)
