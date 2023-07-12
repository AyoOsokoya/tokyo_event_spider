# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader


class BillboardLiveJapanItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    name_in = MapCompose(str.title)
    # description_in = scrapy.Field()
    # address_in = scrapy.Field()
    # datetime_string_in = scrapy.Field()
    # unique_identifier_in = scrapy.Field() # Becomes import_unique_id
    # url_in = scrapy.Field()

# ItemLoader calls a utility class
