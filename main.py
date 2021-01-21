import tweepy

import config


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print('---------------------------------------------')
        if hasattr(status, "retweeted_status"):  # Check if Retweet
            try:
                print('A) ' + status.retweeted_status.extended_tweet["full_text"])
            except AttributeError:
                print('B) ' + status.retweeted_status.text)
        else:
            try:
                print('C) ' + status.extended_tweet["full_text"])
            except AttributeError:
                print('D) ' + status.text)

    def on_error(self, status):
        print(status)


auth = tweepy.OAuthHandler(config.API_CONSUMER_KEY, config.API_CONSUMER_SECRET)
auth.set_access_token(config.API_ACCESS_TOKEN, config.API_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, tweet_mode='extended', listener=myStreamListener)

myStream.filter(track=['#bidenharris '])
