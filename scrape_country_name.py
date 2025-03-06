from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd

print("script started >>>")

# laoding the excel file
df = pd.read_excel("D:/workbench/faolex_playwright/File.xlsx")

def scrape_country_name(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()  # Or p.firefox.launch() or p.webkit.launch()
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")  # Wait until the network is mostly idle

        # Get the rendered HTML
        html = page.content()

        soup = BeautifulSoup(html, "html.parser")

        country_element = soup.select_one("div.item-text.country div.item-value a") # Example using CSS selector
        date_element = soup.select_one("div.item-text.dateOfText div.item-value")
        

        if country_element:
            country_name = country_element.text.strip() # .strip() removes extra whitespace.
            date_name = date_element.text.strip() if date_element else "Date not found"
            print(f"Country Name: {country_name}, Date: {date_name}")
            return country_name, date_name
        else:
            print("Country name element not found.")
            return None

        browser.close()

# applying the function to each row
df["Country, Date"] = df["Links"].apply(scrape_country_name)

# save the updated data to a new excel file
df.to_excel("D:/workbench/faolex_playwright/file_updated.xlsx", index = False)