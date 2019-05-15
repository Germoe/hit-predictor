# NOTE: FOR COMMENTED VERSION OF THE WRANGLING PLEASE SEE THE NOTEBOOK "_Step 2 Wrangling (Hot 100 and Spotify Sample)"

# Read in all Subfiles
hot100_ids = pd.read_csv('../data/iterators/spotify_ids_hot100.csv',sep='\t').drop_duplicates(subset=['iterator'],keep='first')
hot100_ids_uniq = hot100_ids['iterator'].drop_duplicates()
hot100_ids_uniq.to_csv('../data/iterators/hot100_spotify_ids_iterator.csv',sep='\t')