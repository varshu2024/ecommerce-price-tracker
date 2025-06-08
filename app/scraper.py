import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import urlparse

def scrape_product_price(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Amazon
        if 'amazon.' in url:
            price_whole = soup.find('span', class_='a-price-whole')
            price_fraction = soup.find('span', class_='a-price-fraction')
            if price_whole and price_fraction:
                return float(price_whole.text + price_fraction.text)
        
        # eBay
        elif 'ebay.' in url:
            price = soup.find('span', itemprop='price')
            if price:
                return float(price['content'])
        
        # Walmart
        elif 'walmart.' in url:
            price = soup.find('span', itemprop='price')
            if price:
                return float(price.text[1:])
        
        # For JavaScript-rendered sites
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        
        # Generic price detection
        price_elements = driver.find_elements_by_xpath("//*[contains(text(), '$')]")
        for element in price_elements:
            text = element.text
            if '$' in text:
                try:
                    price = float(text.split('$')[1].split()[0].replace(',', ''))
                    return price
                except:
                    continue
        
        return None
        
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None
    finally:
        if 'driver' in locals():
            driver.quit()