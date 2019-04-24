# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
import requests as req
from bs4 import BeautifulSoup
import pandas as pd
import os

from dateutil import rrule
from datetime import datetime, timedelta

def get_text(html):
    return html.get_text().strip()

@click.command()
# @click.argument('input_filepath', type=click.Path(exists=True))
# @click.argument('output_filepath', type=click.Path())
def main():

    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """

    first_week = datetime(1958, 08, 04)
    this_week = datetime(2019, 04, 13)
    weeks_iter = []
    for dt in rrule.rrule(rrule.WEEKLY, dtstart=first_week, until=this_week):
        weeks_iter.append(dt)

    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

    hits = []
    
    response = req.get(
        url='https://www.billboard.com/charts/hot-100/2019-04-06'
    )

    html = response.text
    soup = BeautifulSoup(html,'html.parser')
    date = soup.findAll("button", {"class": "chart-detail-header__date-selector-button"})
    print(date[0].get_text().strip())
    hot100s = []
    date = get_text(date[0])
    dates = [date for i in range(100)]
    ranks = [get_text(rank) for rank in soup.findAll("div", {"class": "chart-list-item__rank"})]
    titles = [get_text(title) for title in soup.findAll("span", {"class": "chart-list-item__title-text"})]
    artists = [get_text(artist) for artist in soup.findAll("div",{"class": "chart-list-item__artist"})]
    equal_length = len(ranks) == len(titles) == len(artists) == len(dates)
    if equal_length:
        df = pd.DataFrame({'date': dates,'rank': ranks, 'title': titles, 'artist': artists})
        outdir = './data/interim/hot100'
        if not os.path.exists(outdir):
            os.mkdir(outdir)
        df.to_csv(outdir + '/' + date.replace(' ','_').replace(',','') + '.csv')



if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
