import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from tqdm import tqdm
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
import warnings

# Filter out the specific warning by category and message
warnings.filterwarnings("ignore", category=UserWarning, message="Error with Permissions-Policy header")


# Function to scrape continent from Google using Selenium
def scrape_continent(university_name, university_country):
    try:
        chrome_driver_path = "C:/Users/troll/Downloads/chromedriver-win64/chromedriver.exe"  # Replace with the path to your ChromeDriver executable
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)

        driver = webdriver.Chrome(
            service=Service(chrome_driver_path),
            options=chrome_options
        )

        # Prepare the Google search URL
        search_url = f"https://www.google.com/search?q=what continent is {university_country} in?"

        # Send an HTTP request and parse the HTML content
        driver.get(search_url)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find the continent information
        continent_info = soup.find("div", class_="Z0LcW")

        if continent_info:
            continent = continent_info.text
            print(university_country + ": " + continent)
            return continent

        return "Unknown"

    except Exception as e:
        print(f"Error scraping continent for {university_name}: {e}")
        return "Unknown"

    finally:
        # Close the WebDriver
        driver.quit()


# Read the CSV file
input_file = "data/top_100.csv"
df = pd.read_csv(input_file)

# Add a new column for Continent
df["Continent"] = ""

# Iterate over the rows with tqdm progress bar
for index, row in tqdm(df.iterrows(), total=len(df), desc="Scraping Continent"):
    university_name = row["Name of University"]
    university_country = row["Location"]
    continent = scrape_continent(university_name, university_country)
    df.at[index, "Continent"] = continent

# Save the updated dataset to the same CSV file
df.to_csv("data/top_100.csv_with_continent.csv", index=False)

print("Data scraped and saved successfully.")

