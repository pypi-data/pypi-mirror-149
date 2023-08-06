import os
import re
import warnings
import itertools
from datetime import datetime as dt
from datetime import timedelta as tmdt

import numpy as np
import pandas as pd

from nylondetector.util.Logger import Logger
from nylondetector.preprocess.text_handling import flatten
from nylondetector.preprocess.text_handling import text_preproc
from nylondetector.preprocess.text_handling import word_matcher_list

warnings.filterwarnings('ignore')


class SIUDataPreprocess():

    def __init__(self, target_keyword, target_yyyymm, data_directory, text_columns):
        '''
        Inputs:
            - target_keyword: 포함여부를 판단할 str
            - target_yyyymm: 크롤링 기준 yyyymm
            - data_directory: 읽어올 파일들이 담긴 directory. os로 확인
            - text_columns: 텍스트 데이터가 담긴 컬럼명(str)
        '''

        self.target_keyword = target_keyword
        self.target_yyyymm = target_yyyymm
        self.dir = data_directory
        self.text_columns = text_columns

    def load_data_dict(self, return_yn=False):
        '''
        Concept:
            data_directory로부터 target_keyword이 담긴 파일들을 불러와 dictionary형태로 저장하는 함수

        Inputs:
            None

        Outputs:
            - data_dict: 로딩된 크롤링 데이터들이 담겨있는 dictionary형태의 data.
            dictionary의 key는 검색 시 사용한 키워드
        '''
        print('///////////////////////////////////////////////')
        print('////////// Data Loading')
        print('///////////////////////////////////////////////')
        self.data_paths = [f'{self.dir}/{x}' for x in os.listdir(self.dir) if self.target_keyword in x]
        self.data_keys = [x.split('_')[2] for x in self.data_paths if len(x.split('_')) > 2]

        data_dict = dict()

        for i, path in enumerate(self.data_paths):
            i_key = self.data_keys[i]

            data_dict[i_key] = pd.read_csv(path, index_col=0)
            print(f'keyword: {i_key}')
            print(f'path: {path}')
            print(f'shape: {data_dict[i_key].shape}')

            # 컬럼으로 키워드 표시해두기
            data_dict[i_key]['keyword'] = i_key

        # ---- dictionary는 저장해두기
        self.data_dict = data_dict

        print('====== successfully done')
        if return_yn:
            return self.data_dict

    def transform_date(self, return_yn=False):
        '''
        Concept:
            긁어온 date형태 중 '~시간 전'등의 값을 일정한 포맷으로 변환시켜주는 함수

        Inputs:
            None

        Outputs:
            - data_dict: date가 변경된 dictionary 형태의 data
        '''

        print('///////////////////////////////////////////////')
        print('////////// Date column processing')
        print('///////////////////////////////////////////////')

        crawl_date = self.target_yyyymm

        for i, path in enumerate(self.data_paths):
            i_key = self.data_keys[i]

            # 각 추출날짜에 따른 date 작업
            # ------ dt_1: 크롤링된 파일명에 있는 날짜형식 (변경가능)
            # ------ dt_2: 크롤링된 파일 내용에 있는 날짜형식
            trgt_date = self.data_dict[i_key]['date']
            dt_1 = '%Y-%m-%d'
            dt_2 = '%Y.%m.%d.'

            # 파일명에 있는 날짜형식들 변경해 i_dt에 저장
            i_dt = dt.strptime(crawl_date, dt_1)

            # 변경작업 시작
            trgt_date = trgt_date.map(lambda x: crawl_date.replace('-', '.') + '.' if '시간 전' in x else x)
            trgt_date = trgt_date.map(lambda x: x.replace('공식', '').strip())
            trgt_date = trgt_date.map(lambda x: x.replace('어제', dt.strftime((i_dt - tmdt(days=1)), dt_2)))
            trgt_date = trgt_date.map(
                lambda x: dt.strftime((i_dt - tmdt(days=int(x.replace('일 전', '')))), dt_2) if '일 전' in x else x)

            # 다시 저장
            self.data_dict[i_key]['date'] = trgt_date

        print('====== successfully done')
        if return_yn:
            return self.data_dict

    def combine_data_dict(self, return_yn=False):
        '''
        Concept:
            dictionary 형태로 분리돼있는 데이터를 합쳐서 pd.Dataframe 형태로 반환

        Inputs:
            None

        Outputs:
            - data_df: pd.Dataframe 형식의 data

        '''
        print('///////////////////////////////////////////////')
        print('////////// Combining to dataframe')
        print('///////////////////////////////////////////////')
        # ---- 합치기
        data_df = pd.concat([self.data_dict[key] for key in self.data_dict.keys()], axis=0).reset_index(drop=True)
        print(f'Raw table: {data_df.shape}')

        # Drop NAs and duplicates(of contents)
        data_df = data_df.dropna()
        data_df = data_df.drop_duplicates(subset='content')

        # Drop '' contents
        data_df['content'] = data_df['content'].map(lambda x: x.strip())
        data_df = data_df.loc[data_df['content'].map(lambda x: len(x)) != 0]

        print(f'After filtering: {data_df.shape}')

        # ---- text preprocessing
        data_df = text_preproc(data_df, self.text_columns, True)

        self.data_df = data_df

        print('====== successfully done')
        if return_yn:
            return self.data_df

    def extract_hashtags(self, content_col, hospital_re_target, return_yn=False):
        '''
        Concept:
            해시태그에 담긴 내용들 불러와 #s 컬럼에 저장해두는 함수

        Inputs:
            - content_col: 글 이름이 담긴 컬럼명
            - hospital_re_target: 병원이름을 해시태그에서 발라내기 위한 정규식,
            이 경우엔 이 단어로 끝나는 것들 (ex: '.*(안과|병원|의원)$')

        Outputs:
            - data_df: pd.Dataframe 형식의 data

        '''
        print('///////////////////////////////////////////////')
        print('////////// Extracting hashtags')
        print('///////////////////////////////////////////////')
        hash_col = self.data_df[content_col].map(
            lambda x: [word.replace(',', '') for word in x.split() if word[0] == '#'])

        hash_col = hash_col.map(lambda x: [[y for y in z.replace('#', ' #').split(' ')
                                            if bool(re.search(hospital_re_target, y))]
                                           if z.count('#') > 1 else z for z in x])
        hash_col = hash_col.map(lambda x: flatten(x))
        hash_col = hash_col.map(lambda x: [y for y in x if bool(re.search(hospital_re_target, y))])

        # make column in data
        self.data_df['#s'] = hash_col
        print('====== successfully done')
        if return_yn:
            return self.data_df

    def hospital_prsnl_split(self, hospital_words_list, non_word_list):
        '''
        Concept:
            병원이 작성한 것으로 보이는 블로그 글과 개인이 작성한 것으로 보이는 글을 분리하는 함수

        Inputs:
            - hospital_words_list: 병원명의 어미(str)가 담긴 list (ex: ['병원', '의원', '외과'])
            - non_word_list: 제외할 단어(str)가 담긴 list (ex: ['동물'])

        Outputs:
            - data_df: pd.Dataframe 형식의 data

        '''
        print('///////////////////////////////////////////////')
        print('////////// Data seperation; by hospital or not')
        print('///////////////////////////////////////////////')
        self.hospital_words_list = hospital_words_list
        self.non_word_list = non_word_list

        for i, col in enumerate(['name', '#s', 'title']):
            if i == 0:
                # ---- 1st Subsetting; by name
                # -------- hospitals
                data_df_hospital = self.data_df.loc[
                    self.data_df[col].map(lambda x: np.sum([y in x for y in hospital_words_list]) != 0)]
                data_df_hospital = data_df_hospital.loc[
                    data_df_hospital[col].map(lambda x: np.sum([y in x for y in non_word_list]) == 0)]
                # -------- personals
                data_df_prsnl = self.data_df.loc[
                    self.data_df[col].map(lambda x: np.sum([y in x for y in hospital_words_list]) == 0)]

            else:
                # ---- 2nd Subsetting: by hashtags // 3rd Subsetting: by title
                # -------- hospitals
                hospital_temp = data_df_prsnl.loc[
                    data_df_prsnl[col].map(lambda x: np.sum([y in x for y in hospital_words_list]) != 0)]
                data_df_hospital = pd.concat([data_df_hospital, hospital_temp], axis=0)
                # -------- personals
                data_df_prnsl = data_df_prsnl.loc[
                    data_df_prsnl[col].map(lambda x: np.sum([y in x for y in hospital_words_list]) == 0)]

        # ---- cleansing
        for col in ['name', 'title']:
            data_df_hospital[col] = data_df_hospital[col].map(lambda x: x.strip())
            data_df_hospital[col] = data_df_hospital[col].map(lambda x: x.strip())

        # ---- Strip and drop '' contents
        data_df_hospital['content'] = data_df_hospital['content'].map(lambda x: x.strip())
        data_df_hospital = data_df_hospital.loc[data_df_hospital['content'].map(lambda x: len(x)) != 0]

        data_df_prnsl['content'] = data_df_prnsl['content'].map(lambda x: x.strip())
        data_df_prnsl = data_df_prnsl.loc[data_df_prnsl['content'].map(lambda x: len(x)) != 0]

        # ---- Save in self; THESE ARE RESULTS
        self.data_hospital = data_df_hospital.reset_index(drop=True)
        self.data_prsnl = data_df_prnsl.reset_index(drop=True)

        print(f'Original: {self.data_df.shape}')
        print(f'Blog written by hospital: {self.data_hospital.shape}')
        print(f'Blog written by personal: {self.data_prsnl.shape}')
        print('====== successfully done')

        return self.data_hospital, self.data_prsnl

    def extract_hospital_name(self, hospital_re_target):
        '''
        Concept:
            1. name, title, #s에서 hospital_re_target 정규식에 해당하는 병원명 의심 단어들을 찾아옴
            2. 한 번 더 돌면서 정제 후 결과 생성

        Inputs:
            - hospital_re_target: 병원이름을 name, title, #s에서 발라내기 위한 정규식,
            이 경우엔 이 단어가 중간에 있는 것들 (ex: '.*(안과|병원|의원).*')

        Outputs:
            - hospitals_series: 병원 이름이 담긴 pd.Series
        '''
        # 1. name, title, #s로부터 병원의심단어 추출해 pd.Series 만들기
        hospitals_dict = dict()

        for i in range(self.data_hospital.shape[0]):
            hospitals_dict[i] = []  # list로 만들거

            name = self.data_hospital['name'][i]
            if np.sum([x in name for x in self.hospital_words_list]) != 0:
                hospitals_dict[i].append(name)

            title = self.data_hospital['title'][i]
            if np.sum([x in title for x in self.hospital_words_list]) != 0:
                hospitals_dict[i].append(title)

            hashs = self.data_hospital['#s'].map(lambda x: [tag for tag in x
                                                         if np.sum([word in tag
                                                                    for word in self.hospital_words_list]) != 0])[i]
            hospitals_dict[i] += hashs

        hospitals_series = pd.Series(hospitals_dict).map(lambda x: [y.replace('#', '') for y in x])

        # 2. 한 번 더 검토하며 병원이름 추가 & 정제하기
        hospitals_series = hospitals_series.map(lambda x: [y if (bool(re.search(hospital_re_target, y))) else None for y in x])
        hospitals_series = hospitals_series.map(lambda x: list(filter(None.__ne__, x)))
        hospitals_series = hospitals_series.map(lambda x: [[y for y in z.split()
                                                      if re.match(hospital_re_target, y) is not None] for z in x])
        hospitals_series = hospitals_series.map(lambda x: list(itertools.chain.from_iterable(x)))

        return hospitals_series

    def match_doubtful_hospitals(self, hospital_series, doubtful_list, threshold):
        '''
        Concept:
            SIU 제공 유의병원 리스트 중 가장 유사도가 높은 이름을 찾아오는 함수

        Inputs:
            - hospital_series: extract_hospital_name()의 결과. 이걸 기반으로 찾아올거임
            - doubtful_list: SIU 제공 유의병원 리스트
            - threshold: 유사도 임계치

        Outputs:
            - doubtful_hospital_series: 유사도가 가장 높다고 판단된 값들이 담긴 pd.Series
        '''
        doubtful_hospital_series = hospital_series.map(lambda x: word_matcher_list(word_list=x,
                                                                             hospitals=doubtful_list,
                                                                             threshold=threshold,
                                                                             mode=1))

        return doubtful_hospital_series
