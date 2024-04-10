from urllib.parse import quote_plus
import pymysql
from ceeg.settings import MYSQL_CONFIG
import logging
import redis
import json

class DB:
    def __init__(self):

        # 连接数据库
        self.conn = pymysql.connect(**MYSQL_CONFIG)
        self.cursor = self.conn.cursor()
        self.r = redis.Redis(host='localhost', port=6379, db=1)

    def InsertData(self,db,item):

        sql = """
                   INSERT INTO data_info (ctime, url, title, publishTime)
                   VALUES (%s, %s, %s, %s)
               """

        try:
            db.cursor.execute(sql, (
                item['ctime'],
                item['url'],
                item['title'],
                item['publishTime']
            ))

        except Exception as e:
            # 记录错误日志
                logging.error(f"Error while inserting item into database: {e}")


    def ReadData(self,db):
        # 	每条数据需要 url params xpath 并把读取的数据放入data数组返回
        data = []
        sql = "SELECT * FROM url_with_xpath"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()


        for row in result[1:3]:
            # params 里的数据是字符串，需要转换为字典
            row['params'] = eval(row['params'])
            # xpath 里的数据是字符串，需要转换为列表
            row["xpath"] = row["xpath"].split(",")  # 将字符串转换为列表

            if int(row["id"]) >1 and int(row["id"]) < 8:
                data.append(row)

        # 将数据放入redis
        # self.PushDatatoRedis(data)
        return data


    def PushDatatoRedis(self,data):

        # 将数据放入redis
        for row in data:
            request_info_str = json.dumps(row)
            self.r.lpush('example:start_urls', request_info_str)

        # datas = self.ReadDataFromRedis()



    # 从redis中读取数据
    def ReadDataFromRedis(self):

        data = self.r.lrange('example:start_urls', 0, -1)
        return data