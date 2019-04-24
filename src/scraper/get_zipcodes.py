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
# USzipcodes with geographic location
try:
    import zipcode
    zipcodepkg = True
except:
    zipcodepkg = False
from uszipcode import SearchEngine, Zipcode
# Pandas
import pandas as pd
# ZipcodeScraper
from models import ZipcodeScraper, Zipcodes

## ----------------------- Utils ------------------------

def print_progress(counter, zipcode, total, interval=500):
    # Prints a progress statement for every 500 records that were processed
    if counter % interval == 0:
        print("Progress: {} \n ID: {} \n Records: {}".format(counter,zipcode,total))


# Taken this function from https://github.com/ChrisMuir/Zillow/blob/master/zillow_functions.py
def zipcodes_list(st_items, zipcodepkg=False):
    print('in zipcodes list')
    # If st_items is a single zipcode string.
    if isinstance(st_items, str):
        # If st_items is the special keyword 'all' fetch all US zipcodes
        if st_items == 'all':
            st_items = ['0','1','2','3','4','5','6','7','8','9']
            if zipcodepkg:
                zc_objects = [n for i in st_items for n in zipcode.islike(str(i))]
            else:
                # Fallback to uszipcode package
                search = SearchEngine(simple_zipcode=True)
                zc_objects = []
                for st_item in st_items:
                    sub_set = [n for i in st_items for n in search.by_prefix(st_item, zipcode_type='Standard', returns=50000)]
                    zc_objects.extend(sub_set)
        else:
            if zipcodepkg:
                zc_objects = zipcode.islike(st_items)
            else:
                # Fallback to uszipcode package
                search = SearchEngine(simple_zipcode=True)
                zc_objects = search.by_prefix(st_items, zipcode_type='Standard', returns=50000)
    # If st_items is a list of zipcode strings.
    elif isinstance(st_items, list):
        if zipcodepkg:
            zc_objects = [n for i in st_items for n in zipcode.islike(str(i))]
        else:
            # Fallback to uszipcode package
            search = SearchEngine(simple_zipcode=True)
            zc_objects = []
            for st_item in st_items:
                sub_set = [n for i in st_items for n in search.by_prefix(st_item, zipcode_type='Standard', returns=50000)]
                zc_objects.extend(sub_set)
    else:
        raise ValueError("arg 'st_items' must be of type str or list")
    
    return(zc_objects)

# Set indentation level of pretty printer
pp = pprint.PrettyPrinter(indent=2)

@click.command()
# @click.argument('input_filepath', type=click.Path(exists=True))
# @click.argument('output_filepath', type=click.Path())
@click.option('--force',is_flag=True)
def main(input_filepath=None, output_filepath='./data/', force=False):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    zip_code_expiry = 180 # Time until zip code csv file expires and needs to be recreated
    rad = 100 # Radius to filter redundant zip codes. NOTE: Use the radius you're planning to scrape data at the Zipcodes filtering method will divide it by two to create the minimum amount of redundancy necessary.
    path = './data/zip_codes/zipcodes_' + str(rad) + '.csv' # Define the path to the csv file that contains the Zip codes that need to be scraped
    
    # Check date of csv creation or modification
    try:
        new_zip_codes = datetime.fromtimestamp(os.stat(path)[8]) > datetime.now() - timedelta(days=zip_code_expiry)
    except:
        new_zip_codes = False

    if new_zip_codes and not force:
        print('Zipcodes are up-to-date. Remove existing files or add --force to update anyways.')
        return

    # Create a new file with the necessary zip codes using this zipcode package (only works if zipcode is installed properly) otherwise uses uszipcode pkg
    all_zipcodes = zipcodes_list('all', zipcodepkg=zipcodepkg)
    us = Zipcodes(all_zipcodes)

    us_zip_filtered = us.filter_by_rad(rad=rad)
    us_zip_filtered = us_zip_filtered.set_index('zip')
    print(len(us_zip_filtered))
    
    us_zip_filtered.to_csv(output_filepath + 'zip_codes/zipcodes_' + str(rad) + '.csv', encoding='utf-8')
        

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
