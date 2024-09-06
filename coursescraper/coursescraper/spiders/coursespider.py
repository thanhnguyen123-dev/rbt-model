import scrapy
from coursescraper.items import CourseItem
import logging

class CoursespiderSpider(scrapy.Spider):
    name = "coursespider"
    start_urls = ["https://comp.anu.edu.au/study/courses/"]

    # * Parse the main school of computing course website
    def parse(self, response):
        courses = response.css("tbody tr")
        for course in courses:
            course_url = course.css('td a').attrib['href']
            yield scrapy.Request(course_url, callback=self.parse_course_page)


    # * Parse each course
    def parse_course_page(self, response):
        # if response.status == 404:
        #     logging.warning(f"Filtered non-offered courses: {response.url}")
        #     return
        course_item = CourseItem()
        course_item['url'] = response.url
        course_item['title'] = response.css('span.intro__degree-title__component ::text').get()
        course_item['code'] = response.css('span.molecule__label a ::text').get()
        course_item['learning_outcomes'] = response.css('h2#learning-outcomes + p + ol li ::text').getall() # stored as an array

        # TODO: course_item['prerequisites']
        yield course_item
        






