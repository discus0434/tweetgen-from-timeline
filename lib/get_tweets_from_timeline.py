from __future__ import annotations

import os
import time
from pathlib import Path

import tweepy


def get_tweets_from_timeline(
    client: tweepy.client,
    *,
    output_dir: str = "./train_texts",
    max_tweets: int = 200,
    oldest_tweet_id: str | int | None = None,
) -> None:

    tweets = []
    n_roop = max_tweets // 200

    for roop_idx in range(n_roop):
        for tweet in tweepy.Paginator(
            client.get_home_timeline,
            max_results=100,
            exclude=["retweets"],
            until_id=oldest_tweet_id,
        ).flatten(limit=200):

            # if tweet includes media or mention, skip it
            if "http" in tweet.text:
                continue
            if tweet.text.startswith("@"):
                continue

            oldest_tweet_id = tweet.id
            tweets.append("<s>" + tweet.text + "</s>")
        print(f"roop {roop_idx} has been finished. wait for {900 // 4} secs...")
        time.sleep(900 // 4)

    tweets = "\n".join(tweets)

    if not os.path.exists(Path(output_dir)):
        os.makedirs(Path(output_dir), exist_ok=True)

    with open(
        Path(output_dir) / "timeline.txt", "w"
    ) as f:
        f.write(tweets)

    with open(
        Path(output_dir) / "timeline_today.txt", "w"
    ) as f:
        f.write(tweets)
