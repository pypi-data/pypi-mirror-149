import os
import requests
import traceback
from datetime import datetime
from urllib.parse import quote

import pandas as pd
import ujson as json


class EachCafeCrawler(object):

    def __init__(self, keyword: str, period_from: int, period_to: int, pages: list, cafe_infos: dict):
        """
        :param keyword: 검색할 단어
        :param period_from: 검색할 기간 시작, yyyymmdd
                    (ex: 20210113)
        :param period_to: 검색할 기간 끝, yyyymmdd
                    (ex: 20220113)
        :param pages: 해당하는 페이지들, int list
        :param cafe_infos: {url 내의 카페이름: cafe_id}
                    (ex: {'fox5282': '12285441', 'suddes': '13067396',
                            'juliett00': '11498714', 'feko': '10912875'}
        """
        self.keyword = keyword
        self.prd_from = str(period_from)
        self.prd_to = str(period_to)
        self.pages = pages
        self.cafe_infos = cafe_infos

        # confirm directory
        if not os.path.exists('data/cafe_each'):
            os.makedirs('data/cafe_each')

        # Load common headers
        try:
            with open('hdrs_each_cmmn.json', 'r') as f_json:
                self.headers_common = json.load(f_json)
        except FileNotFoundError:
            print(traceback.format_exc())

    def crawl_cafe_urls(self):
        """
        검색창에서 검색된 카페 Url을 수집해 json으로 저장하는 함수
        """
        keyword_qt_euckr = quote(self.keyword, encoding='euc-kr')

        rslt = []

        # make headers with headers_common
        headers = self.headers_common
        headers['authority'] = 'cafe.naver.com'
        headers['charset'] = 'utf-8'
        headers['content-type'] = 'application/x-www-form-urlencoded; charset=utf-8'
        headers['accept'] = '*/*'
        headers['ses-fetch-site'] = 'same-origin'

        # for each cafe
        for k, v in self.cafe_infos.items():
            headers['referer'] = f'https://cafe.naver.com/{k}'

            # make lambda to parse period in url
            parse_dt = lambda x: '-'.join([x[:4], x[4:6], x[6:]])

            # for each page
            for page in self.pages:
                # get response from target
                response = requests.get(f'https://cafe.naver.com/ArticleSearchList.nhn?'
                                        f'search.clubid={v}'
                                        f'&search.searchBy=0'
                                        f'&search.query={keyword_qt_euckr}'
                                        f'&search.searchdate={parse_dt(self.prd_from)}{parse_dt(self.prd_to)}'
                                        f'&search.page={page}', headers=headers)

                resp_text = response.text
                resp_article = resp_text.split('class="article"')[1:]

                # gathering information for each page
                is_data_exist = resp_text.split('nodata')

                if is_data_exist != 1:
                    # for every articles in each page
                    article_ids = []
                    subjects = []
                    article_dates = []
                    content_read_cnts = []

                    for x in resp_article:
                        article_ids.append(x.split('articleid=')[1].split('&')[0])
                        subject = x.split('</a>')[0].split(';">')[-1].replace('\n', '').strip()
                        subjects.append(subject.replace('<em class="search_word">', '').replace('</em>', ''))
                        article_dates.append(x.split('"td_date">')[-1].split('</td')[0])
                        content_read_cnts.append(x.split('"td_view">')[-1].split('</td')[0])

                    rslt_tmp = {}
                    rslt_tmp['page'] = str(page)
                    rslt_tmp['cafe_id'] = v
                    rslt_tmp['article_id'] = article_ids
                    rslt_tmp['subject'] = subjects
                    rslt_tmp['article_date'] = article_dates
                    rslt_tmp['content_read_cnt'] = content_read_cnts

                    rslt.append(rslt_tmp)

        # save result as json
        save_to = f'data/cafe_each/cafe_urls_from_{self.prd_from}_to_{self.prd_to}_{self.keyword}.json'
        with open(save_to, 'w') as f_json:
            json.dump(rslt, f_json)

    def crawl_cafe_contents(self):
        """
        각 카페 Url 내의 내용을 수집해 json으로 저장하는 함수
        """
        # load url json file
        filename = f'data/cafe_each/cafe_urls_from_{self.prd_from}_to_{self.prd_to}_{self.keyword}.json'
        with open(filename, 'r') as f_json:
            cafe_each_urls = json.load(f_json)

        # expand list variables for convenience
        urls_dict = pd.DataFrame(cafe_each_urls).explode(['article_id', 'subject', 'article_date', 'content_read_cnt'])
        urls_dict = urls_dict.reset_index(drop=True).to_dict()

        # set parameters
        params = (
            ('query', ''),
            ('useCafeId', 'true'),
            ('requestFrom', 'A'),
        )

        keyword_quote_utf8 = quote(self.keyword, encoding='utf-8')
        keyword_quote_utf8_url = keyword_quote_utf8.replace('%', '%25')

        # make lambda to parse period
        parse_cmt_dt = lambda x: datetime.fromtimestamp(x / 1000).strftime('%Y.%m.%d. %I:%M:%S')

        # set result list
        rslt = []

        # make headers with headers_common
        headers = self.headers_common
        headers['authority'] = 'apis.naver.com'
        headers['accept'] = 'application/json, text/plain, */*'
        headers['origin'] = 'https://cafe.naver.com'
        headers['sec-fetch-site'] = 'same-site'
        headers['x-cafe-product'] = 'pc'
        headers['cookie'] = 'NNB=VHEGGEW73VNWC; nid_tct=iNuJb1d12HcojG03; nx_ssl=2; ' \
                            'BMR=s=1645747139611&r=https%3A%2F%2Fm.blog.naver.com' \
                            '%2Fdaseul_k%2F221915044976&r2=https%3A%2F%2Fwww.google.com%2F; ' \
                            'page_uid=hmmmtlprvxZssL5iVKVssssssg4-297695; nid_inf=1949318804; ' \
                            'NID_AUT=7ECcooBLlCFP+4Qp7OhRgJlJOHx+T3pv4SFW5SOzjUY3LDw5DEej2kiVpTPH864k; ' \
                            'NID_JKL=Nc9wZV+m4q9R68U2dsff/xPBlkdXaSEu6rsU/fiam00=; ' \
                            'NID_SES=AAABdGP/1DLXqIXMFu0uOwHnCSZvz0e2PHy+InGp5Ix+Guhfbqc8el10b' \
                            '/EyG9LVScGHAC+e3C+nQRxFxyf1q2qq2z0c39pK5ygm9AyPcT0iTP+2mvFzQVlqmautPHNmz3BZxnn' \
                            'TF1O3aYR7H18/9M9myk5MtPCXAXV5cC90dfe3VxIbCCZHXWCnwXpQduycpRN73lnmJCpiB0CBv+KiaYh' \
                            'MgP094HldTPlCse0dVUbn8ixDNRKwGShcgHiYmu6IcRSZsqWbaysgRrr/ju2cRadh7T0+PwryfEe/zIHk' \
                            'gKhdsrzlsAjFb49zza1l5fDYBUDeW8hzYkhZQJGf3DE+KodPstcnOM14AIpHwMIObVA5SlW2QuIUEleY' \
                            '9zwndxCz1oiSQoBsVN727Jot4UFS2oQhRO1iuXWjfKhDuvKYrOlzxSTfy4pdFUbxcEavozqCtQcDXRjlW' \
                            '/kpybwxmKtDrr+ZVTvMmcgAe4AbLKRr6TrdAHYNPOekacBe8581ioO43Sy09Q=='

        # for each cafe url
        for i in range(len(urls_dict['page'])):
            cafe_id = urls_dict['cafe_id'][i]
            article_id = urls_dict['article_id'][i]

            headers['referer'] = f'https://cafe.naver.com/ca-fe/cafes/{cafe_id}/articles/{article_id}' \
                                 f'?page=1&inCafeSearch=true&searchBy=0&query={keyword_quote_utf8}' \
                                 f'&includeAll=&exclude=&include=&exact=&searchdate=all&media=0&sortBy=date&' \
                                 f'referrerAllArticles=true&oldPath=%2FArticleRead.nhn%3Fclubid%3D{cafe_id}' \
                                 f'%26page%3D1%26inCafeSearch%3Dtrue%26searchBy%3D0%26query%3D{keyword_quote_utf8_url}' \
                                 f'%26includeAll%3D%26exclude%3D%26include%3D%26exact%3D%26searchdate%3Dall%26media' \
                                 f'%3D0%26sortBy%3Ddate%26articleid%3D{article_id}%26referrerAllArticles%3Dtrue'

            # get response from target
            response = requests.get(f'https://apis.naver.com/cafe-web/cafe-articleapi/v2/cafes/{cafe_id}'
                                    f'/articles/{article_id}', headers=headers, params=params)
            resp_json = response.json()['result']

            # set inital value with url file
            rslt_tmp = {}
            for k in urls_dict.keys():
                rslt_tmp[k] = urls_dict[k][i]

            # if there's error related to level in cafe
            try:
                resp_article = resp_json['article']

                # get each values for every articleS
                # if content was deleted; just continue
                try:
                    rslt_tmp['cafe_name'] = resp_json['cafe']['name']
                    rslt_tmp['writer_id'] = resp_article['writer']['id']
                    rslt_tmp['writer_nick'] = resp_article['writer']['nick']
                    content = ' '.join([x.split('</span></p>')[0].split('>')[-1]
                                      for x in resp_article['contentHtml'].split('<!-- } SE-TEXT -->')])
                    rslt_tmp['content'] = content.replace('\n', '')

                except KeyError as e:
                    continue

                # if comments do not exist; just continue
                try:
                    resp_cmts = resp_json['comments']['items']
                    rslt_tmp['cmt_writer_id'] = [x['writer']['id'] for x in resp_cmts]
                    rslt_tmp['cmt_writer_nick'] = [x['writer']['nick'] for x in resp_cmts]
                    rslt_tmp['cmt_content'] = [x['content'] for x in resp_cmts]
                    rslt_tmp['cmt_date'] = [parse_cmt_dt(x['updateDate'])[:11] for x in resp_cmts]

                except KeyError as e:
                    continue

            except KeyError as e:
                continue

            rslt.append(rslt_tmp)

        # save result as json
        save_to = f'data/cafe_each/cafe_contents_from_{self.prd_from}_to_{self.prd_to}_{self.keyword}.json'
        with open(save_to, 'w') as f_json:
            json.dump(rslt, f_json)

    def load_json(self, file='urls'):
        """
        :param file: urls / contents
        """
        filename = f'data/cafe_each/cafe_{file}_from_{self.prd_from}_to_{self.prd_to}_{self.keyword}.json'

        with open(filename, 'r') as f_json:
            result = json.load(f_json)

        return result
