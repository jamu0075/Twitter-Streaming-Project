import twitter_credentials

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from tweepy import Cursor
from tweepy import API


# Creates an authenticated OAuthHandler object
def create_authentication():
    auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
    auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)

    return auth


class TwitterStreamer():
    """
    Creates a Stream object and connects to the Twitter API
    """
    def __init__(self):
        #Authenticate the stream
        self.authenticator = create_authentication()

    def stream_tweets(self, filter):
        # Stream listener to recieve all messages
        listener = MyStreamListener()

        # Establish a streaming session with a specified filter
        myStream = Stream(self.authenticator, listener, tweet_mode='extended')
        myStream.filter(track=filter)

class TwitterUser():
    """
    Creates a connection to a specified Twitter account
    """
    def __init__(self, user=None):
        self.authenticator = create_authentication()
        self.twitter_api = API(self.authenticator)

        self.twitter_user = user

    def get_user_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_api.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)

        return tweets

class MyStreamListener(StreamListener):
    """
    Inherits the StreamListener class from tweepy
    """
    # ======================================
    # on_data handles all of the following:
    # replies to statuses
    # deletes
    # events
    # direct messages
    # friends
    # limits, disconnects and warnings
    # ======================================
    # def on_data(self, data):
    #     print(data)
    #
    #     return True

    # ======================================
    # on_status only handles statuses
    # ======================================
    def print_tweet(self, status):
        try:
            print(status._json["extended_tweet"]["full_text"])
            print("=" *50)
        except:
            print(status.text)
            print("=" *50)

    def on_status(self, status):
        # Ignore retweets then try for extended full text attributes, otherwise get standard text
        if hasattr(status, 'retweeted_status'):
            return True
        elif hasattr(status, 'quoted_status'):
            print('QUOTED TWEET')
            self.print_tweet(status)
            return True
        else:
            self.print_tweet(status)
            return True


    def on_error(self, status):
        print(status)

        # 420 is a twitter rate limit warning, end stream if encountered
        if status == 420:
            return False


if __name__ == '__main__':
    filter = ['bicycle', 'bicycles', 'cycling']

    user = 'realDonaldTrump'
    num_user_tweets = 20
    user_tweets = []

    # myTwitterUser = TwitterUser(user)
    # user_tweets = myTwitterUser.get_user_tweets(num_user_tweets)

    # for tweet in user_tweets:
    #     print(tweet.text)

    myTwitterStream = TwitterStreamer()
    myTwitterStream.stream_tweets(filter)
