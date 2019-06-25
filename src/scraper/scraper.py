import requests as req
from pathlib import Path
import pandas as pd
import pprint as pp
import json
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
# Import API importers
import musicbrainzngs

def hot100(iterator, path, proxies, timeout):
    '''
        Add your custom Scrape function here. As an example you can find the scrape function to get Walmart Stores across the US.
        This example will scrape all Walmarts (does not include Sam's Club). You can fully customize this function.
        
        IMPORTANT: It's necessary that you name your function the same as your `target` keyword (e.g. in this case the target=walmart).
        
        For return statements make sure you return `False` for a failed or skipped scraping and `True` for a successful scraping.
    '''

    hits = []
    this = Path(path)
    if this.is_file():
        # Iterator exists
        return False
    
    response = req.get(
        url='https://www.billboard.com/charts/hot-100/' + iterator
    )

    def get_lyric_links(divs):
        links = []
        for div in divs:
            href = ''
            try:
                href = div.find('div',{"class": "chart-list-item__lyrics"}).find('a').get('href')
            except:
                pass
            links.append(href)
        return links

    try:
        html = response.text
        soup = BeautifulSoup(html,'html.parser')
        date = soup.findAll("button", {"class": "chart-detail-header__date-selector-button"})
        hot100s = []
        date = date[0].get_text().strip()
        ranks = [rank.get_text().strip() for rank in soup.findAll("div", {"class": "chart-list-item__rank"})]
        titles = [title.get_text().strip() for title in soup.findAll("span", {"class": "chart-list-item__title-text"})]
        artists = [artist.get_text().strip() for artist in soup.findAll("div",{"class": "chart-list-item__artist"})]
        links = get_lyric_links(soup.findAll("div",{"class": "chart-list-item__text"}))
        equal_length = len(ranks) == len(titles) == len(artists) == len(ranks)
        
        array_len = len(ranks)
        dates = [date for i in range(100)]
        dates = [date for i in range(array_len)]
        if not equal_length:
            print('not equal length')
        df = pd.DataFrame({'date': dates,'rank': ranks, 'title': titles, 'artist': artists, 'link': links})
        df = df.set_index('rank',drop=True)
        df.to_csv(path, sep='\t', encoding='utf-8')
    except:
        print(response.status_code)
        raise Exception('Failed Request')
    return True

client_credentials_manager = SpotifyClientCredentials(client_id=os.getenv('SPOTIFY_CLIENT_ID'), client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'))
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def spotify_analysis_api(iterator, path, proxies, timeout):
    '''
        Add your custom Scrape function here. As an example you can find the scrape function to get Walmart Stores across the US.
        This example will scrape all Walmarts (does not include Sam's Club). You can fully customize this function.
        
        IMPORTANT: It's necessary that you name your function the same as your `target` keyword (e.g. in this case the target=walmart).
        
        For return statements make sure you return `False` for a failed or skipped scraping and `True` for a successful scraping.
    '''

    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    this = Path(path)
    if this.is_file():
        # Iterator exists
        print('iterator exists')
        return False
    response = sp.audio_features(iterator)
    hits = []
    for item, spotify_id in zip(response,iterator):
        df_dict = {'name': spotify_id}
        for key, value in zip(item.keys(),item.values()):
            df_dict[key] = [value]
        hits.append(pd.DataFrame(df_dict))
    df_hits = pd.concat(hits)
    df_hits.to_csv(path, sep='\t', encoding='utf-8',index=False)
    return True

def comparison_data_analysis_api(iterator, path, proxies, timeout):
    '''
        Add your custom Scrape function here. As an example you can find the scrape function to get Walmart Stores across the US.
        This example will scrape all Walmarts (does not include Sam's Club). You can fully customize this function.
        
        IMPORTANT: It's necessary that you name your function the same as your `target` keyword (e.g. in this case the target=walmart).
        
        For return statements make sure you return `False` for a failed or skipped scraping and `True` for a successful scraping.
    '''

    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    this = Path(path)
    if this.is_file():
        # Iterator exists
        print('iterator exists')
        return False
    response = sp.audio_features(iterator)
    hits = []
    for item, spotify_id in zip(response,iterator):
        df_dict = {'name': spotify_id}
        try:
            for key, value in zip(item.keys(),item.values()):
                df_dict[key] = [value]
        except:
            print('couldn\'t find {}'.format(spotify_id))
        hits.append(pd.DataFrame(df_dict,index=[spotify_id]))
    df_hits = pd.concat(hits,sort=True)
    df_hits.to_csv(path, sep='\t', encoding='utf-8',index=False)
    return True

# Set musicbrainz crednetials
musicbrainzngs.set_rate_limit(limit_or_interval=1.0, new_requests=1)
musicbrainzngs.set_useragent('hit_predictor', '0.0.1', 'me@sebastian-engels.com')
musicbrainzngs.set_format(fmt='xml')

def musicbrainz_ids_by_isrc():
    res = musicbrainzngs.search_recordings(query='')
    res = musicbrainzngs.browse_events(area=None, artist='650e7db6-b795-4eb5-a702-5ea2fc46c848', place=None, includes=[], limit=100, offset=None)
    pp.pprint(res)

def sample_tracks_by_year():
    import spotipy
    import random
    from spotipy.oauth2 import SpotifyClientCredentials
    client_credentials_manager = SpotifyClientCredentials(client_id=os.getenv('SPOTIFY_CLIENT_ID'), client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'))
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def round_up(x, base=50):
        return base * round(x/base)

    # Sampling Additional Songs By Year
    years = sorted(hot100_uniq['year'].unique())
    for year in years:
        start = 0
        tracks = []
        len_hot100 = len(hot100_uniq.loc[hot100_uniq['year'] == year,'year'])
        print("Number of Songs for {}: {}".format(year,len_hot100))
        len_k_tracks = round(len_hot100 * 0.8 / 50) * 50
        k = int(len_k_tracks / 50)
        len_low_k_tracks = round(len_hot100 * 0.2 / 50) * 50
        low_k = int(len_low_k_tracks / 50)
        print("Number of Songs Sampled from high popularity: {}".format(len_k_tracks))
        print("Number of Songs Sampled from low popularity: {}".format(len_low_k_tracks))
        np.random.seed(500)
        offsets = (x for x in np.random.choice(np.arange(0,10000,50),k,replace=False))
        while len(tracks) < len_k_tracks:
            offset = next(offsets)
            tracks.extend(sp.search(q='year:' + str(year),type='track',limit=50,offset=offset)['tracks']['items'])
        # Fetch Hipster Tags (lowest 10% popularity)
        start = 0
        while (len(tracks) - len_k_tracks) < len_low_k_tracks:
            tracks.extend(sp.search(q='year:' + str(year),type='track',limit=50,offset=start)['tracks']['items'])
            start = start + 50