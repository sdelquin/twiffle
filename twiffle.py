from tweepy_helpers import TwiffleHandler
from db_utils import DBHandler

db_handler = DBHandler()

twiffle_handler = TwiffleHandler(db_handler)
twiffle_handler.run_stream('#BidenHarris', '#BidenHarris2021')
