# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
import os
from dotenv import load_dotenv
import logging

load_dotenv()

class CoursescraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        url = adapter.get('url')
        # * Check if URL contains Error/Index
        if "Error/Index" in url:
            logging.warning(f"Filtered non-offered courses: {url}")
            return None

        # * Strip leading and trailing whitespaces from strings
        learning_outcomes = adapter.get("learning_outcomes")
        for i in range(len(learning_outcomes)):
            if "NA" in learning_outcomes[i]:
                return None
            learning_outcomes[i] = learning_outcomes[i].strip()
        adapter['learning_outcomes'] = learning_outcomes

        return item
        
class SaveToMySQLPipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host = os.getenv('MYSQL_HOST'),
            user = os.getenv('MYSQL_USER'),
            password = os.getenv('MYSQL_PASSWORD'),
            database = os.getenv('MYSQL_DATABASE')
        )

        self.cur = self.conn.cursor()

    def process_item(self, item , spider):
        adapter = ItemAdapter(item)
        course_code = adapter.get('code')
        course_title = adapter.get('title')
        course_url = adapter.get('url')
        learning_outcomes = '\n'.join(adapter.get('learning_outcomes'))

        self.cur.execute(
            """
                INSERT INTO courses (code, title, url, learning_outcomes)
                VALUES (%s, %s, %s, %s)
            """, (course_code, course_title, course_url, learning_outcomes)
        )

        self.conn.commit()

    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.conn.close()



