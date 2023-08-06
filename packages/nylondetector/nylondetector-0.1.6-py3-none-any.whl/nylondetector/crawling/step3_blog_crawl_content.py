import time

from blog_hospital_crawler import HospitalCrawler

hc = HospitalCrawler()

start = time.time()
keyword_dir_list = ['백내장+부수입',
                    '백내장+소개',
                    '백내장+수당',
                    '백내장+숙소',
                    '백내장+실비',
                    '백내장+실손',
                    '백내장+페이백',
                    '백내장+할인',
                    '백내장+호텔']

for keyword_dir in keyword_dir_list:
    hc.crawl_blog_contents(keyword_dir)
end = time.time() - start

print(f'elapsed = {end}')
