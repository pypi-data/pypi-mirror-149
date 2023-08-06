import re

from podcast_scraper.generic_parser import GenericParser


class FranceCulture(GenericParser):
    def get_urls(self, content):

        album = (
            re.compile(
                r"[\s]*<h1>([\s\S]+?)(?:-[\s\S]+)?[\s]*</h1>", flags=re.MULTILINE
            )
            .findall(content)[0]
            .strip()
        )
        title = re.compile(
            r'<span class="teaser-text-title-wrapper"> *(.+?) *</span>',
            flags=re.MULTILINE,
        ).findall(content)
        url = re.compile(r'data-url="(.+?\.mp3)"', flags=re.MULTILINE).findall(content)
        file = [i.split("/")[-1] for i in url]
        date = re.compile(
            r'<div class="teaser-text-date"><span>LE[\s\S]*?(\d\d/\d\d/\d\d\d\d)</span></div>',
            flags=re.MULTILINE,
        ).findall(content)
        return {
            "album": [album] * len(title),
            "title": title,
            "date": date,
            "file": file,
            "url": url,
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
