import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

SURVEY_URL = 'https://docs.google.com/forms/d/e/1FAIpQLSd0M2jeyEnXTCmQKScek5RtRAoh7R2762jMcnjIdsU7mZdHPw/viewform?usp=sf_link'

APT_URL = 'https://www.apartments.com/san-francisco-ca/min-1-bedrooms-under-3000/'

HEADER = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

#Scraping apartments website
response = requests.get(url=APT_URL, headers=HEADER)
house_data = response.text

soup = BeautifulSoup(house_data, 'lxml')

#We want to extract links, price, address
house_addresses = soup.find_all(class_='property-address js-url')
house_addresses_unique = []
for i in house_addresses:
    house_addresses_unique.append(i.contents[0].text)
print(house_addresses_unique)

house_prices = soup.find_all(class_='property-pricing')
house_prices_min = []
for i in house_prices:
    house_prices_min.append(i.contents[0].text[0:6])
print(house_prices_min)

#house_links = soup.find_all(name='article', class_='placard placard-option-diamond has-header js-diamond')
house_links = soup.find_all(class_='property-link')
house_links = [house.get('href') for house in house_links]
house_links_unique = []
[house_links_unique.append(x) for x in house_links if x not in house_links_unique]
print(house_links_unique)

vals = zip(house_addresses_unique, house_prices_min, house_links_unique)
ids = range(1, len(house_addresses_unique)+1)
house_info = dict(zip(ids, vals))
print(house_info)

#We got all the addresses, prices, and links in a dictionary!

#Creating our selenium driver
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
driver.get(SURVEY_URL)
time.sleep(5)

for i in range(1, len(house_info) + 1):
    time.sleep(2)
    address_input = driver.find_element(By.XPATH,
                                        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/div')
    ActionChains(driver).move_to_element(address_input).click(address_input).perform()
    ActionChains(driver).send_keys_to_element(address_input, house_info[i][0]).perform()
    time.sleep(2)
    price_input = driver.find_element(By.XPATH,
                                      '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/div')
    ActionChains(driver).move_to_element(price_input).click(price_input).perform()
    ActionChains(driver).send_keys_to_element(price_input, house_info[i][1]).perform()
    time.sleep(2)
    link_input = driver.find_element(By.XPATH,
                                     '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/div')
    ActionChains(driver).move_to_element(link_input).click(link_input).perform()
    ActionChains(driver).send_keys_to_element(link_input, house_info[i][2]).perform()
    time.sleep(2)
    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    ActionChains(driver).move_to_element(submit_button).click(submit_button).perform()
    time.sleep(3)
    another_one = driver.find_element(By.LINK_TEXT, 'Submit another response')
    ActionChains(driver).move_to_element(another_one).click(another_one).perform()
    time.sleep(3)

