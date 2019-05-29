# Iterator
import os
from dateutil import rrule
from datetime import datetime, timedelta
import re
import pprint
# Pandas
import numpy as np
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

def init_count(target_start,source):
    try:
        return source - target_start
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
    destination_dir = './data/interim/'
    iter_name = 'hot100_songs.csv' 
    source = pd.read_csv(destination_dir + iter_name,sep='\t').drop_duplicates(subset=['artist','title'])
    source['track_artist'] = source['title'] + ' ' + source['artist']

    columns = ('iterator','filename','artist', 'title','spotify_artist','spotify_title','verified')
    target_path = './data/iterators/'+ target +'.csv'
    try:
        target_df = pd.read_csv(target_path,sep='\t')
    except:
        target_df = pd.DataFrame(columns=columns)
    target_df['track_artist'] = target_df['title'] + ' ' + target_df['artist']
    
    iterator = source.loc[~source['track_artist'].isin(target_df['track_artist']) ,:]
    target_df.drop('track_artist',inplace=True,axis=1)

    print('Remaining: ', len(iterator))

    iteration_count = 1
    for i,(track,artist) in enumerate(zip(iterator['title'],iterator['artist'])):
        q = track.lower() + '              ' + artist.lower()
        tracks = sp.search(q=q, type='track',market='US')
        if len(tracks['tracks']['items']) == 0:
            q = q.replace('featuring',' ')
            q = q.replace('\"','')
            q = re.sub('([.|\.]*)','', q)
            tracks = sp.search(q=q, type='track',market='US')
            if len(tracks['tracks']['items']) == 0:
                q = q.replace('part iii','part 3')
                q = q.replace('part ii','part 2')
                q = q.replace('part i','part 1')
                q = q.replace('the','')
                q = re.sub('\(.+?\)','', q)
                tracks = sp.search(q=q, type='track')
        try:
            items = tracks['tracks']['items']
            spotify_id = items[0]['id']
            spotify_title = items[0]['name']
            spotify_artist = ' & '.join(list([artist['name'] for artist in items[0]['album']['artists']]))
            verified = (track == spotify_title) and (artist == spotify_artist)
            track_row = pd.DataFrame({'iterator':[spotify_id] ,'filename':[iter_name] ,'artist':[artist] , 'title':[track] ,'spotify_artist':[spotify_artist] ,'spotify_title':[spotify_title] ,'verified':[verified]})
        except:
            print(q)
            print(tracks['tracks']['items'])
            print('Track couldn\'t be found.')
            track_row = pd.DataFrame({'iterator':np.nan ,'filename':[iter_name] ,'artist':[artist] , 'title':[track] ,'spotify_artist': np.nan ,'spotify_title': np.nan ,'verified': np.nan})
        target_df = target_df.append(track_row)
        
        if iteration_count > 9:
            target_df.to_csv(target_path, sep='\t', index=False, encoding='utf-8')
            iteration_count = 1
            time.sleep(1)
        else:
            iteration_count = iteration_count + 1
            time.sleep(.3)
    print('no wait')
    return target_df, False