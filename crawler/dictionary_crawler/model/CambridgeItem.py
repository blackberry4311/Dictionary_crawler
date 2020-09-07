from scrapy import Item, Field


class CambridgeItem(Item):
    word = Field()
    definitions = Field()
    crawled_at = Field()
