# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EventItem(scrapy.Item):
    name = scrapy.Field()
    description = scrapy.Field()
    image_url = scrapy.Field()
    starts_at = scrapy.Field()
    ends_at = scrapy.Field()
    address = scrapy.Field()
    unique_identifier = scrapy.Field()  # Becomes import_unique_id
    url = scrapy.Field()
