# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from zhaopin.items import ZhaopinItem

class TencentSpider(CrawlSpider):
    name = 'tencent'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['http://hr.tencent.com/position.php?']

    rules = (
        Rule(LinkExtractor(allow=r'start=\d+'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//table[@class="tablelist"]//a'), follow=False,callback='parse_item'),

    )

    def parse_item(self, response):
        item=ZhaopinItem()

        item['name']=response.xpath('//table[@class="tablelist textl"]//tr[1]/td/text()').extract()
        if item['name']:
            item['name']=response.xpath('//table[@class="tablelist textl"]//tr[1]/td/text()').extract()[0]
        print item['name']

        item['location']=response.xpath('//table[@class="tablelist textl"]//tr[2]/td[1]/text()').extract()
        if item['location']:
            item['location']=response.xpath('//table[@class="tablelist textl"]//tr[2]/td[1]/text()').extract()[0]

        item['type']=response.xpath('//table[@class="tablelist textl"]//tr[2]/td[2]/text()').extract()
        if item['type']:
            item['type'] = response.xpath('//table[@class="tablelist textl"]//tr[2]/td[2]/text()').extract()[0]

        item['num']=response.xpath('//table[@class="tablelist textl"]//tr[2]/td[3]/text()').extract()
        if item['num']:
            item['num'] = response.xpath('//table[@class="tablelist textl"]//tr[2]/td[3]/text()').extract()[0][:-1]

        item['zhize']=response.xpath('//table[@class="tablelist textl"]//tr[3]//li/text()').extract()
        if item['zhize']:
            item['zhize'] = response.xpath('//table[@class="tablelist textl"]//tr[3]//li/text()').extract()[0]

        item['yaoqiu']=response.xpath('//table[@class="tablelist textl"]//tr[4]//li/text()').extract()
        if item['yaoqiu']:
            item['yaoqiu'] = response.xpath('//table[@class="tablelist textl"]//tr[4]//li/text()').extract()[0]

        item['url']=response.url
        yield item