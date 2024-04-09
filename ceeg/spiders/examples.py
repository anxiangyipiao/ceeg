import scrapy
from datetime import datetime
from ceeg.databaseConfig import DB
import json


class ExampleSpider(scrapy.Spider):
    name = "examples"

    def start_requests(self):

        db = DB()
        datas = db.ReadData(db)
        for req_data in datas:
            url = req_data['url']
            params = req_data['params']
            method = req_data['method']
            xpath_rule = req_data["xpath"]

            yield scrapy.FormRequest(url, callback=self.parse,
                                     method=method, formdata=params,
                                     meta={'xpath_rule': xpath_rule},
                                     headers={'Referer': url})

    def parse(self, response):

        xpath_rules = response.meta['xpath_rule']

        sign = response.text[0]

        if self.is_potential_json(sign):
            # 如果返回的是json数据
            # self.parse_json(response,xpath_rules)
            json_data = response.json()
            datapath = xpath_rules[:len(xpath_rules) - 3]
            result = self.get_data_by_path(json_data, datapath)
            for item in result:
                title = item[xpath_rules[len(datapath)]]
                url = item[xpath_rules[len(datapath) + 1]]
                time = item[xpath_rules[len(datapath) + 2]]
                nowtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                yield {
                    "ctime": nowtime,
                    "url": url,
                    "title": title,
                    "publishTime": time
                }

        else:
            # 如果返回的是html数据
            # self.parse_html(response,xpath_rules)
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

    def is_potential_json(self, mystr):
        mystr = mystr.strip()  # 移除字符串前后的空格
        if mystr.startswith('{') or mystr.startswith('['):
            return True
        return False

    '''def parse_json(self,response,xpath_rules):

        json_data = response.json()

        datapath = xpath_rules[:len(xpath_rules)-3]
        result = self.get_data_by_path(json_data,datapath)
        for item in result:
            title = item[xpath_rules[len(datapath)]]
            url = item[xpath_rules[len(datapath)+1]]
            time = item[xpath_rules[len(datapath)+2]]
            nowtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


            yield {
                "ctime": nowtime,
                "url": url,
                "title": title,
                "publishTime": time
            }'''

    def get_data_by_path(self, data, path_rules):
        """ 递归地按照path_rules指定的路径访问JSON数据。
        :param data: 当前需要访问的JSON数据（字典或列表）。
        :param path_rules: 一个包含访问路径规则的列表。
        :return: 找到的数据，如果路径不存在则返回None。
        """

        if not path_rules:
            return data
        if isinstance(data, dict) and path_rules[0] in data:
            return self.get_data_by_path(data[path_rules[0]], path_rules[1:])
            # path_rules[1:])
        return None

    '''def parse_html(self,response,xpath_rules):
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
            }'''