import asyncio
import json
import os
from datetime import datetime
from functools import partial
from typing import List, Optional, Tuple

import pyppeteer  # type: ignore[import]
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag

from ._GetNewResource import GetNewResource
from .Dicts import BookData, TulipsParams

BS = partial(BeautifulSoup, features="lxml")
pyppeteer.DEBUG = True


class TulipsGetNewResource(GetNewResource):
    _default_params: TulipsParams = {
        "arrivedwithin": 1,
        "type": "book",
        "target": "local",
        "searchmode": "complex",
        "count": 100,
        "autoDetail": "true",
    }
    _default_user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 "
        "Safari/537.36"
    )

    def __init__(
        self,
        base_url: str = "https://www.tulips.tsukuba.ac.jp",
        params: TulipsParams = _default_params,
        source_path: str = "source",
        user_agent: str = _default_user_agent,
    ) -> None:
        self.base_url = base_url
        self.params = params
        self.source_path = source_path
        self.user_agent = user_agent
        self.page_link = (
            self.base_url
            + "/opac/search?"
            + "&".join(
                [
                    f"{k if k != 'type' else 'type[]'}={v}"
                    for k, v in self.params.items()
                ]
            )
        )

    def get(self, headless: bool = False) -> List[BookData]:
        sources = asyncio.get_event_loop().run_until_complete(self._get_pages(headless))
        book_data = self._extract_json(sources)
        print(f"[get]{len(book_data)} books")
        self._save_data(book_data)
        return book_data

    def set_arrived_within(self, day: int) -> None:
        if "arrivedwithin" in self.params:
            self.params["arrivedwithin"] = day
            self.page_link = (
                self.base_url
                + "/opac/search?"
                + "&".join(
                    [
                        f"{k if k != 'type' else 'type[]'}={v}"
                        for k, v in self.params.items()
                    ]
                )
            )

    def _save_data(self, data: List[BookData]) -> None:
        now = datetime.now()
        save_dir = os.path.join(self.source_path, "%04d" % now.year, "%02d" % now.month)
        save_name = os.path.join(save_dir, now.strftime("%Y-%m-%d.json"))
        os.makedirs(save_dir, exist_ok=True)
        print(json.dumps(data, indent=4), file=open(save_name, "w"))

    async def _get_pages(self, headless: bool) -> List[str]:
        browser = await pyppeteer.launch(headless=headless)
        contents: List[str] = []
        page = await browser.newPage()

        await page.setUserAgent(self.user_agent)
        # await page.setDefaultNavigationTimeout(10 * 1000)
        page_index = 1
        content, has_next = await self._get_page(page, page_index)
        if content is None:
            return contents
        contents.append(content)
        while has_next:
            page_index += 1
            content, has_next = await self._get_page(page, page_index)
            if content is None:
                return contents
            contents.append(content)
        else:
            await browser.close()
            return contents

    async def _get_page(
        self, page: pyppeteer.page.Page, page_index: int
    ) -> Tuple[Optional[str], bool]:
        print(f"[get]{self.page_link}, index = {page_index}")
        if page_index == 1:
            await page.goto(
                self.page_link,
                {"waitUntil": "networkidle0"},
            )
        else:
            await page.evaluate(
                """() => {
                document.getElementById('prevnext2_f').click()
                }"""
            )
        try:
            await page.waitForFunction(
                "document.getElementById('page_input_f').value === '%d'" % page_index
            )
        except pyppeteer.errors.ElementHandleError:
            return None, False

        await asyncio.sleep(10)
        content = str(await page.content())
        next_tag = BS(content).find("td", id="prevnext2_f")
        if isinstance(next_tag, Tag):
            classes = next_tag.get("class", [])
            if type(classes) is list and "active" in classes:
                return content, True
            else:
                return content, False
        else:
            return content, False

    def _extract_json(self, sources: List[str]) -> List[BookData]:
        def get_book_info_text(book: Optional[Tag], class_: str) -> str:
            if book is None:
                return ""
            b = book.find("dl", class_=class_)
            if (
                hasattr(b, "dd")
                and isinstance(b, Tag)
                and hasattr(b.dd, "span")
                and isinstance(b.dd, Tag)
                and isinstance(b.dd.span, Tag)
                and hasattr(b.dd.span, "text")
            ):
                return str(b.dd.span.text)
            else:
                return ""

        res: List[BookData] = []
        for source_idx, source in enumerate(sources):
            b = BS(source)
            books: ResultSet[Tag] = b.select(
                "div.panel.searchCard.l_searchCard.c_search_card.p_search_card"
            )
            default_img = "/bookimage-kango.png"
            for book_idx, book_d in enumerate(books):
                book = book_d.select_one(
                    "div.informationArea.c_information_area.l_informationArea"
                )
                res_i: BookData = {
                    "index": source_idx * self.params["count"] + book_idx,
                    "data": {
                        "link": "",
                        "title": "",
                        "author": "",
                        "publisher": "",
                        "isbn": "",
                        "holding": "",
                        "status": "",
                        "imagesrc": "",
                    },
                }
                h3 = (
                    book.h3.a
                    if hasattr(book, "h3")
                    and isinstance(book, Tag)
                    and hasattr(book.h3, "a")
                    and isinstance(book.h3, Tag)
                    else None
                )
                res_i["data"]["link"] = (
                    "" if h3 is None else self.base_url + str(h3.get("href"))
                )
                res_i["data"]["title"] = "" if h3 is None else h3.text
                res_i["data"]["author"] = get_book_info_text(
                    book, "l_detail_info_au_book"
                )
                res_i["data"]["publisher"] = get_book_info_text(
                    book, "l_detail_info_pu"
                )
                res_i["data"]["isbn"] = get_book_info_text(book, "l_detail_info_sb")
                res_i["data"]["holding"] = get_book_info_text(book, "l_detail_info_hd")
                res_i["data"]["status"] = get_book_info_text(book, "l_detail_info_st")
                img = book_d.select_one("img")
                imgsrc = None if img is None else img.get("src")
                res_i["data"]["imagesrc"] = (
                    imgsrc if type(imgsrc) is str and default_img not in imgsrc else ""
                )
                res.append(res_i)
        else:
            return res
