import twitter_credentials

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

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
        myStream = Stream(self.authenticator, listener)
        myStream.filter(track=filter)


class MyStreamListener(StreamListener):
    """
    Inherits the StreamListener class from tweepy
    """
    def on_data(self, data):
        print(data)

        return True

    def on_error(self, status):
        print(status)

        # 420 is a twitter rate limit warning, end stream if encountered
        if status == 420:
            return False


if __name__ == '__main__':
    filter = ['coronavirus']

    myTwitterStream = TwitterStreamer()
    myTwitterStream.stream_tweets(filter)
