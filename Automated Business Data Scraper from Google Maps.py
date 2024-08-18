# Import necessary libraries for web scraping, data handling, and automation
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
import uuid
from datetime import datetime
import re


# Function to scroll down the page to load more results
def scroll_down(driver, scroll_pause_time=3):
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)  # Scroll down
    time.sleep(scroll_pause_time)  # Wait for the page to load


# List of keywords for which to perform the search (to be filled)
keywords = ["Games store in USA"]  # put here keywords for scraping

# Setup Chrome driver using WebDriverManager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# List to store the extracted business data
business_data = []
# Set to track URLs already processed to avoid duplicates
processed_urls = set()


# Function to extract city, state, country, and zipcode from the address
def extract_location_info(address):
    if address:
        country = "USA"
        parts = address.split(',')
        if len(parts) > 2:
            city = parts[-3].strip()
            state = parts[-2].strip().split()[0]
            zipcode_match = re.search(r'\b\d{5}\b', parts[-2])
            if zipcode_match:
                zipcode = zipcode_match.group(0)
    return city, state, country, zipcode


# Loop through each keyword to perform the search
for keyword in keywords:
    print(f"Searching for: {keyword}")

    # Create the Google Maps search URL using the keyword
    search_url = "https://www.google.com/maps/search/" + keyword.replace(" ", "+")
    driver.get(search_url)

    print("Loading page...")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))  # Wait for page to load
    print("Page loaded")

    num_scrolls = 0  # Counter for the number of scrolls performed
    max_scrolls = 10  # Maximum number of scrolls allowed
    while len(driver.find_elements(By.CLASS_NAME, 'hfpxzc')) < 100 and num_scrolls < max_scrolls:
        scroll_down(driver)  # Scroll down to load more results
        num_scrolls += 1  # Increment scroll count
    print(f"Scrolled {num_scrolls} times, found {len(driver.find_elements(By.CLASS_NAME, 'hfpxzc'))} elements")

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find all business elements on the page
    business_elements = soup.find_all('a', class_='hfpxzc')
    print(f"Found {len(business_elements)} business elements")

    # Loop through each business element to extract data
    for index, business in enumerate(business_elements):
        if len(business_data) >= 100:  # Stop after 100 businesses
            break
        try:
            href = business.get('href')  # Extract the business URL
            if href in processed_urls:  # Skip if already processed
                continue
            processed_urls.add(href)

            print(f"Processing business {index + 1}/{len(business_elements)}")

            name = business.get('aria-label')  # Extract the business name
            print(f"Name: {name}, URL: {href}")

            # Open the business page in a new tab
            driver.execute_script("window.open(arguments[0]);", href)
            driver.switch_to.window(driver.window_handles[1])
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

            # Parse the business page with BeautifulSoup
            business_soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Extract the address, city, state, and zipcode
            address_element = business_soup.find('button', attrs={'data-tooltip': 'Copy address'})
            address = address_element.text if address_element else 'N/A'

            city, state, country, zipcode = extract_location_info(address)

            # Extract the phone number
            phone_number = business_soup.find('button', attrs={'data-tooltip': 'Copy phone number'})
            phone_number = phone_number.text if phone_number else 'N/A'

            # Extract hours of operation
            hours_of_operation = []
            hours_elements = business_soup.find_all('div', class_='MkV9')  # Use class from your snippet
            for hour in hours_elements:
                hours_of_operation.append(hour.text.strip())

            # Extract the number of reviews
            reviews_element = business_soup.find('span', class_='UY7F9')  # Class name from your snippet
            reviews = reviews_element.text if reviews_element else 'No reviews'

            # Extract social media links (Facebook and Instagram)
            social_media_links = [link['href'] for link in business_soup.find_all('a', href=True) if
                                  'facebook.com' in link['href'] or 'instagram.com' in link['href']]

            # Extract the rating
            rating_element = business_soup.find('div', class_='F7nice')  # Updated class name
            rating = rating_element.get_text() if rating_element else "No rating"

            print(f"Extracted rating: {rating}")

            # Extract the website link
            website_link = business_soup.find('a', attrs={'data-tooltip': 'Open website'})
            website = website_link['href'] if website_link else 'N/A'

            # Generate a unique ID for the business entry
            id_counter = str(uuid.uuid4())
            # Get the current date
            date = datetime.now().strftime("%Y-%m-%d")

            # Set open and close schedules (first and last entries in hours_of_operation)
            open_schedule = hours_of_operation[0] if hours_of_operation else "N/A"
            close_schedule = hours_of_operation[-1] if hours_of_operation else "N/A"

            location = address
            no_of_reviews = reviews

            # Extract the first Facebook and Instagram links found
            facebook_link = next((link for link in social_media_links if 'facebook.com' in link), "N/A")
            instagram_link = next((link for link in social_media_links if 'instagram.com' in link), "N/A")

            # Append the business data to the list
            business_data.append({
                'ID': id_counter,
                'Date': date,
                'Name': name,
                'Address': address,
                'City': city,
                'State': state,
                'Country': country,
                'Zip': zipcode,
                'Open Schedule': open_schedule,
                'Close Schedule': close_schedule,
                'Website': website,
                'Phone': phone_number,
                'Location': location,
                'Rating': rating,
                'No of Reviews': no_of_reviews,
                'Place URL': website,  # Changed from href to website
                'Service Summary': keyword,
                'Facebook': facebook_link,
                'Instagram': instagram_link
            })

            print(f"Added business {name}")

            # Close the business tab and return to the search results tab
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        except Exception as e:
            print(f"Error processing business {index + 1}: {e}")
            if len(driver.window_handles) > 1:
                driver.close()
            driver.switch_to.window(driver.window_handles[0])
            continue

driver.quit()  # Close the browser once all processing is done

# Save the business data to a CSV file
df = pd.DataFrame(business_data)
df.to_csv('Business_data_5.csv', index=False)
print("Data saved to Business_data_5.csv")

# Count and display the number of businesses that have ratings
ratings_found = sum(1 for business in business_data if business['Rating'] != "No rating")
print(f"Total ratings found: {ratings_found} out of {len(business_data)} businesses")