# Books2Scrape Challenge
**Summary:**

As per the requirement, this spider is going to scrape first 750 items from books.toscrape.com with a custom item pipeline and export the output to s3 bucket. It will feed the items to these fields give below:

book title

book price

book image URL

book details page URL

### Steps:
We need to create a new scrapy project with the scrapy commands as given below:

```
scrapy startproject books2scrape_challenge
scrapy genspider books2scrape books.toscrape.com
```

You can export scraped data to a JSON or CSV file format, use the below commands:

```
scrapy crawl books -o output.json
```

As per the requirement, we need to stop the items yield at 750 for which I had to create a custom item pipeline which will count the no. of items and as soon as it satisfies to condition i.e. matching ITEMCOUNT to 750, it will start dropping rest of the items.

```
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
```

Also, you need to un-comment the items_pipeline in the settings.py so that the items pipeline which we created to drop items after 750 can be used.

``
ITEM_PIPELINES = {
'books2scrape_challenge.pipelines.Books2ScrapeChallengePipeline': 300,
}
``

You can modify the ITEMCOUNT value to as per your need. For Ex: you can set it to 100 to only get the first 100 items.

```
ITEMCOUNT = 750
```

To Export the Scraped items to the S3, we need to install botocore as per the scrapy docs: https://docs.scrapy.org/en/latest/topics/feed-exports.html#s3.

```
pip install botocore
```

After installation, you have to create an s3 bucket in AWS Console and gather the AWS_ACCESS_KEY and AWS_SECRET_KEY. Add both to the settings.py file.

```
AWS_ACCESS_KEY_ID = "" # REDACTED
AWS_SECRET_ACCESS_KEY = "" # REDACTED
BUCKET = "books2scrape-challenge"
FEEDS = {
    (
        "s3://books2scrape-challenge/%(name)s_750_items_%(time)s.csv"
    ): {
        "format": "json",
        "encoding": "utf8",
    }
}
```

Screenshots for reference:

Starting.

![starting](https://user-images.githubusercontent.com/132034355/235129913-c9c07a29-1144-4f95-9e8c-472769c748fe.png)

Ending.

![finishing](https://user-images.githubusercontent.com/132034355/235130171-98b5584d-4acb-451a-b12e-646773f5fc0d.png)

Exported Data to S3 bucket.

![image](https://user-images.githubusercontent.com/132034355/235129957-220e6572-2595-47aa-95ee-cbdb2148e414.png)
