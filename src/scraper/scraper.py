import requests as req
from pathlib import Path
import pandas as pd
import pprint as pp
import json
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def walmart(zip_code, path, proxies, timeout, radius):
    '''
        Add your custom Scrape function here. As an example you can find the scrape function to get Walmart Stores across the US.
        This example will scrape all Walmarts (does not include Sam's Club). You can fully customize this function.
        
        IMPORTANT: It's necessary that you name your function the same as your `target` keyword (e.g. in this case the target=walmart).
        
        For return statements make sure you return `False` for a failed or skipped scraping and `True` for a successful scraping.
    '''
    stores = []
    this = Path(path)
    if this.is_file():
        # Zip Code exists
        return False
    # Make sure the headers are still correct
    url="https://www.walmart.com/store/finder/electrode/api/stores?singleLineAddr={}&distance={}".format(zip_code.zip, radius)
    headers={ 'accept':'*/*',
            'accept-encoding':'gzip, deflate, br',
            'accept-language':'en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7',
            'cache-control':'max-age=0, no-cache, no-store',
            'upgrade-insecure-requests':'1',
            'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
    }
    get_store = req.get(url, 
        headers=headers, 
        proxies=proxies, 
        verify=False,
        timeout=timeout
    )
    try:
        store_response = get_store.json()
    except:
        print(get_store)
        print(get_store.status_code)
        print(get_store.text)
        raise JSONDecodeError("Expecting value from {}".format(get_store))
    stores_data = store_response.get('payload',{}).get("storesData",{}).get("stores",[])
    if not stores_data:
        print('no stores found near %s'%(zip_code.zip))
        stores = [{
                'name':'',
                'distance':'',
                'address':'',
                'zip_code':'',
                'city':'',
                'store_id':'',
                'phone':'',
        }]
    else:
        print('processing store details')
        #iterating through all stores
        for store in stores_data:
            store_id = store.get('id')
            display_name = store.get('displayName')
            address = store.get('address').get('address')
            postal_code = store.get('address').get('postalCode')
            city = store.get('address').get('city')
            phone = store.get('phone')
            distance = store.get('distance')

            data = {
                    'name':display_name,
                    'distance':distance,
                    'address':address,
                    'zip_code':postal_code,
                    'city':city,
                    'store_id':store_id,
                    'phone':phone,
            }
            stores.append(data)
    stores = pd.DataFrame(stores)
    stores.to_csv(path, sep='\t', encoding='utf-8')
    return True

def paul_mitchell(zip_code, path, proxies, timeout, radius):
    '''
        Add your custom Scrape function here. As an example you can find the scrape function to get Walmart Stores across the US.
        This example will scrape all Walmarts (does not include Sam's Club). You can fully customize this function.
        
        IMPORTANT: It's necessary that you name your function the same as your `target` keyword (e.g. in this case the target=walmart).
        
        For return statements make sure you return `False` for a failed or skipped scraping and `True` for a successful scraping.
    '''
    stores = []
    this = Path(path)
    if this.is_file():
        # Zip Code exists
        return False
    # Make sure the headers are still correct
    session = req.Session()

    # HEAD requests ask for *just* the headers, which is all you need to grab the session cookie
    session.head('https://locator.paulmitchell.com/SalonLocator/')

    response = session.post(
        url='https://locator.paulmitchell.com/SalonLocator/generateXML.php',
        data={
            'lat': zip_code.lat,
            'lng': zip_code.lng,
            'radius': radius
        },
        headers={
            'Referer': 'https://locator.paulmitchell.com/SalonLocator/locator.php?zip={}'.format(zip_code.zip)
        },
        proxies=proxies,
        timeout=timeout
    )

    try:
        df = pd.DataFrame(json.loads(response.text))
    except:
        print(response.status_code)
        print(response.text)
        raise Exception('Failed Request')
    df.to_csv(path, sep='\t', encoding='utf-8')
    return True

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
        dates = [date for i in range(100)]
        ranks = [rank.get_text().strip() for rank in soup.findAll("div", {"class": "chart-list-item__rank"})]
        titles = [title.get_text().strip() for title in soup.findAll("span", {"class": "chart-list-item__title-text"})]
        artists = [artist.get_text().strip() for artist in soup.findAll("div",{"class": "chart-list-item__artist"})]
        links = get_lyric_links(soup.findAll("div",{"class": "chart-list-item__text"}))
        equal_length = len(ranks) == len(titles) == len(artists) == len(dates) == len(links)
        if equal_length:
            df = pd.DataFrame({'date': dates,'rank': ranks, 'title': titles, 'artist': artists, 'link': links})
            df = df.set_index('rank',drop=True)
            df.to_csv(path, sep='\t', encoding='utf-8')
    except:
        print(response.status_code)
        raise Exception('Failed Request')
    return True

client_credentials_manager = SpotifyClientCredentials(client_id='e3cddf5da81f43c3a33814866a8de8ed', client_secret='f885f6255fb34c90b8679817d9c63c25')
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