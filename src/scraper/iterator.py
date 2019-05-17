# Iterator
import os
from dateutil import rrule
from datetime import datetime, timedelta

import pprint
# Pandas
import pandas as pd
# Spotiy Id
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time
from glob import glob

def week_saturday(target):
    first_week = datetime(1958, 8, 4)
    this_week = datetime(2019, 4, 13)
    weeks_iter = []
    for dt in rrule.rrule(rrule.WEEKLY, dtstart=first_week, until=this_week):
        weeks_iter.append(dt)

    return pd.DataFrame({'iterator':weeks_iter}), False

def init_count(target,filenames):
    try:
        scraped_rows = int(len(pd.read_csv('./data/iterators/'+ target +'.csv',sep='\t')))
        return cumul_row_count(filenames,scraped_rows)
    except:
        return 0

def cumul_row_count(filenames,scraped_rows):
    rows = 0
    for i, filename in enumerate(filenames):
        rows += int(len(pd.read_csv(filename,sep='\t',usecols=['date','rank','title','artist'])))
        if rows > scraped_rows:
            return i, rows
    return len(filenames), rows

def spotify_ids_hot100(target):
    client_credentials_manager = SpotifyClientCredentials(client_id='e3cddf5da81f43c3a33814866a8de8ed', client_secret='f885f6255fb34c90b8679817d9c63c25')
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    current_dir = os.getcwd()
    destination_dir = './data/interim/hot100'
    filenames = glob(destination_dir + '/*.csv') 
  
    count, start_pos = init_count(target,filenames)
    print(count)
    print(start_pos)

    if count >= 1:
        iter_df = pd.read_csv('./data/iterators/'+ target +'.csv',sep='\t')
    else:
        iter_df = pd.DataFrame(columns=columns)

    try:
        filename = filenames[count]
    except IndexError:
        print('It looks like the end of the filename list was reached.')
        return iter_df, True

    hot100_df = pd.read_csv(filename,sep='\t',usecols=['date','rank','title','artist'],
                            parse_dates=['date']).sort_values(by=['title','artist'])
    hot100_sample = hot100_df.loc[:,['title','artist']]
    print('length of sample:',len(hot100_sample))
    columns = ('iterator','filename','artist', 'title','spotify_artist','spotify_title','verified')

    iteration_count = 0
    for i,(track,artist) in enumerate(zip(hot100_sample['title'],hot100_sample['artist'])):
        i = i + (count * 100)
        if ((iter_df['title'] == track) & (iter_df['artist'] == artist)).any():
            iter_df.loc[i] = ['',filename,artist,track,'','','duplicate']
            continue
        q = track + ' ' + artist
        tracks = sp.search(q=q, type='track',market='US')
        try:
            items = tracks['tracks']['items']
            spotify_id = items[0]['id']
            spotify_title = items[0]['name']
            spotify_artist = ' & '.join(list([artist['name'] for artist in items[0]['album']['artists']]))
            verified = (track == spotify_title) and (artist == spotify_artist)
            iter_df.loc[i] = [spotify_id,filename,artist,track,spotify_artist,spotify_title, verified]
        except:
            iter_df.loc[i] = ['',filename,artist,track,'','','']
    print('no wait')
    return iter_df, False