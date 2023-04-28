# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings


class Books2ScrapeChallengePipeline:
    item_count = 0
    settings = get_project_settings()

    def process_item(self, item, spider):
        if self.settings['ITEMCOUNT'] != 0 and self.item_count >= self.settings['ITEMCOUNT']:
            raise DropItem(
                "ITEMCOUNT limit has been reached - " + str(self.settings['ITEMCOUNT']))
        else:
            self.item_count += 1
            pass
        return item
