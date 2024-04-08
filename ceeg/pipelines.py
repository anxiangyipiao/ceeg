# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from ceeg.databaseConfig import DB


class CeegPipeline:
    def __init__(self):
        pass

    def open_spider(self, spider):
        self.db = DB() #实例化数据库连接
        # self.db.create_table() #创建表

    def close_spider(self, spider):
        self.db.conn.commit()
        self.db.cursor.close()
        self.db.conn.close()

    def process_item(self, item, spider):

        self.db.InsertData(self.db,item)

        return item


    def create_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS request_info (
                id  int PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255),
                url VARCHAR(255),
                method VARCHAR(255),
                params text,
                xpath text,
            )
        """
        self.db.cursor.execute(sql)
        self.db.conn.commit()
        print("Table created successfully")