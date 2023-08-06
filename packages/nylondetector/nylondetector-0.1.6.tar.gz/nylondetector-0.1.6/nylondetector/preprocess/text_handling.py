import re
import warnings

import numpy as np
import pandas as pd
from difflib import SequenceMatcher

warnings.filterwarnings('ignore')


def text_preproc(df, columns, kor_only=False):
    '''
    Concept:
        품사 Tagging 이전의 텍스트에 대한 전처리
          -> [ㄱ-ㅎ가-힣]의 정규식 처리는 이후에
          -> 그 이전에 컬럼 만들 게 있음!

    Inputs:
     - df: content, title, name을 가진 pd.DataFrame
     - columns: 전처리할 column들의 이름이 담긴 list
     - kor_only
         True: re.compile("[^ㄱ-ㅎ가-힣#]+").sub("", x) 시행
         False: re.compile("[^ㄱ-ㅎ가-힣#]+").sub("", x) 미시행
    
    Outputs:
     - df: 전처리된 pd.DataFrame
    '''
    # 전처리::: 태깅 전
    # 1. 이모지 날리기
    emoji_pattern = re.compile("["
                               u"\U00010000-\U0010FFFF"
                               "]+", flags=re.UNICODE)

    for col in columns:
        df[col] = df[col].map(lambda x: re.sub(emoji_pattern, "", x))

    # 2. 괄호 및 기타 이모티콘 날리기 (^^ 등)
    if kor_only:
        for col in columns:
            df[col] = df[col].map(lambda x: re.compile("[^ㄱ-ㅎ가-힣# ]+").sub("", x))

    # 3. ㅅㅅ등의 초성 변환 (지속 추가)
    for col in columns:
        df[col] = df[col].map(lambda x: x.replace('ㅅㅅ', '삼성'))
        df[col] = df[col].map(lambda x: x.replace('ㅎㅎ', '한화'))

    return df


def do_text_ma(text_series, tagger, pos_list, stopwords, is_morph='n'):
    '''
    Concept:
        text(str)이 담긴 pd.Series에 품사를 태깅해주는 함수

    Inputs:
        - text_series: text가 담긴 pd.Series
        - tagger: pos를 태깅할 tagger
        - pos_list: 보려고 하는 품사의 list
        - stopwords: 불용어
        - is_morph
             'y': 품사까지 넣어서 tuple list로 return
             'n': 품사 제외한 string list로 return
    
    Outputs:
     - text_series_ma: 지정된 tagger를 통해 품사가 태깅된 pd.Series
    '''

    text_series_ma = text_series.map(lambda x: tagger.pos(x))
    text_series_ma = text_series_ma.map(lambda x: [text_ma for text_ma in x
                                                   if (text_ma[1] in pos_list) and (text_ma not in stopwords)])

    return text_series_ma
    if is_morph == 'y':
        return text_series_ma
    else:
        text_series_ma_2 = text_series_ma.map(lambda x: [word for word, pos in x])
        return text_series_ma_2


def make_ngram(word_pos_list, N):
    '''
    ----------------------------------------------------------------------------------------------
                                tagging된 단어를 기반으로 N-gram 생성
    ----------------------------------------------------------------------------------------------
    ===================Inputs
     - word_pos_list: (word, pos) 형태의 원소를 포함한 array
     - N: 이을 단어 개수
    
    ===================Outputs
     - result: N에 따른 N-gram list
    '''

    words = [word for word, pos in word_pos_list]
    result = []
    for i in range(len(words) - N):
        if N == 2:
            result.append('{}_{}'.format(words[i], words[i + 1]))
        elif N == 3:
            result.append('{}_{}_{}'.format(words[i], words[i + 1], words[i + 2]))
        elif N == 4:
            result.append('{}_{}_{}_{}'.format(words[i], words[i + 1], words[i + 2], words[i + 3]))
        elif N == 5:
            result.append('{}_{}_{}_{}_{}'.format(words[i], words[i + 1], words[i + 2], words[i + 3], words[i + 4]))

    return result


def add_ngrams_to_ma(text_series_ma, max_ngrams):
    '''
    ----------------------------------------------------------------------------------------------
                            각 컬럼에 있는 텍스트에 대한 tagging 및 N-gram 생성
    ----------------------------------------------------------------------------------------------
    ===================Inputs
     - text_series_ma: 지정된 tagger를 통해 품사가 태깅된 pd.Series
     - max_ngrams: 추가할 N-gram의 최대 N
         
    ===================Outputs
     - result: contents_ma, content_1gram_1, content_1gram_2, 
               content_2gram 등이 담긴 pd.DataFrame
    '''

    ma_with_ngram_df = pd.DataFrame()
    for i in range(1, max_ngrams + 1):
        if i == 1:
            ma_with_ngram_df['content_{}gram_1'.format(i)] = text_series_ma.map(
                lambda x: [word for word, pos in x if len(word) > 1])
            ma_with_ngram_df['content_{}gram_2'.format(i)] = text_series_ma.map(lambda x: [word for word, pos in x])
        else:
            ma_with_ngram_df['content_{}gram'.format(i)] = text_series_ma.map(lambda x: make_ngram(x, i))

    return ma_with_ngram_df


def wrds_for_cnt(data, name_ngrams):
    '''
    ----------------------------------------------------------------------------------------------
                                        각 N-gram에 대한 count
    ----------------------------------------------------------------------------------------------
    ===================Inputs
     - data: pd.DataFrame. 내용이 담긴 컬럼이름은 content
     - name_ngrams: 각 N-gram이 담긴 컬럼의 이름
    
    ===================Outputs
     - result: 1gram, 2gram등의 key와 그에 대한
               값들이 담겨있는 dictionary
    '''

    ##1. empty dictionary 생성
    result = {}

    ##2. 각 N-gram의 이름에 해당하는 컬럼 요소들 담기
    for i in range(data.shape[0]):
        for j, name in enumerate(name_ngrams):
            if i == 0:
                result['{}gram'.format(j + 1)] = data[name][i]
            else:
                result['{}gram'.format(j + 1)] += data[name][i]

    return result


def flatten(lst):
    '''
    ----------------------------------------------------------------------------------------------
                               이중 list flattening (ex: [[], []] -> [ , ])
    ----------------------------------------------------------------------------------------------
    ===================Inputs
     - lst: 이중 list
     
    ===================Outputs
     - result: flatten된 list
    '''
    result = []
    for item in lst:
        if type(item) == list:
            result += flatten(item)
        else:
            result += [item]
    return result


def word_matcher(string, hospitals, threshold, mode, subject=None):
    '''
    ----------------------------------------------------------------------------------------------
                병원명 체크 시 유의병원과의 유사도 계산
                    -> string단위
                    -> 현재 '코'라는 키워드에 치중돼있음. 추후 generalization 필요
    ----------------------------------------------------------------------------------------------
    ===================Inputs
     - string: 병원명과의 유사여부를 체크할 str
     - hospitals: 유의병원명이 담긴 1d array
     - threshold: 유사도 임계값
     - mode
         ==0: 유의병원목록 중 유사하다고 여겨지는 값의 존재여부를 True/False로 반환.
         ==1: 포함되는 유의병원의 이름을 반환. mode가 1일 땐 인덱싱하지 말고 그냥 결과로 활용
    
    ===================Outputs
     - mode에 따라 boolean 혹은 str
    '''

    ##1. 유의병원명에 붙는 '의원' 제거
    hospitals_uniq = np.unique([y.replace('의원', '').strip() for y in hospitals])

    ##2. subject 종류에 따른 전처리
    if subject == '코':
        replacing = lambda x: x.replace('이비인후과', '_이비').replace('성형외과', '')

    ##3. SequenceMatcher를 통한 유사도 계산
    if subject != None:
        max_match_list = [SequenceMatcher(None, replacing(string), replacing(x)).ratio() for x in hospitals_uniq]
    else:
        max_match_list = [SequenceMatcher(None, string, x).ratio() for x in hospitals_uniq]

    ##4. 최대로 유사한 값의 유사도를 구한 후 최대로 유사한 이름 저장
    max_match_ratio = np.max(max_match_list)
    match_name = hospitals_uniq[max_match_list == np.max(max_match_list)][0]

    ##5. 최대 유사도가 threshold를 넘으면 출력, 이 때 mode에 따라 출력종류 변경
    if max_match_ratio > threshold:
        if mode == 0:
            return True
        elif mode == 1:
            return match_name
    else:
        if mode == 0:
            return False
        elif mode == 1:
            return 'None'


def word_matcher_list(word_list, hospitals, threshold, mode, subject=None):
    '''
    ----------------------------------------------------------------------------------------------
                병원명 체크 시 유의병원과의 유사도 계산
                    -> list 단위
                    -> 지속적인  generalization 필요
    ----------------------------------------------------------------------------------------------
    ===================Inputs
     - word_list: 병원명과의 유사여부를 체크할 list
     - hospitals: 유의병원명이 담긴 1d array
     - threshold: 유사도 임계값
     - mode
         ==0: 유의병원목록 중 유사하다고 여겨지는 값의 존재여부를 True/False로 반환.
         ==1: 포함되는 유의병원의 이름을 반환. mode가 1일 땐 인덱싱하지 말고 그냥 결과로 활용
    
    ===================Outputs
     - mode에 따라 boolean list 혹은 string list
    '''
    list_result = [word_matcher(y, hospitals, 0.77, mode, subject) for y in word_list]
    list_result_filtered = list(filter(lambda y: y != 'None', list_result))

    if mode == 1:
        if len(list_result_filtered) == 0:
            result = None
        else:
            result = list_result_filtered[0]

    elif mode == 0:
        result = [j for j, x in enumerate(list_result_filtered) if x]

    return result
