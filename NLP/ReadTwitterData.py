import tweepy as tw
import pandas as pd


class ReadTwitterData:

    def __init__(self, key):
        self.consumer_key = key[0]
        self.consumer_secret = key[1]
        self.access_token = key[2]
        self.access_token_secret = key[3]
        self.auth = tw.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tw.API(self.auth, wait_on_rate_limit=True)

    # Get user tweets and respective tweet ids - last 50
    def get_user_timeline(self, count=50):
        user_tweets = []
        tweets = self.api.user_timeline(tweet_mode="extended", count=count)
        for tweet in tweets:
            try:
                user_tweets.append([tweet.retweeted_status.full_text, tweet.user.name, tweet.user.screen_name,
                                    tweet.created_at.strftime("%d-%m-%Y %H:%M:%S")])
            except AttributeError:  # Not a Retweet
                user_tweets.append([tweet.full_text, tweet.user.name, tweet.user.screen_name,
                                    tweet.created_at.strftime("%d-%m-%Y %H:%M:%S")])
        user_tweets.columns = ['text', 'name', 'screen_name', 'created_at']
        user_tweets = pd.DataFrame(user_tweets)
        return user_tweets

    # Get user mentions, user id, tweet ids - last 50
    def get_user_mentions(self, count=50):
        user_mentions = []
        tweets_mentions = self.api.mentions_timeline(tweet_mode="extended", count=count)
        for tweet in tweets_mentions:
            try:
                user_mentions.append([tweet.retweeted_status.full_text, tweet.user.name, tweet.user.screen_name,
                                      tweet.created_at.strftime("%d-%m-%Y %H:%M:%S")])
            except AttributeError:  # Not a Retweet
                user_mentions.append([tweet.full_text, tweet.user.name, tweet.user.screen_name,
                                      tweet.created_at.strftime("%d-%m-%Y %H:%M:%S")])
        user_mentions = pd.DataFrame(user_mentions)
        user_mentions.columns = ['text', 'name', 'screen_name', 'created_at']
        return user_mentions

    def search_tweets(self, count=10, lang='en', q='germany'):
        tweets = []
        raw_tweets = self.api.search_tweets(q=q+' -filter:retweets', lang=lang, tweet_mode="extended", count=count)
        for tweet in raw_tweets:
            try:
                tweets.append([tweet.retweeted_status.full_text, tweet.user.name, tweet.user.screen_name,
                                      tweet.created_at.strftime("%d-%m-%Y %H:%M:%S")])
            except AttributeError:  # Not a Retweet
                tweets.append([tweet.full_text, tweet.user.name, tweet.user.screen_name,
                                      tweet.created_at.strftime("%d-%m-%Y %H:%M:%S")])
        tweets = pd.DataFrame(tweets)
        tweets.columns = ['text', 'name', 'screen_name', 'created_at']
        return tweets

    # Get blocked user list
    def get_blocks(self):
        blocks = []
        for user in self.api.get_blocks():
            blocks.append([user.name, user.screen_name])
        blocks = pd.DataFrame(blocks, columns=['name', 'screen_name'])
        return blocks

    # Get muted user list
    def get_mutes(self):
        mutes = []
        for user in self.api.get_mutes():
            mutes.append([user.name, user.screen_name])
        mutes = pd.DataFrame(mutes, columns=['name', 'screen_name'])
        return mutes

        # Block users
    def block_users(self, users):
        for user in users:
            block = self.api.create_block(screen_name=user)

    # Mute users
    def mute_users(self, users):
        for user in users:
            mute = self.api.create_mute(screen_name=user)

    # Unblock users
    def unblock_users(self, users):
        for user in users:
            destroy_block = self.api.destroy_block(screen_name=user)

    # Unmute users
    def unmute_users(self, users):
        for user in users:
            destroy_block = self.api.destroy_mute(screen_name=user)
