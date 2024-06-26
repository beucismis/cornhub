import os
from typing import Iterator
from dataclasses import dataclass

import yt_dlp
import requests_html


PORNHUB_BASE_URL = os.environ.get("PORNHUB_BASE_URL", "https://pornhub.com")
VIDEO_ROUTE = PORNHUB_BASE_URL + "/view_video.php?viewkey={}"

session = requests_html.HTMLSession()
session.cookies.set("accessPH", "1")
session.cookies.set("age_verified", "1")
session.cookies.set("accessAgeDisclaimerPH", "1")
session.cookies.set("accessAgeDisclaimerUK", "1")


@dataclass
class VideoSource:
    title: str
    formats: list


@dataclass
class Uploader:
    name: str


@dataclass
class VideoItem:
    title: str
    viewkey: str
    thumbnail_url: str
    uploader: Uploader


def request(endpoint: str = "/", params: dict = {}):
    return session.get(PORNHUB_BASE_URL + endpoint, params=params)


def get_video(viewkey: str) -> VideoSource:
    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(VIDEO_ROUTE.format(viewkey), download=False)

    formats = [format for format in info["formats"] if "https" in format["protocol"]]
    return VideoSource(info["fulltitle"], formats)


def search_video(self, keywords: str, page: int = 1) -> Iterator[VideoItem]:
    # https://pornhub.com/webmasters/search
    pass


def get_section(section_code: str) -> Iterator[VideoItem]:
    if section_code == "video":
        response = request("/video")
    elif section_code == "recommended":
        response = request("/recommended")
    else:
        response = request("/video", {"o": section_code})

    video_item_list = response.html.find("li.pcVideoListItem")

    for item in video_item_list:
        title = item.find("span.title", first=True).find("a", first=True).text
        uploader_name = (
            item.find("div.usernameWrap", first=True).find("a", first=True).text
        )
        viewkey = item.attrs["data-video-vkey"]
        thumbnail_url = item.find("img", first=True).attrs["src"]

        yield VideoItem(title, viewkey, thumbnail_url, Uploader(uploader_name))
