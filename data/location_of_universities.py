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


def dms_to_decimal(dms_str):
    # Use regular expressions to extract degrees, minutes, seconds, and direction
    pattern = r'(\d+\.\d+)°\s*([NSWE])'
    match = re.match(pattern, dms_str)
    
    if match:
        value = float(match.group(1))
        direction = match.group(2)
        
        if direction in ['S', 'W']:
            value = -value
            
        return value
    
    raise ValueError("Invalid input format")

# Function to scrape latitude and longitude from Google using Selenium
def scrape_lat_long(university_name, university_location):
    try:
        chrome_driver_path = "C:/Users/troll/Downloads/chromedriver-win64/chromedriver.exe"  # Replace with the path to your ChromeDriver executable
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)

        driver = webdriver.Chrome(
            service=Service(chrome_driver_path),
            options=chrome_options
        )


        # Prepare the Google search URL
        search_url = f"https://www.google.com/search?q={university_name} latitude and longitude"

        # Send an HTTP request and parse the HTML content
        driver.get(search_url)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find the latitude and longitude information
        location_info = soup.find("div", class_="Z0LcW t2b5Cf")

        if location_info:
            location_text = location_info.text
            lat_long_parts = location_text.split(" ")
            if len(lat_long_parts) >= 4:
                latitude = lat_long_parts[0] + " " + lat_long_parts[1]
                longitude = lat_long_parts[2] + " " + lat_long_parts[3]
                print(dms_to_decimal(latitude), dms_to_decimal(longitude))
                return dms_to_decimal(latitude), dms_to_decimal(longitude)

        return None, None

    except Exception as e:
        print(f"Error scraping latitude and longitude for {university_name}: {e}")
        return None, None

    finally:
        # Close the WebDriver
        driver.quit()

# Read the CSV file
input_file = "World University Rankings 2023.csv"
df = pd.read_csv(input_file)

# Add new columns for Latitude and Longitude
df["Latitude"] = ""
df["Longitude"] = ""

# Iterate over the rows with tqdm progress bar
for index, row in tqdm(df.iterrows(), total=len(df), desc="Scraping Coordinates"):
    university_name = row["Name of University"]
    university_location = row["Location"]
    latitude, longitude = scrape_lat_long(university_name, university_location)
    df.at[index, "Latitude"] = latitude
    df.at[index, "Longitude"] = longitude

# Save the updated dataset to the same CSV file
df.to_csv("World University Rankings 2023_coords.csv", index=False)

print("Data scraped and saved successfully.")
