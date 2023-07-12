import re

import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Response
from scrapy.selector import Selector

from ..items import EventItem

# Parse only the main page, the rest of the site is a mess. It uses sessions and event urls to the same page.
class BluenoteTokyo(scrapy.Spider):
    name = "BluenoteTokyo"
    allowed_domains = ["reserve.bluenote.co.jp"]
    start_urls = ["https://reserve.bluenote.co.jp/reserve/schedule/"]

    custom_settings = {
        'CONCURRENT_REQUESTS': 1
    }

    def parse(self, response: Response):
        all_schedule_elements = response.css(".scheduleTable > *").getall()

        max_index = len(all_schedule_elements) - 1
        index = 0

        month = response.css('.thisMonth .month::text').get()
        year = response.css('.thisMonth .year::text').get()
        while index <= max_index:
            current_element = Selector(text=all_schedule_elements[index])

            if self.is_event_header(current_element):
                if index < max_index:
                    next_element = Selector(text=all_schedule_elements[index + 1])
                    if not self.is_event_header(next_element):
                        if next_element.css('.today_bg').get():  # Today inserts an extra div
                            index += 1
                            continue
                        if current_element.css('.oldBox').get():  # Skip old events as they have no unique url
                            index += 3
                            continue

                        price_info = next_element
                        details = Selector(text=all_schedule_elements[index + 2])
                        day = current_element.css('.dayBox .day::text').get()

                        event_item = EventItem()
                        event_item['name'] = current_element.css('.title::text').get()
                        event_item['description'] = BeautifulSoup(details.css('.details').get(), 'lxml').text.strip()
                        event_item['description'] = re.sub(r"\s+", " ", event_item['description'], flags=re.UNICODE)

                        event_item['image_url'] = 'https://reserve.bluenote.jp' \
                                                  + current_element.css('.columnImg img::attr("src")').get()

                        # TODO: Only get the first day for now it's good enough
                        event_date = f'{year}-{month}-{day}'
                        # TODO: Parsing the time out is a pain, 17:00 is good enough for now
                        event_item['starts_at'] = f'{event_date} 17:00'
                        event_item['ends_at'] = event_item['starts_at']
                        url = details.css('.btn:nth-child(1) a::attr("href")').get()
                        # Event urls are sometimes duplicated between events so stick the date on
                        event_item['unique_identifier'] = url + '@' + event_date
                        event_item['url'] = url
                        yield event_item

                        index += 3
                        continue

            index += 1

        next_page = response.css(".prevNext .next a::attr('href')").get()

        if next_page is not None:
            print(next_page)
            next_page_url = next_page
            yield response.follow(next_page_url, callback=self.parse)

    @staticmethod
    def is_event_header(response: Selector):
        if response.css('.oldBox, .todayBox, .later'):
            return True
        return False
