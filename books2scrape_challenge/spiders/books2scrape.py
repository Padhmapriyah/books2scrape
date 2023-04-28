import scrapy

class Books2scrapeSpider(scrapy.Spider):
    name = 'books2scrape'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']
    base_url = 'http://books.toscrape.com/'

    def parse(self, response):
        books = response.xpath('.//article[@class="product_pod"]')
        for book in books:
            full_url = book.xpath('.//h3/a/@href').extract_first()
            if 'catalogue/' not in full_url:
                full_url = 'catalogue/' + full_url

            full_url = self.base_url + full_url

            book_title = book.xpath('.//h3/a/@title').extract_first() # extracting the text value of title and storing it in title

            book_price = book.xpath('.//div/p[@class="price_color"]/text()').extract_first() # extracting the text value of book price and storing it in price

            book_image_url = book.xpath('.//div[@class="image_container"]/a/img/@src').extract_first() # extracting the src value of book image and storing it in image

            full_image_url = self.base_url + book_image_url.replace('../', '') # replacing the ../ in the image src with the base url

            yield {
                'book title': book_title,
                'book price': book_price,
                'book image URL': full_image_url,
                'book details page URL': full_url,
            }
        # Getting the next_page URL and parsing it using the call_back function
        pagination = response.xpath('//li[@class="next"]/a/@href').extract_first()

        # Checking if the next_page is not None, if its none then we are at the last page and we dont need to parse it.
        if pagination is not None:
            yield response.follow(pagination, callback=self.parse)
