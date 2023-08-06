import requests
import traceback

import ujson as json


class SearchedCafeCrawler(object):

    def __init__(self, keyword: str, period_from: str, period_to: str, pages: list, opt_words: list):
        """
        :param keyword: 검색할 단어
        :param period_from: 검색할 기간 시작, 문자처리된 string yyyymmdd
                        (ex: '20210113')
        :param period_to: 검색할 기간 끝, 문자처리된 string yyyymmdd
                        (ex: '20220113')
        :param pages: 해당하는 페이지들, int list
        :param opt_words: include, includeAll, exclude 순서의 string list
                            (ex: ['백내장', '실비', '동물'])
        """
        self.keyword = keyword
        self.prd_from = period_from
        self.prd_to = period_to
        self.pages = pages
        self.opt_words = opt_words

        # response 중 사용할 json 내의 key 목록 설정
        self.variables = ['subject', 'rawWriteDate', 'clubid', 'clubname',
                          'linkUrl', 'content', 'articleid']

    def crawl_cafe_urls(self):
        """
        검색창에서 검색된 카페 Url을 수집해 json으로 저장하는 함수
        """
        # Load common headers
        try:
            with open('hdrs_srch_cmmn.json', 'r') as f_json:
                headers_common = json.load(f_json)
        except FileNotFoundError:
            print(traceback.format_exc())

        # Set headers for curl
        headers = headers_common
        headers['sec-ch-ua'] = '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"'
        headers['content-type'] = 'application/json;charset=UTF-8'
        headers['origin'] = 'https://section.cafe.naver.com'
        headers['referer'] = 'https://section.cafe.naver.com/ca-fe/home/search/' \
                             'articles?q=%EB%B3%91%EC%9B%90%20%EC%B6%94%EC%B2%9C&od=1&' \
                             'em=1&pr=6&in=%EB%B0%B1%EB%82%B4%EC%9E%A5&ia=%EC%8B%A4%EB%B9%84&ex=%EB%8F%99%EB%AC%BC'

        # Set dictionary for multiple pages
        cafe_urls_dict = {}

        # Gathering information for each page
        for page in self.pages:
            data = {"query": self.keyword,
                    "page": str(page),
                    "sortBy": 1,
                    "exceptMarketArticle": 1,
                    "period": [self.prd_from, self.prd_to],
                    "include": self.opt_words[0],
                    "includeAll": self.opt_words[1],
                    "exclude": self.opt_words[2]}
            data_json = json.dumps(data, ensure_ascii=False)

            response = requests.post('https://apis.naver.com/cafe-home-web/cafe-home/v1/search/articles',
                                     headers=headers,
                                     data=data_json.encode('utf-8'))
            try:
                resp_json = response.json()['message']['result']['searchResultArticle']['searchResult']
                cafe_urls_dict[str(page)] = resp_json

            except:
                print(traceback.format_exc())
                cafe_urls_dict[str(page)] = 'None'

        save_to = f'data/cafe_search/{self.keyword}_from_{self.prd_from}_to_{self.prd_to}.json'
        with open(save_to, 'w') as f_json:
            json.dump(cafe_urls_dict, f_json)

    def load_json_as_list(self):
        """
        json파일을 dictionary list로 변환하며 로드하는 함수
        """
        filename = f'data/cafe_search/{self.keyword}_from_{self.prd_from}_to_{self.prd_to}.json'
        with open(filename, 'r') as f_json:
            cafe_urls_dict = json.load(f_json)

        # url dictionary에 있는 key에 page를 추가하며 결과 list에 concat
        for page in self.pages:
            for i in range(len(cafe_urls_dict[str(page)])): # for every url list in each page
                values = {k: v for k, v in cafe_urls_dict[str(page)][i].items() if k in self.variables}
                values['page'] = str(page)

                # 첫 페이지면 result 생성
                if page == 1 and not i:
                    result = []

                result.append(values)

        return result
