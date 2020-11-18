import feedparser
from datetime import datetime, timedelta
from time import mktime
import pandas as pd
import numpy as np
import time
from parameters import *
import sys

###Helper Functions
def ts_to_dt(t_struct):
    '''
    Transforms a time.struct_time into a datetime-object
    '''
    return datetime.fromtimestamp(mktime(t_struct))

def dt_to_str(dt, time_format = "%Y/%m/%d, %H:%M:%S"):
    '''
    Transform a datetime object to string
    '''
    return dt.strftime(time_format)


###Main Function
def start_scraping_rss(FIRST_RUN):

    '''
    This function scraps the RSS-Feeds as defined in parameters.py. It needs a parameter FIRST_RUN, which is a boolean.
    '''
    ### Preprocess
    dict_of_feeds = zip(NAME_OF_FEEDS, RSS_FEEDS)
    column_for_dataframe = ['date', 'Newspaper', 'title', 'link', 'summary']
    df = pd.DataFrame(columns = column_for_dataframe)
    next_backup = datetime.now() + timedelta(minutes=BACKUP_TIME)
    RUNNING = True
    ###
    
    while RUNNING:
        if FIRST_RUN:
            FIRST_RUN = False
            for name_newspaper, url_rss in dict_of_feeds:
                d = feedparser.parse(url_rss)
                for entry in d['entries']:
                    try:
                        df_ = pd.DataFrame([[ts_to_dt(entry['published_parsed']), name_newspaper, entry['title'], entry['link'], entry['summary']]], columns = column_for_dataframe)
                        df_.sort_values(by='date', inplace=True)
                    except KeyError as E:
                        continue
                    
                    df = df.append([df_], ignore_index = True)
                    df.sort_values(by=['Newspaper', 'date'], inplace=True)
                    df.to_csv(BACKUP_FILE_PATH_NAME, index = False)

            if RUN_ONCE:
                RUNNING = False
            print("First run done!")
            continue


        for name_newspaper, url_rss in dict_of_feeds:
            d = feedparser.parse(url_rss)
            for entry in d['entries']:
                try:
                    df_ = pd.DataFrame([[ts_to_dt(entry['published_parsed']), name_newspaper, entry['title'], entry['link'], entry['summary']]], columns = column_for_dataframe)
                except KeyError as E:
                    continue
                # Append to overall DataFrame:
                df = df.append([df_], ignore_index = True)
                df.drop_duplicates(inplace=True) # Drop Duplicates because currently its not smart with dates. Many RSS-Feeds don't tell us when it was updated. 
                df.sort_values(by=['Newspaper', 'date'], inplace=True)

        # Backup and reset Dataframe:
        if datetime.now() > next_backup:
            backup = pd.read_csv(BACKUP_FILE_PATH_NAME)
            df = backup.append([df], ignore_index = True)
            df.drop_duplicates(inplace=True) # Drop Duplicates because currently its not smart with dates. Many RSS-Feeds don't tell us when it was updated. 
            df.sort_values(by=['Newspaper', 'date'], inplace=True)
            df.to_csv(BACKUP_FILE_PATH_NAME, index = False)
            df.drop_duplicates(subset = 'Newspapers', keep = 'last', inplace=True) # Keep one entry per newspapers. Keep the newest ones, which are appended at the end of the Dataframe.

            next_backup = datetime.now() + timedelta(minutes=BACKUP_TIME)
            print("Backup done!")
        print("Sleeping....")
        time.sleep(SECONDS_TO_SLEEP_FOR_NEXT_REQUEST)
        
if __name__ == "__main__":
    start_scraping_rss(sys.argv[0])

