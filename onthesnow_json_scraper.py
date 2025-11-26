#!/usr/bin/env python3
"""
OnTheSnow California Scraper - JSON Parser
Extracts data from the __NEXT_DATA__ JSON embedded in the page
This gets ALL resort data including trails/lifts that the table scraper misses
"""

import os
import pandas as pd
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import re
import json

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("onthesnow_json.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class OnTheSnowJSONScraper:
    """Scrapes snow conditions from OnTheSnow.com using embedded JSON data"""
    
    def __init__(self, headless=True):
        self.url = "https://www.onthesnow.com/california/skireport.html"
        self.headless = headless
        self.driver = None
    
    def setup_driver(self):
        """Configure Chrome driver for Selenium"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless")
        
        # Essential options for CI/cloud environments
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
        
        # Initialize driver
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            logger.info("Chrome driver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Chrome driver: {e}")
            raise
    
    def fetch_page(self):
        """Load the page and wait for data to render"""
        try:
            logger.info(f"Loading {self.url}")
            self.driver.get(self.url)
            
            # Wait for the page to load
            logger.info("Waiting for page to load...")
            wait = WebDriverWait(self.driver, 30)
            
            # Wait for body
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            logger.info("Page body loaded")
            
            # Give extra time for dynamic content
            time.sleep(5)
            
            # Get the rendered HTML
            html = self.driver.page_source
            logger.info(f"Retrieved {len(html)} bytes of HTML")
            
            return html
            
        except Exception as e:
            logger.error(f"Error fetching page: {e}")
            raise
    
    def parse_json_data(self, html):
        """Extract resort data from __NEXT_DATA__ JSON"""
        try:
            # Find the __NEXT_DATA__ script tag
            match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html, re.DOTALL)
            
            if not match:
                logger.error("Could not find __NEXT_DATA__ in HTML")
                return []
            
            # Parse JSON
            data = json.loads(match.group(1))
            resorts_data = data['props']['pageProps']['resorts']
            
            logger.info(f"Found {len(resorts_data)} status categories in JSON")
            
            # resorts_data is a dict with keys '1', '2', '3', etc. representing different status tables
            # '1' = Open resorts
            # '2' = Closed resorts (opening soon)
            # etc.
            
            all_resorts = []
            
            for category_key, category_data in resorts_data.items():
                resorts_list = category_data.get('data', [])
                logger.info(f"Category '{category_key}': {len(resorts_list)} resorts")
                
                for resort_json in resorts_list:
                    resort = self._parse_resort_json(resort_json)
                    if resort:
                        all_resorts.append(resort)
            
            logger.info(f"Extracted {len(all_resorts)} total resorts from JSON")
            return all_resorts
            
        except Exception as e:
            logger.error(f"Error parsing JSON data: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _parse_resort_json(self, resort_json):
        """Parse individual resort from JSON structure"""
        try:
            name = resort_json.get('title', '')
            if not name:
                return None
            
            # Status: openFlag values: 1=Open, 2=Closed, 5=Weekends Only
            open_flag = resort_json.get('status', {}).get('openFlag', 2)
            if open_flag == 1:
                status = 'Open'
            elif open_flag == 5:
                status = 'Open'  # Weekends only - still show as open
            else:
                status = 'Closed'
            
            # Snow data
            snow = resort_json.get('snow', {})
            base_depth = snow.get('base') or snow.get('middle') or 0
            if base_depth:
                base_depth = round(base_depth / 2.54)  # Convert cm to inches
            
            new_snow_24h = snow.get('last24', 0)
            if new_snow_24h:
                new_snow_24h = round(new_snow_24h / 2.54)  # Convert cm to inches
            
            new_snow_48h = snow.get('last48', 0)
            if new_snow_48h:
                new_snow_48h = round(new_snow_48h / 2.54)  # Convert cm to inches
            
            # Lifts data
            lifts = resort_json.get('lifts', {})
            open_lifts = lifts.get('open', 0)
            total_lifts = lifts.get('total', 0)
            lifts_open = f"{open_lifts}/{total_lifts}"
            
            # Trails/Runs data
            runs = resort_json.get('runs', {})
            open_trails = runs.get('open', 0)
            total_trails = runs.get('total', 0)
            trails_open = f"{open_trails}/{total_trails}"
            
            resort = {
                'name': name,
                'status': status,
                'new_snow_24h': int(new_snow_24h),
                'new_snow_48h': int(new_snow_48h),
                'base_depth': int(base_depth),
                'trails_open': trails_open,
                'lifts_open': lifts_open,
                'open_lifts': int(open_lifts),
                'total_lifts': int(total_lifts),
                'open_trails': int(open_trails),
                'total_trails': int(total_trails),
            }
            
            return resort
            
        except Exception as e:
            logger.warning(f"Error parsing resort JSON: {e}")
            return None
    
    def scrape(self):
        """Main scraping method"""
        try:
            self.setup_driver()
            html = self.fetch_page()
            
            # Save HTML for debugging
            with open('onthesnow_california_page_rendered.html', 'w', encoding='utf-8') as f:
                f.write(html)
            logger.info("Saved rendered HTML to onthesnow_california_page_rendered.html")
            
            resorts = self.parse_json_data(html)
            
            if not resorts:
                logger.warning("No resort data found! Check HTML file for structure")
                return pd.DataFrame()
            
            # Convert to DataFrame
            df = pd.DataFrame(resorts)
            
            # Add metadata
            df['data_fetched_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            df['source'] = 'OnTheSnow'
            
            logger.info(f"Successfully processed {len(df)} resorts")
            
            return df
            
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("Chrome driver closed")
            except Exception as e:
                logger.warning(f"Error closing driver: {e}")


def main():
    """Test the JSON scraper"""
    logger.info("="*70)
    logger.info("ONTHESNOW JSON SCRAPER - TEST RUN")
    logger.info("="*70)
    
    scraper = OnTheSnowJSONScraper(headless=True)
    
    try:
        df = scraper.scrape()
        
        if df.empty:
            logger.error("No data scraped")
            return
        
        # Display results
        logger.info(f"\n{'='*70}")
        logger.info("SCRAPING RESULTS")
        logger.info(f"{'='*70}")
        logger.info(f"Total resorts: {len(df)}")
        
        # Show sample data
        print("\n" + df[['name', 'status', 'lifts_open', 'trails_open', 'base_depth']].to_string())
        
        # Check for open resorts
        open_resorts = df[df['status'] == 'Open']
        logger.info(f"\n🎿 {len(open_resorts)} resorts currently OPEN:")
        for _, resort in open_resorts.iterrows():
            logger.info(f"  - {resort['name']}: {resort['lifts_open']} lifts, {resort['trails_open']} trails")
        
    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

