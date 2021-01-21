import tweepy

import config


class TwiffleHandler:
    def __init__(self, db_handler):
        auth = tweepy.OAuthHandler(config.API_CONSUMER_KEY, config.API_CONSUMER_SECRET)
        auth.set_access_token(config.API_ACCESS_TOKEN, config.API_ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)

        self.listener = TwiffleListener(api, db_handler)
        self.stream = tweepy.Stream(
            auth=api.auth, tweet_mode='extended', listener=self.listener
        )

    def run_stream(self, *tracking_keywords):
        # filter whole keywords
        track = [f' {k.strip()} ' for k in tracking_keywords]
        self.stream.filter(track=track)


class TwiffleStatus:
    def __init__(self, status):
        self.status = status

    @property
    def is_retweet(self):
        return hasattr(self.status, 'retweeted_status')

    @property
    def text(self):
        if self.is_retweet:
            try:
                text = self.status.retweeted_status.extended_tweet['full_text']
            except AttributeError:
                text = self.status.retweeted_status.text
        else:
            try:
                text = self.status.extended_tweet["full_text"]
            except AttributeError:
                text = self.status.text
        return text

    @property
    def url(self):
        return f'https://twitter.com/twitter/statuses/{self.status.id}'


class TwiffleListener(tweepy.StreamListener):
    def __init__(self, api, db_handler):
        self.api = api
        self.db_handler = db_handler

    def on_status(self, status):
        print('NEW!')
        ts = TwiffleStatus(status)
        self.db_handler.insert(
            ts.status.id,
            ts.status.user.screen_name,
            ts.text,
            ts.status.created_at,
            ts.url,
            ts.is_retweet,
        )

    def on_error(self, status):
        print(status)
