import scrapy
from datetime import datetime
from ceeg.databaseConfig import DB
from scrapy_redis.spiders import RedisSpider
import  json


class ExampleSpider(RedisSpider):
    name = "example"

    def __init__(self):
        # 连接数据库,读取数据到redis
        db = DB()
        data = db.ReadData(db)
        db.PushDatatoRedis(data)


    # 重写make_request_from_data方法，实现从redis中读取数据并发送POST请求
    def make_request_from_data(self, data):

        decoded_data = data.decode()
        request_info = json.loads(decoded_data)

        url = request_info['url']
        params = request_info['params']
        method = request_info['method']
        xpath_rule = request_info["xpath"]

        return scrapy.FormRequest(url, callback=self.parse, method=method,
                                  formdata=params, meta={'xpath_rule': xpath_rule},
                                  headers={'Referer':url}
                                  )

    def parse(self, response):

        xpath_rules = response.meta['xpath_rule']

        sign = response.text[0]

        if self.is_potential_json(sign):
            # 如果返回的是json数据
            # self.parse_json(response, xpath_rules)
            json_data = response.json()
            datapath = xpath_rules[:len(xpath_rules) - 3]
            result = self.get_data_by_path(json_data, datapath)
            for item in result:
                title = item[xpath_rules[len(datapath)]]
                url = item[xpath_rules[len(datapath) + 1]]
                time = item[xpath_rules[len(datapath) + 2]]
                nowtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                yield {"ctime": nowtime, "url": url, "title": title, "publishTime": time}

        else:
            # 如果返回的是html数据
            # self.parse_html(response, xpath_rules)

            result = response.xpath(xpath_rules[0])
            for item in result:
                title = ''.join(item.xpath(xpath_rules[1]).getall())
                url = item.xpath(xpath_rules[2]).get()
                time = item.xpath(xpath_rules[3]).get()
                nowtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                yield {"ctime": nowtime, "url": url,"title": title,"publishTime": time}
    
    
    def is_potential_json(self,mystr):
        mystr = mystr.strip()  # 移除字符串前后的空格
        if mystr.startswith('{') or mystr.startswith('['):
                return True
        return False



    def get_data_by_path(self,data, path_rules):

        if not path_rules:
            return data
        if isinstance(data, dict) and path_rules[0] in data:
            return self.get_data_by_path(data[path_rules[0]],path_rules[1:])
        return None

    





    def ensure_http_protocol(url, default_protocol='http://'):
        if not url.startswith(('http://', 'https://')):
            url = default_protocol + url
        return url







