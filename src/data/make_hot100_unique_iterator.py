# NOTE: FOR COMMENTED VERSION OF THE WRANGLING PLEASE SEE THE NOTEBOOK "_Step 2 Wrangling (Hot 100 and Spotify Sample)"
import pandas as pd

# Read in all Subfiles
hot100_ids = pd.read_csv('./data/iterators/spotify_ids_hot100.csv',sep='\t')
hot100_ids_uniq = hot100_ids.drop_duplicates(subset=['iterator']).dropna(subset=['iterator'])
hot100_ids_uniq.to_csv('./data/iterators/spotify_ids_hot100_uniq.csv',sep='\t')