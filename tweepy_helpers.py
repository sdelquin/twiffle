import tweepy
import config


class TwiffleHandler:
    def __init__(self):
        auth = tweepy.OAuthHandler(config.API_CONSUMER_KEY, config.API_CONSUMER_SECRET)
        auth.set_access_token(config.API_ACCESS_TOKEN, config.API_ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth)

        self.listener = TwiffleListener()
        self.stream = tweepy.Stream(
            auth=self.api.auth, tweet_mode='extended', listener=self.listener
        )

    def run_stream(self, *tracking_keywords):
        # filter whole keywords
        track = [f' {k.strip()} ' for k in tracking_keywords]
        self.stream.filter(track=track)


class TwiffleListener(tweepy.StreamListener):
    def current_status_is_retweeted(self):
        return hasattr(self.status, 'retweeted_status')

    def current_status_get_text(self):
        if self.current_status_is_retweeted():
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

    def on_status(self, status):
        self.status = status
        # text = self.current_status_get_text()
        print(self.status.user.screen_name)

    def on_error(self, status):
        print(status)
