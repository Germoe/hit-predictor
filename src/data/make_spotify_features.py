import pandas as pd
import time
from pathlib import Path
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import dotenv

project_dir = os.path.join(os.path.dirname(__file__), os.pardir)
dotenv_path = os.path.join(project_dir, '.env')
dotenv.load_dotenv(dotenv_path)

iter_filepath = './data/iterators/spotify_ids_iterator.csv'
try:
    iterators = pd.read_csv(iter_filepath, sep='\t',dtype={'iterator': object})['iterator'].drop_duplicates().dropna()
except:
    raise ValueError('It doesn\'t look like you have a /data/iterators/spotify_ids_iterator.csv file. Make sure to run Hot 100 Wrangling Notebook until that iterator file is created.')
print(iterators.head())
print(len(iterators))
client_credentials_manager = SpotifyClientCredentials(client_id=os.getenv("SPOTIFY_CLIENT_ID"), client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"))
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
        df_dict = {'iterator': iterator}
        for key, value in zip(item.keys(),item.values()):
            df_dict[key] = [value]
        hits.append(pd.DataFrame(df_dict))
    songs = []
    df_hits = pd.concat(hits)
    df_hits.to_csv(path, sep='\t', encoding='utf-8',index=False)
    time.sleep(2)