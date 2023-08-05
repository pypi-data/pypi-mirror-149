import json
import os
import sys
from datetime import datetime, timedelta
from typing import Any, List, Tuple

import tweepy  # type: ignore[import]


class PostSummaryTweet:
    def __init__(
        self,
        keys: Tuple[str, str, str, str],
        source_path: str = "source",
        summary_tweet_log_path: str = "log",
    ):
        self.keys = keys
        self.api = self._get_tweepy_oauth(*self.keys)
        self.source_path = source_path
        self.summary_tweet_log_path = summary_tweet_log_path

    def update_oauth(self, keys: Tuple[str, str, str, str]) -> tweepy.API:
        self.keys = keys
        self.api = self._get_tweepy_oauth(*self.keys)

    def tweet(self, days: int = 7) -> None:
        tweet_log = os.path.join(self.summary_tweet_log_path, "summary_tweet.log")
        os.makedirs(self.summary_tweet_log_path, exist_ok=True)
        open(tweet_log, "a").close()
        week_data_paths = [
            os.path.join(
                self.source_path,
                (datetime.now() - timedelta(days=i)).strftime("%Y/%m/%Y-%m-%d.json"),
            )
            for i in range(days)
        ][::-1]
        for i in week_data_paths:
            if not os.path.isfile(i):
                print("[]", file=open(i, "w"))
        week_book_count = [
            (
                i.split("/")[-1].replace(".json", "", 1),
                len(json.load(open(i, "r"))),
            )
            for i in week_data_paths
        ]

        log = open(tweet_log, "w")
        status, detail = self._tweet(
            self._make_tweet_content(week_book_count), self.api
        )
        if status:
            print(f"[success]{week_book_count[-1][0]}")
            print(week_book_count[-1][0], file=log)
        else:
            print(f"[error]{week_book_count[-1][0]}, {detail}", file=sys.stderr)

        log.close()

    @staticmethod
    def _get_tweepy_oauth(ck: str, cs: str, at: str, as_: str) -> tweepy.API:
        oauth = tweepy.OAuthHandler(ck, cs)
        oauth.set_access_token(at, as_)
        return tweepy.API(oauth)

    def _tweet(self, content: str, api: tweepy.API) -> Tuple[bool, Any]:
        try:
            status = api.update_status(content)
            return (True, status)
        except tweepy.TweepyException as e:
            print(content, file=sys.stderr)
            return (False, e)

    @staticmethod
    def _make_tweet_content(book_count: List[Tuple[str, int]]) -> str:
        contents = [
            "✨今週の新着資料まとめ✨",
        ]
        sum_books = 0
        for day, cnt in book_count:
            contents.append(f"{day}: {cnt} 冊")
            sum_books += cnt
        else:
            contents.append("-" * 12)
            contents.append(f"計: {sum_books} 冊")
            return "\n".join(contents)
