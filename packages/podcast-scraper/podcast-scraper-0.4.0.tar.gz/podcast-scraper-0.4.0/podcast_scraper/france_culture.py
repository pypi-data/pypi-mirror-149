import re
from html import unescape

from podcast_scraper.generic_parser import GenericParser


class FranceCulture(GenericParser):
    def get_urls(self, content):

        artist = (
            re.compile(
                r"[\s]*<h1>([\s\S]+?)(?:-[\s\S]+)?[\s]*</h1>", flags=re.MULTILINE
            )
            .findall(content)[0]
            .strip()
        )

        urls = []
        titles = []
        albums = []
        dates = []
        pattern = re.compile(
            r'data-url="(.+?\.mp3)"([\s\S]+?)<span class="teaser-text-title-wrapper"> *(.+?) *</span>[\s\S]+?<div class="teaser-text-date"><span>LE[\s\S]*?(\d\d/\d\d/\d\d\d\d)</span></div>',
            flags=re.MULTILINE,
        )
        for (url, between, title, date) in pattern.findall(content):
            pattern_album = re.compile(
                r'<a class="label-sticker" title="(.+)" href=', flags=re.MULTILINE
            )
            album = pattern_album.search(content)
            if album:
                albums.append(unescape(album.group(1)))
            else:
                albums.append(unescape(artist))
            urls.append(url)
            titles.append(unescape(title))
            dates.append(date)

        files = [i.split("/")[-1] for i in urls]

        return {
            "artist": [unescape(artist)] * len(titles),
            "album": albums,
            "title": titles,
            "date": dates,
            "file": files,
            "url": urls,
        }

    def get_next(self, webdriver):
        try:
            next = webdriver.find_element_by_css_selector(
                "#main-content > article > section > div.teasers-list > div.pager-container > ul > li.pager-item.next > a"
            )
            new_url = next.get_attribute("href")
            webdriver.get(new_url)
            return new_url
        except Exception as e:
            return False
