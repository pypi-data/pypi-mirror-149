import time

from nylondetector.crawling.blog_hospital_crawler import HospitalCrawler

hc = HospitalCrawler()
start = time.time()
hc.deduplicate_url()
end = time.time() - start

print(f'elapsed = {end}')
