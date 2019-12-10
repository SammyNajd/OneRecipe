# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 20:06:52 2019

@author: Najd
"""

from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import config
import mail
import time


class FreshScraper():
        
    def __init__(self, items):
        self.fresh_url = config.FRESH_URL
        self.items = items
        
      # Attempts to run headless, getting errors
      # chrome_options = Options()
      #  chrome_options.add_argument('--headless')
      #  chrome_options.add_argument('--disable-gpu')
      #  chrome_options.add_argument('--no-sandbox')
      #  chrome_options.add_argument('--allow-insecure-localhost')
      #  chrome_options.add_argument('--ignore-certificate-errors') 
       # self.driver = webdriver.Chrome(config.chromedriver, options=chrome_options)
       
        self.driver = webdriver.Chrome(config.chromedriver)
        self.driver.get(self.fresh_url)
        
    
    def search_items(self):
        urls = []
        prices = []
        titles = []
        
        for item in self.items:
            print(f"Searching for {item}")
                         
            search_bar = self.driver.find_element_by_id('twotabsearchtextbox')
            search_bar.send_keys(item)
            
            time.sleep(2)
                
            search_button = self.driver.find_element_by_xpath('//*[@id="nav-search"]/form/div[2]/div/input')
            search_button.click()
            
            time.sleep(2)
            
         #   WebDriverWait(self.driver, 5).until(visibility_of_element_located((By.XPATH,'//*[@id="a-autoid-0-announce"]' )))
            sort_by = self.driver.find_element_by_xpath('//*[@id="a-autoid-0-announce"]')
            sort_by.click()
            
            time.sleep(2)
            
            sort_by_low_high = self.driver.find_element_by_xpath('//*[@id="s-result-sort-select_1"]')
            sort_by_low_high.click()
            
            time.sleep(2)
            
            search_results = self.driver.find_element_by_xpath('//*[@id="search"]/div[1]/div[2]/div/span[4]/div[1]/div[1]/div/span/div/div/div[2]/div[3]/div/div/h2/a')
            result_url = search_results.get_attribute('href')
            self.driver.get(result_url)
            
            title = self.driver.find_element_by_id('productTitle').text
            price = self.driver.find_element_by_id('priceblock_ourprice').text
            
            urls.append(result_url)
            prices.append(price)
            titles.append(title)
            
            self.driver.get(self.fresh_url)
            
        
        self.driver.close() 
        return urls, prices, titles


def constructMail(urls, prices, titles):
    
    links = []
    
    for url, price, title in zip(urls, prices, titles):
        title_and_price = title + ': ' + price
        link = '<a href="{}">{}</a>'.format(url, title_and_price)
        links.append(link)
    
    return links

    
def main():
    items = ["Lime"]
    scrape = FreshScraper(items)
    urls, prices, titles = scrape.search_items()
    
    ingredient_links = constructMail(urls, prices, titles)
    mail.send_mail(ingredient_links)
    print('mail should be sent')
            
            
if __name__ == '__main__':
    main()