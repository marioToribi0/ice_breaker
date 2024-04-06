import logging
import os
from datetime import datetime, timezone
import tweepy
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("twitter")

auth = tweepy.OAuthHandler(
    os.environ["TWITTER_API_KEY"], os.environ["TWITTER_API_SECRET"]
)
auth.set_access_token(
    os.environ["TWITTER_ACCESS_TOKEN"], os.environ["TWITTER_ACCESS_SECRET"]
)
api = tweepy.API(auth)


def scrape_user_tweets(username: str, num_tweets: int = 5):
    """Scrapes a Twitter user's original tweets (i.e., not retweets or replies) and returns them as a list of dictionaries.
    Each dictionary has three fields: "time_posted" (relative to now), "text", and "url"

    Args:
        username (str): username from the user to search
        num_tweets (int, optional): quantity of tweets to search. Defaults to 5.
    """
    tweets = api.user_timeline(screen_name=username, count=num_tweets)

    tweet_list = []

    for tweet in tweets:
        if "RT @" not in tweet.text and not tweet.text.startswith("@"):
            tweet_dict = {}
            tweet_dict["time_posted"] = str(
                datetime.now(timezone.utc) - tweet.create_at
            )
            tweet_dict["text"] = tweet.text
            tweet_dict["url"] = (
                f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"
            )
            tweet_list.append(tweet_dict)

    return tweet_list


if __name__ == "__main__":
    print(api)
    print(scrape_user_tweets("dev_manishshah", 5))
