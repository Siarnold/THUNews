from __future__ import absolute_import
import scrapy
import re
import html2text
import datetime
from thuspider.items import ThuSpiderItem

h = html2text.HTML2Text()
h.ignore_emphasis = True
h.ignore_links = True
h.ignore_images = True

class ThuSpider(scrapy.Spider):
    name = "thuspider"
    allowed_domains = ["news.tsinghua.edu.cn"]
    start_urls = ["http://news.tsinghua.edu.cn/publish/thunews/index.html"]

    def parse(self, response):
        for href in response.xpath('//a/@href'):
            url = response.urljoin(href.extract())
            if re.match(
                r"^http://news.tsinghua.edu.cn/publish/thunews/[0-9]{4,5}/"
                "[0-9]{4}/[0-9]+/[0-9]+_.html",
                url
            ):
                yield scrapy.Request(url, callback=self.parse_news)
            else:
                yield scrapy.Request(url, callback=self.parse)

    def parse_news(self, response):
        item = ThuSpiderItem()

        item['news_id'] = response.url.split('/')[-2]
        h1 = response.xpath('//article//h1[1]')
        if h1:
            item['title'] = h.handle(h1[0].extract())
        else:
            h2 = response.xpath('//article//h2[1]')
            if h2:
                item['title'] = h.handle(h2[0].extract())
            else:
                h3 = response.xpath('//article//h3[1]')
                if h3:
                    item['title'] = h.handle(h3[0].extract())
                else:
                    any_tag = response.xpath('//article//*[1]')
                    item['title'] = h.handle(any_tag[0].extract())

        item['title'] = item['title'].strip().strip('#')

        item['url'] = response.url
        item['date'] = datetime.datetime.strptime(
            item['news_id'][:8], '%Y%m%d').date().isoformat() + " 00:00:00.000"
        item['content'] = h.handle(''.join(response.xpath('//article//p')\
                                           .extract())).strip()
        yield item

        self.parse(response)
