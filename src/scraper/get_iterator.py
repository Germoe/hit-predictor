# -*- coding: utf-8 -*-
import os
import click
import logging
from datetime import datetime
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
# Pandas
import pandas as pd
import iterator as iter_func
import inspect

iterator_functions = dict()
for x in inspect.getmembers(iter_func):
    if inspect.isfunction(x[1]):
        key = x[0]
        val = x[1]
        iterator_functions[key] = val

@click.command()
@click.argument('target', type=str)
@click.argument('reps', default=1, type=int)
def main(target,reps):
    """ 
    Create your own custom iterators in this function and then run `make iterator` in your console
    """
    output_filepath='./data/'
    subdir = 'iterators'
    
    for i in range(reps):
        filename = target + '.csv' # Define the filename to the csv file that contains the Zip codes that need to be scraped
        df = iterator_functions[target](target)

        if not os.path.exists(output_filepath + subdir):
            os.mkdir(output_filepath + subdir)
        df.to_csv(output_filepath + subdir + '/' + filename, sep='\t', index=False,encoding='utf-8')

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
