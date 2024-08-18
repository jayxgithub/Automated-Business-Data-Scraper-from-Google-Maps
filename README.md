### Title: Automated Business Data Scraper from Google Maps

### Description:

This Python script automates the process of extracting business data from Google Maps using Selenium and BeautifulSoup. It performs the following tasks:

1. **Setup and Initialization**:
   - Configures a Selenium WebDriver using ChromeDriver managed by `webdriver_manager`.
   - Defines necessary libraries for web scraping, data handling, and automation.

2. **Scroll and Load Data**:
   - Opens Google Maps and performs searches based on provided keywords.
   - Scrolls through the search results to load more businesses, up to a limit of 100 businesses.

3. **Data Extraction**:
   - Extracts key details from business listings, including:
     - Business name
     - Address, including city, state, and ZIP code
     - Phone number
     - Hours of operation
     - Number of reviews
     - Rating
     - Social media links (Facebook and Instagram)
     - Website URL

4. **Handling Business Details**:
   - Opens each business page in a new browser tab.
   - Extracts additional information from the business page and compiles it into a structured format.

5. **Data Compilation and Export**:
   - Collects all extracted data into a list and saves it into a CSV file named `Business_data_5.csv`.
   - Displays the number of businesses with ratings.

6. **Error Handling and Logging**:
   - Includes error handling to manage potential issues during data extraction.
   - Logs processing status and errors to help with debugging.
