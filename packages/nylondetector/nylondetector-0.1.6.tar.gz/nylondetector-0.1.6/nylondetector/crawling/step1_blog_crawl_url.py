import time

from blog_hospital_crawler import HospitalCrawler

keyword_list = ['"백내장"+"부수입"',
                '"백내장"+"소개"',
                '"백내장"+"수당"',
                '"백내장"+"숙소"',
                '"백내장"+"실비"',
                '"백내장"+"실손"',
                '"백내장"+"페이백"',
                '"백내장"+"할인"',
                '"백내장"+"호텔"']

hc = HospitalCrawler()

start = time.time()
for keyword in keyword_list:
    hc.crawl_blog_urls(keyword, 12, 133)  # 133 is heuristic number.
end = time.time() - start

print(f'elapsed = {end}')
