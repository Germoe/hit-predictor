# -*- coding: utf-8 -*-
import click
import logging
import pprint
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
# Scraping and IP rotation
import requests as req
from lxml.html import fromstring
from itertools import cycle
import traceback
# Pandas
import pandas as pd
# Headless Scraper
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

## ----------------------- Utils ------------------------

def print_progress(counter, zipcode, total, interval=500):
    # Prints a progress statement for every 500 records that were processed
    if counter % interval == 0:
        print("Progress: {} \n ID: {} \n Records: {}".format(counter,zipcode,total))

# Set indentation level of pretty printer
pp = pprint.PrettyPrinter(indent=2)

def check_proxy(proxy, timeout=3):
    '''
        Make sure that input proxy are responsive
    '''
    proxies = {"http": proxy, "https": proxy}
    url = 'https://httpbin.org/ip'
    try:
        response = req.get(url,proxies=proxies, timeout=timeout)
        print(response.json())
        return True
    except:
        return False

def validate_proxies(proxies):
    valid_proxies = []
    for proxy in proxies:
        if check_proxy(proxy):
            valid_proxies.append(proxy)
    return valid_proxies


def scrape_proxies(url, xpath_tbody_tr, xpath_scrape_condition, xpath_ip, xpath_port, xpath_next_disable_condition=None, xpath_next_a=None, timeout=10, ip_port=None):
    # create Proxy Set
    proxies = set()
    # initialize webdriver
    options = Options()
    if ip_port:
        # Checks if a specific ip and port were set to fetch proxies otherwise uses computer credentials
        options.add_argument('--proxy-server=' + ip_port)
    driver = webdriver.Chrome(chrome_options=options)
    driver.set_page_load_timeout(timeout)
    try:
        driver.get(url)
    except:
        print('timeout')
        return proxies
    try:
        next_page = True
        counter = 1
        while next_page:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath_tbody_tr))
            )
            for i in element.find_elements_by_xpath(xpath_tbody_tr):
                # condition to scrape
                try:
                    i.find_element_by_xpath(xpath_scrape_condition)
                except:
                    continue
                #Grabbing IP and corresponding PORT
                proxy = ":".join([i.find_element_by_xpath(xpath_ip).text, i.find_element_by_xpath(xpath_port).text])
                proxies.add(proxy)
            try:
                if element.find_element_by_xpath(xpath_next_disable_condition):
                    next_page = True
            except:
                next_page = False
            if next_page:
                if driver and element:
                    driver.find_element_by_xpath(xpath_next_a).click()
                    counter += 1
                    print('Next Page: ', counter)
            else:
                print('End of Site')
    finally:
        driver.quit()
    return proxies

# Utility for Random Proxies
def get_proxies(ip_territory=None, ip_port=None):
    proxies = set()
    # free-proxy-list
    if not ip_territory or ip_territory=='all':
        url = 'https://free-proxy-list.net/'
    elif ip_territory == 'US':
        url = 'https://www.us-proxy.org/'
    proxies_free_proxy_set = scrape_proxies(url, xpath_tbody_tr='//tbody/tr', xpath_scrape_condition='.//td[7][contains(text(),"yes")]', xpath_ip='.//td[1]', xpath_port='.//td[2]', xpath_next_disable_condition="//li[@id='proxylisttable_next'][not(contains(@class, 'disabled'))]", xpath_next_a="//li[@id='proxylisttable_next']/a", ip_port=ip_port)
    proxies.update(proxies_free_proxy_set)
    # proxynove.com
    if not ip_territory:
        url = 'https://www.proxynova.com/proxy-server-list/'
        proxies_hidemyname = scrape_proxies(url, xpath_tbody_tr='//tbody/tr', xpath_scrape_condition='.//td[7]/span[contains(text(),"Elite")]', xpath_ip='.//td[1]', xpath_port='.//td[2]', ip_port=ip_port)
        proxies.update(proxies_hidemyname)

    # proxy.rudnkh.me/txt
    if not ip_territory:
        url = 'https://proxy.rudnkh.me/txt'
        try:
            if ip_port:
                proxies_settings = {"http": ip_port, "https": ip_port}
                response = req.get(url, proxies=proxies_settings)
            else:
                response = req.get(url)
            proxies_rudnkh = set(response.text.split('\n'))
            proxies.update(proxies_rudnkh)
        except:
            print('rudnkh not reachable')

    # remove empty values
    proxies.discard('')

    return proxies


@click.command()
@click.option('--ip_territory',default=None,type=str)
@click.option('--ip_port',default=None,type=str)
@click.option('--force',is_flag=True)
def main(ip_territory, ip_port, force=False):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """

    output_filepath = './data/proxies'
    if not os.path.exists(output_filepath):
        os.mkdir(output_filepath)

    # Round Robin proxy rotation
    if ip_territory:
        path = output_filepath + '/proxies_' + ip_territory + '.csv'
    else:
        path = output_filepath + '/proxies.csv'
    # Check date of csv creation or modification
    try:
        new_proxies = datetime.fromtimestamp(os.stat(path)[8]) > datetime.now() - timedelta(minutes=30)
    except:
        new_proxies = False
    if not new_proxies or force:
        proxies = get_proxies(ip_territory=ip_territory, ip_port=ip_port)
        proxies = validate_proxies(proxies)
        proxy_df = pd.DataFrame(proxies, columns=['ip'])
        if len(proxy_df) > 0:
            proxy_df.to_csv(path, sep='\t', encoding='utf-8')
        else:
            raise Exception('No Responsive Proxies found.')
    else:
        print('Proxies are up-to-date.')

    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
