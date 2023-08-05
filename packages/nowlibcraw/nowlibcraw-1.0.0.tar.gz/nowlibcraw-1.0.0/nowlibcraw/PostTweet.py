import os
import sys
import time
from io import BytesIO
from typing import Any, List, Optional, Tuple

import requests
import tweepy  # type: ignore[import]

from .Dicts import BookData, BookDetailedInfo


class PostTweet:
    def __init__(self, keys: Tuple[str, str, str, str], tweet_log_path: str = "log"):
        self.keys = keys
        self.api = self._get_tweepy_oauth(*self.keys)
        self.tweet_log_path = tweet_log_path

    def update_oauth(self, keys: Tuple[str, str, str, str]) -> tweepy.API:
        self.keys = keys
        self.api = self._get_tweepy_oauth(*self.keys)

    def tweet(self, data: List[BookData]) -> None:
        tweet_log = os.path.join(self.tweet_log_path, "tweet.log")
        os.makedirs(self.tweet_log_path, exist_ok=True)
        open(tweet_log, "a").close()
        tweeted_links = open(tweet_log, "r").readlines()
        target_data = [
            datam for datam in data if datam["data"]["link"] + "\n" not in tweeted_links
        ]
        log = open(tweet_log, "w")
        for idx, datam in enumerate(target_data):
            print(f'[{idx+1}]{datam["data"]["title"]}')
            tweet_content = self._make_tweet_content(datam["data"])
            tweet_img = self._get_book_image(datam["data"]["imagesrc"])

            if tweet_img is None:
                status, detail = self._tweet(tweet_content, self.api)
            else:
                status, detail = self._tweet(
                    tweet_content, self.api, img_data=tweet_img
                )

            if status:
                print(f'[success]{datam["data"]["link"]}, {detail.id}')
                print(datam["data"]["link"], file=log)
            else:
                print(f'[error]{datam["data"]["link"]}', file=sys.stderr)

            time.sleep(40)
        else:
            log.close()

    @staticmethod
    def _get_tweepy_oauth(ck: str, cs: str, at: str, as_: str) -> tweepy.API:
        oauth = tweepy.OAuthHandler(ck, cs)
        oauth.set_access_token(at, as_)
        return tweepy.API(oauth)

    def _tweet(
        self, content: str, api: tweepy.API, img_data: Optional[bytes] = None
    ) -> Tuple[bool, Any]:
        try:
            if img_data is None:
                status = api.update_status(content)
            else:
                result_img = api.media_upload(
                    filename="img.png", file=BytesIO(img_data)
                )
                status = api.update_status(content, media_ids=[result_img.media_id])
            return (True, status)
        except tweepy.TweepyException as e:
            print(content, file=sys.stderr)
            return (False, e)

    @staticmethod
    def _make_tweet_content(datam_info: BookDetailedInfo) -> str:
        def shorten(text: str, byte_len: int = 40, encoding: str = "utf-8") -> str:
            if len(text.encode(encoding)) <= byte_len:
                return replace_and(text)
            while len(text.encode(encoding)) > byte_len:
                text = text[:-1]
            else:
                return text + "…"

        def replace_and(text: str) -> str:
            return "<no data>" if text == "" else text

        content = "\n".join(
            [
                "✨{date}の新着資料✨",
                "📖: {title}",
                "👤: {author}",
                "🏢: {publisher}",
                "🏛️: {holding}",
                "💬: {link}",
            ]
        )

        return content.format(
            date=time.strftime("%Y-%m-%d"),
            title=shorten(datam_info["title"], 70),
            author=shorten(datam_info["author"], 40),
            publisher=shorten(datam_info["publisher"], 40),
            holding=shorten(datam_info["holding"], 50),
            link=replace_and(datam_info["link"]),
        )

    @staticmethod
    def _get_book_image(datam_imagesrc: str) -> Optional[bytes]:
        if datam_imagesrc == "":
            return None
        else:
            return requests.get(datam_imagesrc).content
