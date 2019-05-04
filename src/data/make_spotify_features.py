import pandas as pd
import time
from pathlib import Path
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


iter_filepath = './data/iterators/spotify_ids_filled.csv'
iterators = pd.read_csv(iter_filepath, sep='\t',dtype={'iterator': object})['iterator'].drop_duplicates().dropna()
print(iterators.head())
print(len(iterators))
client_credentials_manager = SpotifyClientCredentials(client_id='e3cddf5da81f43c3a33814866a8de8ed', client_secret='f885f6255fb34c90b8679817d9c63c25')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

songs = []
start = 0

for i, iterator in enumerate(iterators):
    if type(iterator) == float:
        continue
    if len(songs) == 0:
        start = i
    songs.append(iterator)
    if (len(songs) < 50) and (i != len(iterators) - 1):
        continue
    else:
        end = i
        print(end)
    path = './data/interim/spotify_features' + '/' + 'spotify_features' + '_' + str(start) + '_' + str(end) + '.csv'
    this = Path(path)
    if this.is_file():
        # Iterator exists
        # return False
        songs = []
        print('exists already')
        continue
    response = sp.audio_features(songs)
    hits = []
    for item, iterator in zip(response,songs):
        df_dict = {'name': iterator}
        for key, value in zip(item.keys(),item.values()):
            df_dict[key] = [value]
        hits.append(pd.DataFrame(df_dict))
    songs = []
    df_hits = pd.concat(hits)
    df_hits.to_csv(path, sep='\t', encoding='utf-8',index=False)
    time.sleep(2)