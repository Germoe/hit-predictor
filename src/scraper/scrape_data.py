# -*- coding: utf-8 -*-
import click
import logging
import pprint
import json
import os
import time
import random
import re
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
# Import the Scrape Function defined in scraper.py
import scraper as scrape_func
from models import Scraper, ZipcodeScraper, APIScraper
import inspect

## ----------------------- Utils ------------------------

def print_progress(counter, zip_code, total, interval=500):
    # Prints a progress statement for every 500 records that were processed
    if counter % interval == 0:
        print("Progress: {} \n ID: {} \n Records: {}".format(counter,zip_code,total))

# Set indentation level of pretty printer
pp = pprint.PrettyPrinter(indent=2)

scrape_functions = dict()
for x in inspect.getmembers(scrape_func):
    if inspect.isfunction(x[1]):
        key = x[0]
        val = x[1]
        scrape_functions[key] = val

@click.command()
@click.argument('target', type=str) # Target is the identifier for the scraped url, destination directory and name (e.g. walmart)
@click.argument('scrapetype', default='iterator',type=str) # Scraper Type defines the iteration unit or type of scraper that will be used (e.g. zipcode)
@click.argument('scrapespeed',default='regular',type=str)
@click.argument('batch',default=False,type=bool)
@click.argument('batch_size',default=50,type=int)
@click.argument('iter_filepath',default=None,type=str) # Necessary for scraper type `iterator` -- create using `make iterator` and custom function in get_iterator.py
@click.option('--ip_territory',default=None,type=str)
@click.option('--ip_port',default=None,type=str) # This option is not tied to any action
@click.option('--force',is_flag=True)
def main(target, scrapetype, ip_territory, ip_port, scrapespeed, iter_filepath,batch,batch_size, force=False):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    print('target',target,'scrapetype',scrapetype,'ip_territory',ip_territory,'ip_port',ip_port,'scrapespeed',scrapespeed,'iter_filepath',iter_filepath,'batch',batch,'batch_size',batch_size,'force',force)
    if scrapetype.lower() == 'zipcode':
        scraper = ZipcodeScraper(target)
        radius = 100 # Set Scrape Radius
        scraper.set_radius(radius)
    elif scrapetype.lower() == 'iterator':
        # Most common iterator
        scraper = Scraper(target)
    elif scrapetype.lower() == 'api':
        # Most common iterator
        scraper = APIScraper(target)

    # Read in proxies
    if ip_territory:
        ip_path = './data/proxies/proxies_' + ip_territory + '.csv'
    else:              
        ip_path = './data/proxies/proxies.csv'

    scrape_limit = scraper.init_proxies(ip_path, force)
    scraper.set_speed(scrapespeed)
    print('Scrape Limit: {} units'.format(scrape_limit))
    if scrapetype.lower() == 'zipcode':
        # Read in Zip Codes. Zipcodes csv need to have columns = ['zip','lat','lng','type']
        if radius:
            zip_codes_file = './data/zip_codes/zipcodes_' + str(radius) + '.csv'
        else:
            zip_codes_file = './data/zip_codes/zipcodes_100.csv'
        scraper.init_zipcodes(zip_codes_file)
    elif scrapetype.lower() == 'iterator':
        iterator_list = pd.read_csv(iter_filepath, dtype={'iterator': object})
        scraper.init_iterator(iterator_list)
    elif scrapetype.lower() == 'api':
        iterator_list = pd.read_csv(iter_filepath, dtype={'iterator': object},sep='\t')
        scraper.init_iterator(iterator_list)

    scraper.init_scraper(scrape_functions[target])
    scraper.scrape(batch=batch,batch_size=batch_size)

    print('done')

    # ------- Redken --------
    # HEAD requests ask for *just* the headers, which is all you need to grab the
    # session cookie
    # session.head('https://www.redken.com/salon-finder')

    # response = session.post(
    #     url='https://storelocator.api.lorealebusiness.com/api/SalonFinderservice/GetSalonFinderstores',
    #     data={
    #         'radius': 5,
    #         'storesperpage': 5,
    #         'pagenum': 1,
    #         'latitude': 29.9339046,
    #         'longitude': -90.03053899999998,
    #         'brand': 'Redken',
    #         'Nametype': 'N',
    #         'IsCurrentloc': False
    #     },
    #     headers={
    #         'Referer': 'https://www.redken.com/salon-finder?search=20010'
    #     }
    # )

    # pp.pprint(json.loads(response.text))

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
