import asyncio
import os
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

import aiohttp
import nest_asyncio
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta
from baram.s3_manager import S3Manager
from baram.kms_manager import KMSManager


class HospitalCrawler(object):

    def __init__(self, is_lambda: bool = False, start_date=datetime.strftime(datetime.today(), "%Y%m%d")):
        """
        :param start_date: 검색 기준일 (최근날짜 기준, ex: 20220401)
                            - 미입력시 실행 당일로 입력
        """
        self.CRAWL_DATA_DIR = 'data/blog'
        self.URL_ORIGINAL_DIR = 'url_original'
        self.URL_DEDUP_DIR = 'url_dedup'
        self.CSV_DELIMETER = '|DELIMITER|'
        self.START_DATE = start_date
        self.is_lambda = is_lambda
        if not self.is_lambda:
            os.makedirs(self.CRAWL_DATA_DIR, exist_ok=True)

        self.sm = S3Manager('sli-dst-security', KMSManager().get_kms_arn('s3-hydra01-kms'))

    def crawl_blog_urls(self, keyword: str, num_months: int, max_page: int = 1):
        """
        :param keyword: 검색창에 입력할 키워드
        :param num_months: 검색 기준일로부터 가져올 개월 수
        :param max_page: 검색 시 나타나는 페이지 중 가져올 페이지 최대값
        """
        print(f'{keyword} start')
        keyword_dir = os.path.join(self.CRAWL_DATA_DIR, self.encode_keyword(keyword), self.URL_ORIGINAL_DIR)
        if not self.is_lambda:
            Path(keyword_dir).mkdir(parents=True, exist_ok=True)

        date_lst = [(datetime.strptime(str(self.START_DATE), '%Y%m%d')
                     - relativedelta(months=i)).strftime('%Y%m%d') for i in range(num_months + 1)]

        for i in range(len(date_lst) - 1):
            date_from = date_lst[i + 1]
            date_to = date_lst[i]

            print(f'From {date_from} to {date_to}')
            try:
                loop = asyncio.get_event_loop()
                loop.run_until_complete(
                    self.fetch_srch_pages(keyword_dir, keyword, date_from, date_to, max_page))
            except RuntimeError:
                nest_asyncio.apply()
                loop.run_until_complete(
                    self.fetch_srch_pages(keyword_dir, keyword, date_from, date_to, max_page))

        print(f'{keyword} end')

    async def fetch_srch_pages(self, keyword_dir, keyword, date_from, date_to, max_page):
        srch_url_lst = [
            f'https://search.naver.com/search.naver?where=blog&query={quote(keyword)}'
            f'&sm=tab_pge&srchby=all&nso=so%3Add%2Cp%3Afrom{date_from}to{date_to}&start={i}'
            for i in range(1, max_page * 30, 30)]
        print(srch_url_lst[0])

        keyword_save = self.encode_keyword(keyword)
        output_filename = os.path.join(keyword_dir, f'blog_urls_{keyword_save}_from{date_from}_to{date_to}.csv')

        text = ''
        async with aiohttp.ClientSession() as session:
            all_page_blog_urls = await asyncio.gather(
                *[self.fetch_srch_page(session, url) for url in srch_url_lst], return_exceptions=True)
            for page_blog_urls in all_page_blog_urls:
                if page_blog_urls:
                    for blog_url in page_blog_urls:
                        if blog_url and isinstance(blog_url, str):
                            text += blog_url

        if not self.is_lambda:
            with open(output_filename, 'w') as f:
                f.write(text)
        else:
            self.sm.put_object(f'nylon-detector/{output_filename}', text)

    async def fetch_srch_page(self, session, url):
        async with session.get(url) as response:
            html = await response.text()
            return self.parse_srch_page(html) if response.status == 200 else None

    def parse_srch_page(self, html):
        blog_urls = []
        sp = BeautifulSoup(html, 'html.parser')
        blog_items = sp.find_all('div', 'total_area')
        for item in blog_items:
            total_s_area = item.find('div', 'total_sub')
            date_text = total_s_area.find('span', 'sub_time sub_txt').text
            blog_name = total_s_area.find('a', 'sub_txt sub_name').text

            a_link = item.find('a', 'api_txt_lines total_tit')
            title, link = a_link.text, a_link['href']

            content = f'{date_text}{self.CSV_DELIMETER}{blog_name}{self.CSV_DELIMETER}{title}{self.CSV_DELIMETER}{link}\n'
            blog_urls.append(content)
        return blog_urls

    def encode_keyword(self, keyword):
        return keyword.replace('"', '')

    def deduplicate_url(self, is_lambda: bool = False):
        if is_lambda:
            keyword_dirs = [x for x in self.sm.list_dir(os.path.join('nylon-detector', self.CRAWL_DATA_DIR) + '/')]
        else:
            keyword_dirs = [x for x in os.listdir(self.CRAWL_DATA_DIR) if 'ipynb' not in x]

        for keyword_dir in keyword_dirs:
            dedup_dir = os.path.join(self.CRAWL_DATA_DIR, keyword_dir, self.URL_DEDUP_DIR)
            if not self.is_lambda:
                Path(dedup_dir).mkdir(parents=True, exist_ok=True)

                for filename in os.listdir(os.path.join(self.CRAWL_DATA_DIR, keyword_dir, self.URL_ORIGINAL_DIR)):
                    if 'ipynb_checkpoints' in filename:
                        continue
                    with open(os.path.join(os.path.join(self.CRAWL_DATA_DIR, keyword_dir, self.URL_ORIGINAL_DIR),
                                           filename)) as fin:
                        with open(os.path.join(dedup_dir, filename), 'w') as fout:
                            for line in set(fin.readlines()):
                                fout.write(line)
            else:
                for keyword_dir in keyword_dirs:
                    keys = self.sm.list_objects(os.path.join(keyword_dir, self.URL_ORIGINAL_DIR) + '/')
                    for k in keys:
                        text = ''
                        for line in set(self.sm.get_object_by_lines(k['Key'])):
                            text += line
                        self.sm.put_object(k['Key'].replace(self.URL_ORIGINAL_DIR, self.URL_DEDUP_DIR), text)
                        print(f"{k['Key'].replace(self.URL_ORIGINAL_DIR, self.URL_DEDUP_DIR)} written.")

    def crawl_blog_contents(self, keyword_dir: str):
        print(f'{keyword_dir} start')
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.fetch_blog_contents(keyword_dir))
        except RuntimeError:
            nest_asyncio.apply()
            loop.run_until_complete(self.fetch_blog_contents(keyword_dir))
        print(f'{keyword_dir} end')

    def parse_content_url(self, line):
        tokens = line.split(self.CSV_DELIMETER)
        if len(tokens) == 4:
            date, writer, title, url = tokens[0], tokens[1], tokens[2], tokens[3]
            # Skip outlink.
            if "blog.naver.com" not in url:
                return
            url = url.replace("?Redirect=Log", "").replace("blog.naver.com/",
                                                           "blog.naver.com/PostView.naver?blogId=").replace(
                '\n', '') + '&redirect=Dlog&widgetTypeCall=true&directAccess=false'
            return (date, writer, title, url)

    async def fetch_blog_contents(self, keyword_dir: str):
        contents_dir = os.path.join(self.CRAWL_DATA_DIR, keyword_dir, 'contents')
        if not self.is_lambda:
            Path(contents_dir).mkdir(parents=True, exist_ok=True)

        contents_url_list = []
        if not self.is_lambda:
            for filename in os.listdir(os.path.join(self.CRAWL_DATA_DIR, keyword_dir, self.URL_DEDUP_DIR)):
                if 'ipynb_checkpoints' in filename:
                    continue
                with open(os.path.join(os.path.join(self.CRAWL_DATA_DIR, keyword_dir, self.URL_DEDUP_DIR),
                                       filename)) as f:
                    for line in set(f.readlines()):
                        content_url = self.parse_content_url(line)
                        if content_url:
                            contents_url_list.append(content_url)
        else:
            for file in self.sm.list_objects(os.path.join('nylon-detector', self.CRAWL_DATA_DIR, keyword_dir,
                                                          self.URL_DEDUP_DIR)):
                for line in self.sm.get_object_by_lines(file['Key']):
                    content_url = self.parse_content_url(line)
                    if content_url:
                        contents_url_list.append(content_url)

        from_date = (datetime.strptime(str(self.START_DATE), '%Y%m%d') - relativedelta(years=1)).strftime('%Y-%m-%d')
        end_date = datetime.strptime(str(self.START_DATE), '%Y%m%d').strftime('%Y-%m-%d')

        output_filename = os.path.join(self.CRAWL_DATA_DIR,
                                       keyword_dir,
                                       'contents',
                                       f'blog_contents_{keyword_dir}_from{from_date}_to{end_date}.csv')

        text = f'date{self.CSV_DELIMETER}' \
               f'name{self.CSV_DELIMETER}' \
               f'title{self.CSV_DELIMETER}' \
               f'url{self.CSV_DELIMETER}' \
               f'keyword{self.CSV_DELIMETER}content\n'
        for i in range(0, len(contents_url_list), 500):
            print(f'process {keyword_dir} from {i} to {i + 500}')
            split_list = contents_url_list[i:i + 500]
            headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/'
                                     '537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
            async with aiohttp.ClientSession(headers=headers) as session:
                all_page_blog_contents = await asyncio.gather(
                    *[self.fetch_blog_content(session, date, writer, title, url, keyword_dir)
                      for date, writer, title, url in split_list], return_exceptions=True)
                for blog_contents in all_page_blog_contents:
                    if blog_contents and isinstance(blog_contents, str):
                        text += blog_contents + "\n"
        if not self.is_lambda:
            with open(output_filename, 'w') as f:
                f.write(text)
        else:
            self.sm.put_object(os.path.join('nylon-detector', output_filename), text)

    async def fetch_blog_content(self, session, date, writer, title, url, keyword_dir):
        async with session.get(url) as response:
            if response.status == 200:
                html = await response.text()
                return self.parse_srch_content(date, writer, title, url, keyword_dir, html)
            else:
                return None

    def remove_html_tags(self, text):
        """Remove html tags from a string"""
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)

    def clean_html(self, raw_html):
        plain_text = re.sub(re.compile('<.*?>'), '', raw_html)
        plain_text = plain_text.replace('\r', '') \
            .replace('\n', '') \
            .replace('​', '') \
            .replace(' ', '') \
            .replace('\t', '')
        return plain_text

    def parse_srch_content(self, date, writer, title, url, keyword_dir, html):
        plain_text = ''.join([self.clean_html(start_token.split('<!-- } SE-TEXT -->')[0])
                              for start_token in html.split('<!-- SE-TEXT { -->')[1:]])
        return f'{date}{self.CSV_DELIMETER}' \
               f'{writer}{self.CSV_DELIMETER}' \
               f'{title}{self.CSV_DELIMETER}' \
               f'{url}{self.CSV_DELIMETER}' \
               f'{keyword_dir}{self.CSV_DELIMETER}' \
               f'{plain_text}'
