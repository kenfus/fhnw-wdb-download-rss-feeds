### Parameters
RUN_ONCE = False
SECONDS_TO_SLEEP_FOR_NEXT_REQUEST = 30 # in seconds
BACKUP_TIME = 30 # INT: Every X minutes a Backup of the data is done.
BACKUP_FILE_PATH_NAME = "Backup_RSS_Feed-scrap.csv" #Backup file name with .csv
# URLSs to RSS-Feeds
SRF_FEED = "https://www.srf.ch/news/bnf/rss/1646"
NZZ_FEED = "https://www.nzz.ch/recent.rss"
TA_FEED = "https://partner-feeds.publishing.tamedia.ch/rss/tagesanzeiger/ticker"
BLICK_FEED = "https://www.blick.ch/news/rss.xml"
AGZ_FEED = "https://www.aargauerzeitung.ch/rss2.xml"

# Array of urls to News RSS-Feeds
RSS_FEEDS = [SRF_FEED, TA_FEED, BLICK_FEED, NZZ_FEED, AGZ_FEED]
NAME_OF_FEEDS = ['SRF',  'TA', 'Blick', 'NZZ', 'AGZ']