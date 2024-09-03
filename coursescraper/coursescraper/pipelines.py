# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

class CoursescraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # * Strip leading and trailing whitespaces from strings
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name == 'learning_outcomes':
                learning_outcomes = adapter.get(field_name)
                for i in range(len(learning_outcomes)):
                    learning_outcomes[i] = learning_outcomes[i].strip()
                adapter[field_name] = learning_outcomes
        
class SaveToMySQLPipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host = os.getenv('MYSQL_HOST'),
            user = os.getenv('MYSQL_USER'),
            password = os.getenv('MYSQL_PASSWORD'),
            database = os.getenv('MYSQL_COURSESSDB')
        )

        self.cur = self.conn.cursor()

