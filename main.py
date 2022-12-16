import os
import csv
import airtable
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Airtable secrets
AIRTABLE_API_KEY = os.environ['AIRTABLE_API_KEY']
AIRTABLE_BASE_ID = os.environ['AIRTABLE_BASE_ID']

# Initialize an Airtable object
airtable_object = airtable.Airtable(AIRTABLE_BASE_ID, 'Products',
                                    AIRTABLE_API_KEY)
records = airtable_object.get_all(view='Grid view')

# Set up the webdriver
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--window-size=1280,720')
driver = webdriver.Chrome(chrome_options=chrome_options)

# Loop through the websites and take a screenshot of each one
for i in range(0, len(records)):
  record = records[i]
  print(record['fields']['Name'])
  driver.get(record['fields']['Website'])
  driver.save_screenshot(f"screenshots/" + record['fields']['Slug'] + ".png")
  fields = {
    'Image':
    "https://replit.com/@GaborSoter/Screenshotmaker#" + "screenshots/" +
    record['fields']['Slug'] + ".png"
  }
  airtable_object.update(record['id'], fields)

print('Done')

# Close the webdriver
driver.close()