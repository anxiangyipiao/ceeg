import scrapy
from datetime import datetime
from ceeg.databaseConfig import DB


class ExampleSpider(scrapy.Spider):
    name = "example"
    keywords = "变压器"

    def start_requests(self):

        db = DB()
        datas = db.ReadData(db)
        for req_data in datas:
            url = req_data['url']
            params = req_data['params']
            method = req_data['method']
            xpath_rule = req_data["xpath"]

            yield scrapy.FormRequest(url, callback=self.parse, method=method, formdata=params, meta={'xpath_rule': xpath_rule})
    def parse(self, response):

        xpath_rules = response.meta['xpath_rule']  # 从meta中获取多个XPath规则

        result = response.xpath(xpath_rules[0])

        for item in result:
              title = ' '.join(item.xpath(xpath_rules[1]).getall())
              url = item.xpath(xpath_rules[2]).get()
              time = item.xpath(xpath_rules[3]).get()
              nowtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

              yield {
                  "ctime": nowtime,
                  "url": url,
                  "title": title,
                  "publishTime": time
              }
