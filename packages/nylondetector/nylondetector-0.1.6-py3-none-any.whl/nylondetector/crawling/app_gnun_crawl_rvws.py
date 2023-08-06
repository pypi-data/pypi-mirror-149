import os
import requests
import traceback

import pandas as pd
import ujson as json
from datetime import datetime


class AppGnUnCrawler(object):

    def __init__(self):
        # confirm directory
        if not os.path.exists('data/app_gnun'):
            os.makedirs('data/app_gnun')

        # Load common headers
        try:
            with open('hdrs_gnun_hospital_lst.json', 'r') as f_json:
                self.headers_common = json.load(f_json)
        except FileNotFoundError:
            print(traceback.format_exc())

    def get_hospital_lst(self, end=1740):
        """
        앱 내의 병원 리스트를 받아 변수로 저장하는 함수

        :param end: response를 받아올 때 쓰이는 start 변수의 최댓값
        """
        # set header
        headers = self.headers_common
        headers['authorization'] = '67681b7461be441e8594253ccfb77183'
        headers['cookie'] = '_gcl_au=1.1.537414666.1647479003; _ga=GA1.2.1095262571.1647479003; ' \
                            '_gid=GA1.2.1436164380.1647479003; _fbp=fb.1.1647479004225.551549886; ' \
                            'token=5a3188cd12424a03a0a7a2e6fca67a1c; amplitude_id_ee9e97f46fa77da052305bb94e327b88ga' \
                            'ngnamunni.com=eyJkZXZpY2VJZCI6IjYyMmNmY2FiLWRlMGQtNDI1Mi1hNWNiLWZjMDFiZmFlM2I4OFIiLCJ1c' \
                            '2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTY0NzQ5ODIyNzMyOCwibGFzdEV2ZW50VGlt' \
                            'ZSI6MTY0NzQ5ODU3ODk3MywiZXZlbnRJZCI6OTMsImlkZW50aWZ5SWQiOjAsInNlcXVlbmNlTnVtYmVyIjo5M30' \
                            '=; _dd_s=rum=1&id=1d4ed482-3fc4-4e49-99ea-e378d044cda4' \
                            '&created=1647497884756&expire=1647499631869&logs=1'
        headers['referer'] = 'https://www.gangnamunni.com/hospitals'

        # get lists via cURL
        hospital_info_lst = []

        for start in range(20, end, 20):
            params = (
                ('start', str(start)),
                ('country', 'KR'),
                ('sort', 'rating'),
            )

            response = requests.get('https://www.gangnamunni.com/api/hospitals',
                                    headers=headers,
                                    params=params)

            for data in response.json()['data']:
                # make temp dictionary
                hospital_info = dict()

                # get info of each hospital
                for k in ['id', 'name', 'reviewCount']:
                    hospital_info[k] = data[k]

                # append it to list
                hospital_info_lst.append(hospital_info)

        return hospital_info_lst

    def get_hospital_rvws(self, hospital_info_lst: list):
        """
        저장된 병원 리스트의 리뷰들을 받아 json으로 저장하는 함수

        :param hospital_info_lst: 병원들의 정보에 대한 dictionary가 담긴 list
        """
        # set cookie
        cookies = {
            '_gcl_au': '1.1.537414666.1647479003',
            '_ga': 'GA1.2.1095262571.1647479003',
            '_fbp': 'fb.1.1647479004225.551549886',
            'token': '67681b7461be441e8594253ccfb77183',
            '_gid': 'GA1.2.1306802079.1649808609',
            'amplitude_id_ee9e97f46fa77da052305bb94e327b88gangnamunni.com': 'eyJkZXZpY2VJZCI6IjYyMmNmY2FiLWRlMG'
                                                                            'QtNDI1Mi1hNWNiLWZjMDFiZmFlM2I4OFIi'
                                                                            'LCJ1c2VySWQiOm51bGwsIm9wdE91dCI6Zm'
                                                                            'Fsc2UsInNlc3Npb25JZCI6MTY0OTgwODYw'
                                                                            'ODMzOSwibGFzdEV2ZW50VGltZSI6MTY0OT'
                                                                            'gxMDQ5Njc2MiwiZXZlbnRJZCI6MTIxLCJp'
                                                                            'ZGVudGlmeUlkIjowLCJzZXF1ZW5jZU51bW'
                                                                            'JlciI6MTIxfQ==',
            '_dd_s': 'rum=1&id=f546f7f9-5cd2-4927-98a4-2e29112aea5a'
                     '&created=1649808607097&expire=1649811983604&logs=1',
        }
        # set header
        headers = self.headers_common
        headers['authorization'] = '67681b7461be441e8594253ccfb77183'
        headers['review-token'] = 'c3e9a53aa4e9688b3d48292eff9b8433:1b913b8fc62ed954d4f6077c813f07df7a3f8dade5afd75' \
                                  'e7ac053fd1b19a5b2fdd3da5d8f1507eb71022a0414b4b767'

        # set lambda for changing datetime format
        parse_date = lambda x: datetime.fromtimestamp(x / 1000).strftime('%Y.%m.%d. %I:%M:%S')

        # get reviews via cURL
        rslt = []
        for hospital_info in hospital_info_lst:
            headers['referer'] = f"https://www.gangnamunni.com/reviews?hospitalId={hospital_info['id']}"
            params = (
                ('start', '0'),
                ('length', str(hospital_info['reviewCount'])),
                ('hospitalId', str(hospital_info['id']))
            )

            response = requests.get('https://www.gangnamunni.com/api/reviews',
                                    headers=headers,
                                    params=params,
                                    cookies=cookies)

            for data in response.json()['data']:
                rslt_temp = {'rvw_date': parse_date(data['createTime']),
                             'eval_cat': data['evalCategory']['message'],
                             'rvw_content': data['contents'],
                             'hospital_name': data['hospitalInfo']['name']}
                rslt_temp.update(data['amplitudeTreatmentInfo'])

                rslt.append(rslt_temp)

        # save result list as json
        with open('data/app_gnun/hospital_rvws.json', 'w') as f_json:
            json.dump(rslt, f_json)

    def cnt_n_save(self, count_word_list: list):
        """
        json으로 저장된 파일을 인코딩 변환 및 단어 카운트 후 csv로 저장하는 함수(전달용)
        """
        with open('data/app_gnun/hospital_rvws.json', 'r') as f_json:
            rslt = json.load(f_json)

        rslt_df = pd.DataFrame(rslt)

        if len(count_word_list)!=0:
            for count_word in count_word_list:
                rslt_df[count_word] = rslt_df['rvw_content'].map(lambda x: x.count(count_word))

        # save result dataframe as csv
        rslt_df.to_csv('data/app_gnun/hospital_rvws.csv', encoding='utf-8-sig')
