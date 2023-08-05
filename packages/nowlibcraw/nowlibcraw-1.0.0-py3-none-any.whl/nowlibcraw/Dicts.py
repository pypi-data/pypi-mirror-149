from typing import Literal, TypedDict


class BookDetailedInfo(TypedDict):
    link: str
    title: str
    author: str
    publisher: str
    isbn: str
    holding: str
    status: str
    imagesrc: str


class BookData(TypedDict):
    index: int
    data: BookDetailedInfo


class TulipsParams(TypedDict):
    arrivedwithin: int
    type: Literal["book", "article"]
    target: Literal["local", "public"]
    searchmode: Literal["complex", "simple"]
    count: int
    autoDetail: Literal["true", "false"]
