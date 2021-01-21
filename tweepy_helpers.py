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
    @staticmethod
    def _get_tweet(status):
        if hasattr(status, "retweeted_status"):  # Check if Retweet
            retweeted = True
            try:
                text = status.retweeted_status.extended_tweet["full_text"]
            except AttributeError:
                text = status.retweeted_status.text
        else:
            retweeted = False
            try:
                text = status.extended_tweet["full_text"]
            except AttributeError:
                text = status.text
        return text, retweeted

    def on_status(self, status):
        text, retweeted = TwiffleListener._get_tweet(status)
        print(text)

    def on_error(self, status):
        print(status)
