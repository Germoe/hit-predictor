# Sampling Spotify Data

"""
In the next step we'll generate a sample from Spotify data that roughly resembles the 
distribution by year we've seen in the Hot 100 data. To capture the breadth of various songs 
we'll sample ~20% of our spotify songs from the 10% least popular songs on Spotify. This is 
taking into account that by using the Spotify Search we're only able to sample from the 10000 
most popular songs of a year (according to Spotify their popularity score tends to emphasize 
CURRENT popularity). 

To avoid sampling too many overly popular songs we're going to take random samples from the 
first 10000 search results (in chunks of 50 songs) and we're going to slightly oversample 
so as to be able to remove the overlap in a later step.
"""

from pprint import pprint
import json
import ast
import spotipy
import random
import math
from spotipy.oauth2 import SpotifyClientCredentials
import dotenv

project_dir = os.path.join(os.path.dirname(__file__), os.pardir)
dotenv_path = os.path.join(project_dir, '.env')
dotenv.load_dotenv(dotenv_path)

client_credentials_manager = SpotifyClientCredentials(client_id=os.getenv("SPOTIFY_CLIENT_ID"), client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"))
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Set Current Working Directory to ../

def round_up(x, base=50):
    return base * math.ceil(x/base)

target_path = './data/interim/spotify_songs.csv'

try:
    sampling_df = pd.read_csv(target_path,sep='\t',parse_dates=['album.release_date'])
except:
    print('Sampling Songs from Spotify - Beware that a client and secret is necessary for this method.')
    
    output_filepath = './data/interim/'
    temp_dir = 'spotify_sampling_temp'
    skip = 0

    if not os.path.exists(output_filepath + temp_dir):
        os.mkdir(output_filepath + temp_dir)
    else:
        for file in iglob(output_filepath + temp_dir + '/*.csv'):
            m = re.search('sampling_([0-9]+?).csv$', file)
            if m:
                file_nr = int(m.group(1))
                if file_nr > skip:
                    skip = file_nr
    
    # Seed random function            
    np.random.seed(500)
    
    # Sampling Additional Songs By Year
    years = sorted(hits_uniq['year'].unique())
    spotify_song_sets = []
    ceil_to = 100
    for i, year in enumerate(years):
        file_nr = i + 1
        if file_nr <= skip:
            print('skip:', file_nr)
            continue
        start = 0
        tracks = []
        len_hot100 = len(hits_uniq_no_nan.loc[hits_uniq['year'] == year,'year'])
        print(year)
        print("Number of Songs for {}: {}".format(year,len_hot100))
        len_k_tracks = round_up(len_hot100 * 0.8,base=ceil_to)
        k = int(len_k_tracks / 50)
        len_low_k_tracks = round_up(len_hot100 * 0.2,base=ceil_to)
        low_k = int(len_low_k_tracks / 50)
        print("Number of Songs Sampled from high popularity: {}".format(len_k_tracks))
        print("Number of Songs Sampled from low popularity: {}".format(len_low_k_tracks))
        offsets = (x for x in np.random.choice(np.arange(0,10000,50),k,replace=False))
        while len(tracks) < len_k_tracks:
            offset = next(offsets)
            tracks.extend(sp.search(q='year:' + str(year),type='track',limit=50,offset=offset,market='us')['tracks']['items'])
        # Fetch Hipster Tags (lowest 10% popularity)
        start = 0
        while (len(tracks) - len_k_tracks) < len_low_k_tracks:
            tracks.extend(sp.search(q='year:' + str(year),type='track',limit=50,offset=start,market='us')['tracks']['items'])
            start = start + 50
        time.sleep(3)
        spotify_songs = pd.DataFrame(pd.io.json.json_normalize(tracks))
        
        spotify_songs.to_csv(output_filepath + temp_dir + '/sampling_' + str(file_nr) + '.csv',sep='\t',index=False)
    
    subfiles_sampling = [pd.read_csv(file,sep='\t') for file in iglob(output_filepath + temp_dir + '/sampling_*.csv')]

    sampling_df = pd.concat(subfiles_sampling).reset_index(drop=True)
    sampling_df.to_csv(target_path,sep='\t',index=False)
    
    # Clean up temp files
    [os.remove(file) for file in iglob(output_filepath + temp_dir + '/sampling_*.csv')]
    try:
        os.remove(output_filepath + temp_dir + '/.DS_Store')
    except:
        print('No .DS_Store file. You\'re all set!')

    os.rmdir(output_filepath + temp_dir)

sampling_df['album.release_date'] + pd.to_timedelta((6 - sampling_df['album.release_date'].dt.dayofweek), unit='d')

# Create String of artists
sampling_df['artist'] = [' + '.join([artist['name'] for artist in ast.literal_eval(artists)]) for artists in sampling_df['artists']]
sampling_df['album.release_date'] = pd.to_datetime(sampling_df['album.release_date'])
sampling_df.rename(columns={'name':'title'},inplace=True)
# Add or deduct days of 'album.release_date' to get to the following Saturday (Hot 100 dates are set as Saturdays)
saturday = 5
sampling_df['date'] = sampling_df['album.release_date'] + pd.to_timedelta((saturday - sampling_df['album.release_date'].dt.dayofweek), unit='d')
sampling_df['year'] = sampling_df['date'].dt.year
sampling_df['month'] = sampling_df['date'].dt.month
sampling_df['day'] = sampling_df['date'].dt.day
spotify_songs = sampling_df.loc[:,['id','title','artist','album.id','album.name','year','month','day','date','album.release_date','duration_ms','popularity','uri']]
spotify_songs = spotify_songs.drop_duplicates()

spotify_songs['orig_artist'] = spotify_songs.loc[:,'artist']
spotify_songs['orig_title'] = spotify_songs.loc[:,'title']

spotify_songs = wrangle_artist_title(spotify_songs,artist_col='orig_artist',title_col='orig_title')

duplicates = pd.merge(hits_uniq.loc[:,['orig_artist','orig_title']],spotify_songs.loc[:,['orig_artist','orig_title']],on=['orig_artist','orig_title'],how='inner')

spotify_songs['orig_artist_title'] = spotify_songs['orig_artist'] + ' ' + spotify_songs['orig_title']
duplicates['orig_artist_title'] = duplicates['orig_artist'] + ' ' + duplicates['orig_title']

# Remove Songs that are also in the Hot 100
nhits = spotify_songs.loc[~(spotify_songs['id'].isin(hot100_processed['iterator']) | spotify_songs['orig_artist_title'].isin(duplicates['orig_artist_title'])),:]
overlap = spotify_songs.loc[spotify_songs['id'].isin(hot100_processed['iterator']) | spotify_songs['orig_artist_title'].isin(duplicates['orig_artist_title']),:]
print("{} Songs had to be removed as they overlap with Hot 100 Data".format(len(overlap)))

years = len(nhits['year'].unique())
spotify_uniq_by_year = nhits.groupby(by='year').count()

fig = plt.figure(figsize=(16,6))
data=pd.concat([spotify_uniq_by_year['id'],hits_uniq_by_year['total']],axis=1)
data.columns = ['spotify','hot100']

data_ratio = pd.DataFrame(index=data.index)
data_ratio['ratio'] = (data['spotify'] - data['hot100'])
data_ratio.reset_index(inplace=True)

data.reset_index(inplace=True)
data = data.melt(id_vars=['year'])
data.columns = ['year','dataset','value']

title='Spotify Song Sample Distribution'
ylabel='Year'
xlabel='Number of Songs'

_ = sns.scatterplot(x='year',y='value',hue='dataset',data=data)
_ = plt.title(title)
_ = plt.xlabel(xlabel)
_ = plt.ylabel(ylabel)
_ = plt.legend(loc='upper left')
_ = plt.twinx()
_ = sns.lineplot(x='year',y='ratio',data=data_ratio,label='Diff Spotify - Hot 100')
_ = plt.legend(loc='upper right')
_ = plt.yticks(np.arange(-300,350,100))
_ = plt.grid(False)

total_spotify = data.loc[data['dataset'] == 'spotify','value'].sum()
total_hot100 = data.loc[data['dataset'] == 'hot100','value'].sum()
print("Total Spotify Songs: {}\nTotal Hot 100 Songs: {}\nSpotify to Hot 100 ratio: {}\nSpotify/Total: {}%".format(total_spotify,total_hot100,round(total_spotify/total_hot100,4),round(total_spotify/(total_spotify+total_hot100),4)*100))

# The above graph shows the Spotify Sample compared to the Hot 100 Data. We can see that the two datasets are almost equally distributed. The Line Graph ("Diff Spotify Hot 100") shows absolute count differences between Spotify and the Hot 100 Data and we can see that the Spotify song set is minimally larger (i.e. Spotify songs make up 51.92% of all songs).

# Create Iterator for data set 
spotify_songs_iterator = nhits.drop_duplicates()['id'].to_frame()
spotify_songs_iterator.columns = ['iterator']
spotify_songs_iterator.to_csv('./data/iterators/spotify_songs_ids_iterator.csv',sep='\t',index=False,encoding='utf-8')