# -*- coding: utf-8 -*-
from scrapy import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule

from house_renting.items import HouseRenting58Item


class A58Spider(CrawlSpider):
    name = '58'
    allowed_domains = ['58.com']
    start_urls = ['http://gz.58.com/chuzu']

    rules = (
        Rule(LinkExtractor(allow=(r'/zufang/\?', '/hezu/\?'),
                           restrict_css='div.main > div.content > div.listBox > ul.listUl > li'),
             follow=True),
        Rule(LinkExtractor(allow=(r'/zufang/\d+x\.shtml', '/hezu/\d+x\.shtml')), callback='parse_item'),
    )

    def parse_item(self, response):
        selector = Selector(response=response)
        selector.css('div.main-wrap')

        item_loader = ItemLoader(item=HouseRenting58Item(), selector=selector, response=response)
        item_loader.add_css(field_name='title', css='div.house-title > h1::text')
        item_loader.add_value(field_name='source', value=self.name)
        item_loader.add_css(field_name='author', css='div.house-basic-info div.house-agent-info p.agent-name > a::text')
        item_loader.add_css(field_name='image_urls', css='div.basic-pic-list > ul > li > img::attr(data-src)',
                            re=r'(.*)\?.*')
        item_loader.add_css(field_name='author_link',
                            css='div.house-basic-info div.house-agent-info p.agent-name > a::attr(href)')
        item_loader.add_css(field_name='content', css='ul.introduce-item *::text')
        item_loader.add_value(field_name='source_url', value=response.url)
        item_loader.add_css(field_name='publish_time', css='p.house-update-info::text')
        item_loader.add_css(field_name='price', css='div.house-pay-way *::text')
        item_loader.add_css(field_name='detail', css='div.house-desc-item > ul > li > span::text')

        yield item_loader.load_item()