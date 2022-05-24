import numbers
from tkinter.tix import TCL_WINDOW_EVENTS
import tweepy
import time
from config.config import ACCESS_SECRET, ACCESS_TOKEN, API_KEY, API_SECRET, BEARER_TOKEN


def limit_handler(cursor):
    '''
        A method to control Rate Limit from Twitter Api
    '''
    try:
        while True:
            yield cursor.next()
    except tweepy.RateLimitError as rate_limit_exception:
        time.sleep(1000)
    except StopIteration as stop_iteration_exception:
        return


def config_auth():
    auth = tweepy.OAuthHandler(
        consumer_key=API_KEY,
        consumer_secret=API_SECRET
    )
    auth.set_access_token(
        key=ACCESS_TOKEN,
        secret=ACCESS_SECRET
    )
    return auth


def show_public_tweets(api, user_name):
    public_tweets = api.home_timeline()
    print(f"Public Tweets from the {user_name}")
    for tweet in public_tweets:
        print(tweet.text)


def follow_someone(api):
    # generous bot
    print('Followers name:')
    for follower in limit_handler(tweepy.Cursor(api.followers).items()):
        print(follower.name)
        if follower.name == 'someone_else':
            follower.follow()
            print(f'Now following the user {follower.name}')


def like_tweets(api, search_tweet, total_items):
    for tweet in limit_handler(tweepy.Cursor(api.search, search_tweet).items(total_items)):
        try:
            tweet.favorite()
            print(f'You liked that tweet {tweet}')
        except tweepy.TweepError as e:
            print(e.reason)


def retweet_tweets(api, search_tweet, total_items):
    for tweet in limit_handler(tweepy.Cursor(api.search, search_tweet).items(total_items)):
        try:
            tweet.retweet()
            print(f'You retweeted that tweet.\n{tweet}')
        except tweepy.TweepError as e:
            print(e.reason)


def main():
    auth = config_auth()
    api = tweepy.API(auth)
    user = api.me()
    print(f'Username: {user.name}')
    # show_public_tweets(api, user.name)
    # follow_someone(api)

    search_string = 'python'
    numbers_of_tweet = 1
    # like_tweets(api, search_string, numbers_of_tweet)
    retweet_tweets(api, search_string, numbers_of_tweet)


if __name__ == '__main__':
    main()
