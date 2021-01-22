from prettyconf import config

API_CONSUMER_KEY = config('API_CONSUMER_KEY')
API_CONSUMER_SECRET = config('API_CONSUMER_SECRET')
API_ACCESS_TOKEN = config('API_ACCESS_TOKEN')
API_ACCESS_TOKEN_SECRET = config('API_ACCESS_TOKEN_SECRET')

LOGFILE_NAME = config('LOGFILE_NAME', default='twiffle.log')
LOGFILE_ROTATION = config('LOGFILE_ROTATION', default='10MB')
LOGFILE_RETENTION = config('LOGFILE_RETENTION', default=5, cast=int)

TWITTER_STATUS_BASE_URL = config(
    'TWITTER_STATUS_BASE_URL', default='https://twitter.com/twitter/statuses/'
)

DATABASE_NAME = config('DATABASE_NAME', default='twiffle.db')
