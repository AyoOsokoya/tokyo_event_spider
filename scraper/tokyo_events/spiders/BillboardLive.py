import re

import scrapy
from bs4 import BeautifulSoup

from ..items import EventItem


class BillboardLiveSpider(scrapy.Spider):
    name = "BillboardLive"
    allowed_domains = ["billboard-live.com"]
    # start_urls = ["http://www.billboard-live.com/pg/shop/show/index.php?mode=calendar&shop=1"]
    start_urls = [
        "http://www.billboard-live.com/pg/shop/show/index.php?mode=calendar&date=200708&shop=1"]  # beginning of events

    def parse(self, response):
        all_event_links = response.css("div.lf_btn_detail > ul > li:last-of-type > a::attr('href')").getall()

        for event_link in all_event_links:
            yield response.follow(event_link, callback=self.parse_event_page)

        next_page = response.css('.lf_btn_month ul > li:last-of-type > a::attr(href)').get()

        if next_page is not None:
            next_page_url = next_page
            yield response.follow(next_page_url, callback=self.parse)

    def parse_event_page(self, response):
        # if response.url != 200:
        event_item = EventItem()
        event_item['name'] = response.css('h3.lf_tokyo').get().strip()
        event_item['name'] = BeautifulSoup(event_item['name'], 'lxml').text.strip()
        event_item['name'] = re.sub("\s+", " ", event_item['name'], flags=re.UNICODE)
        event_item['image_url'] = "http://www.billboard-live.com" + response.css(
            '.lf_slider_liveinfo img::attr(src)').get()

        event_item['description'] = response.css('.lf_txtarea > p::text').get().strip()
        # event_item['datetime_string'] = response.css('.lf_openstart > p::text').get()
        event_item['datetime_string'] = response.css('.lf_ttl').get()
        event_item['datetime_string'] = BeautifulSoup(event_item['datetime_string'], 'lxml').text.strip()
        event_item['datetime_string'] = re.sub("\s+", " ", event_item['datetime_string'], flags=re.UNICODE)

        # Example date strings;
        # "2007/9/23（日）",
        # "2007/9/13（木） - 9/16（日）"
        date_match = re.search(r'^(\d+)/(\d+)/(\d+)', event_item['datetime_string'])

        year_start = date_match.group(1)
        month_start = date_match.group(2)
        day_start = date_match.group(3)
        date_start = f"{year_start}-{month_start}-{day_start}"

        if "-" in event_item['datetime_string']:  # Event has a start date and end date
            date_end_match = re.search(r'- (\d+)/(\d+)', event_item['datetime_string'])
            date_end_month = date_end_match.group(1)
            date_end_day = date_end_match.group(2)

            # in theory an event could start this year and next year but it never happens.
            date_end = f"{year_start}-{date_end_month}-{date_end_day} 17:00"
        else:  # Event has a single date to start and end
            date_end = f"{year_start}-{month_start}-{day_start} 17:00"

        event_item['starts_at'] = date_start
        event_item['ends_at'] = date_end
        event_item['unique_identifier'] = response.url
        event_item['url'] = response.url
        yield event_item
