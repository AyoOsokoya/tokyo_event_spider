import re

import scrapy
from ..items import EventItem
from bs4 import BeautifulSoup


class Metropolis(scrapy.Spider):
    name = "Metropolis"
    allowed_domains = ["gaijinpot.com"]
    start_urls = ["https://metropolisjapan.com/events/"]  # beginning of events
    # Run in sequence
    custom_settings = {
        'CONCURRENT_REQUESTS': 1
    }

    def parse(self, response):
        all_event_links = response.css(".tribe-event-url::attr('href')").getall()
        all_event_links = list(set(all_event_links))  # Remove duplicates
        print(len(all_event_links))

        for event_link in all_event_links:
            yield response.follow(event_link, callback=self.parse_event_page, dont_filter=True)

        next_page_url = response.css(".tribe-events-nav-next > a::attr('href')").get()

        if next_page_url is not None:
            print(next_page_url)
            # All pages are same url with different parameters so dont_filter allows duplicate page crawls
            yield response.follow(next_page_url, callback=self.parse, dont_filter=True)

    def parse_event_page(self, response):
        # if response.url != 200:
        event_item = EventItem()
        event_item['name'] = response.css('.tribe-events-single-event-title::text').get()
        description = ''
        event_item['description'] = response.css('.tribe-events-single-event-description').get()
        event_item['image_url'] = response.css('.tribe-events-event-image img::attr("src")').get()
        event_item['starts_at'] = ''
        event_item['ends_at'] = ''
        event_item['url'] = response.request.url
        event_item['unique_identifier'] = ''
        # event_item['image_url'] = \
        # re.search(r'background-image:url\((.+)\)', response.css(".hero.outdated::attr('style')").get())[1]

        # description = BeautifulSoup(response.css('.content.outdated').get()).text.strip()
        # event_item['description'] = description
        # date_match = re.search(r'^Date: (\w+ \d+, 20\d\d)', description)
        # time_match = re.search(r'^Time: (\d+:\d+) (\w{2}) \(JST\))', description)

        # event_item['starts_at'] = date_start
        # event_item['ends_at'] = date_end
        # event_item['unique_identifier'] = response.url
        # event_item['url'] = response.url
        print(event_item)
        # Meta information
        # print(response.css('.tribe-events-meta-group-details').get())
        # print(response.css('.tribe-events-meta-group-organizer').get())
        # print(response.css('.tribe-events-meta-group-venue').get())
        yield event_item
