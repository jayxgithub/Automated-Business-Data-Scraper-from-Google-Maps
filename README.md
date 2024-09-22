# Automated Business Data Scraper from Google Maps

## Overview

This script written in Python quickens the need to collect specific businesses and details on GoogleMaps where the analysis is based on Selenium and BeautifulSoup web scraping. It allows users to look for businesses using relevant keywords and captures relevant business listing information to a CSV file.

## Features

- Automated Search: It is able to search Google maps for business listings using given keywords
- Scrolling and Loading Search Results: Navigates through the search results pages not exceeding more than 100 businesses to be scraped.
- Detailed Data Extraction: Gets information which is most often needed including:
  - Name of the business
  - Full address (with zip code + State + City)
  - Contact number
  - Business hours
  - Reviews count
  - Rating
  - Social Networks (Facebook, Instagram)
  - Domain name of the page
- Business Page Handling: Loads every business page on a new tab and updates to add more data collected.
- CSV Export: All the data which is collected is exported to a CSV format for better organization and further use.
- Error Handling and Logging: Option to handle errors enough to have the executable code work smoothly, logs available in the system outlining works done and to be m ade during the scraping.

## How It Works

### Setup and Initialization:
- The script loads a Selenium WebDriver, specifically the ChromeDriver, which is installed easily by using webdriver_manager.
- All the packages necessary for extracting and analyzing data on the web, and carrying out automated tasks have been included and set up.

### Searching and Scrolling:
- Google Maps is opened and the performed search matches the entered keywords provided by the users e.g. "restaurants in New York".
- Scrolls through the list of results in order to obtain more businesses, with a limit set where data is only collected from a hundred businesses.

### Data Extraction:
- For every business listing available in the business directory, the script determines useful details that include the name, address as well as the phone number of the business.
- Navigates to each of the businesses in order to get their respective social media links and business websites.

### Data Export:
- A proper compilation of the detailed information gathered from all the processes is made and saved into a file cc Business_data_5.csv where further analysis will be done.
- Reports the number of the businesses which have been fully processed and also provides their rating.

### Error Handling and Logging:
- The script is designed to proceed smoothly and even produce output despite meeting unexpected challenges such as missing information or failure to load a page.
- Logs make it possible to have a status update on the progress and this facilitates the debugging process.

## Installation and Usage

1. **Cloning the Repository:**
   ```bash
   git clone https://github.com/jayxgithubutomated-Business-Data-Scraper-from-G-Maps
   cd-Business-Data-Scraper-from-Google-Maps
   ```

2. **Dependencies:**
   Ensure that you have Python 3.x installed. Then execute the following command to install the necessary libraries:
   ```bash
   pip install - requirements.txt
   ```

   The key are:
   - Selenium
   - BeautifulSoup (bs4)
   - Pandas
   - Webdriver Manager

3. **Running the Script:**
   Adjust the script with your preferred search and initiate scraper by running:
   ```bash
   python.py
   ```

## Requirements:
- Python 3.x
- Chrome browser
- ChromeDriver (automatically managed bydriver Manager)

## Output:
The extracted data is in Business_data_5.csv, featuring the following fields:
- Business Name
- Address
- Phone Number
- Hours of Operation
- Rating
- Number of Reviews
- Social Media (if available)
- Website URL

## Known Limitations:
- TCHA: Google Maps might a CAPTCHA after multiple.
- Limit: It's advisable to introduce delays between requests to prevent being by Google Maps.

## Contributing:
You are welcome to fork this repository and contribute by submitting pull requests enhancements, bug fixes, or new features.