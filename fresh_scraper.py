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
import spoonacular_get as spn

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
            self.driver.get(self.fresh_url)
               
            search_bar = self.driver.find_element_by_id('twotabsearchtextbox')
            search_bar.send_keys(item)
            
            time.sleep(2)
                
            search_button = self.driver.find_element_by_xpath('//*[@id="nav-search"]/form/div[2]/div/input')
            search_button.click()
            
            time.sleep(2)
            
            search_results = self.driver.find_element_by_css_selector("div[data-index='0']")
            result_url = search_results.find_element_by_css_selector('a.a-link-normal.a-text-normal').get_attribute('href')
            self.driver.get(result_url)
            
            title = self.driver.find_element_by_id('productTitle').text
            price = self.driver.find_element_by_id('priceblock_ourprice').text
            
            urls.append(result_url)
            prices.append(price)
            titles.append(title)
            
            
            self.driver.get(self.fresh_url)
            
            time.sleep(1)
            
        
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
    recipe_title, recipe_ingr, fresh_ingr, time, serving_ct, instru, link = spn.get_random_recipe() 
    scrape = FreshScraper(fresh_ingr)
    urls, prices, ingr_names = scrape.search_items()
    
    ingredient_links = constructMail(urls, prices, ingr_names)
    mail.send_mail(ingredient_links)
    print('mail should be sent')
            
            
if __name__ == '__main__':
    main()