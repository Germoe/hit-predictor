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

    return pd.DataFrame({'iterator':weeks_iter})