import itertools
from collections import Counter

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin

from nylondetector.preprocess.text_handling import add_ngrams_to_ma


class KeywordGenerator(BaseEstimator, TransformerMixin):
    def __init__(self, ngram_names, ngram_ns, target_series):
        '''
        Concept:
            - ngram_names: input으로 들어갈 dataframe의 column 중 ngram들에 대한 column name list.
                           1gram에 해당하는 이름부터 오름차순으로 기재
        
            - ngram_ns: 어떠한 ngram들이 존재하는지에 대한 numeric list
                        -> ngram_names에 해당하는 ngram_n이 순서대로 들어가야함
                        
            - target_series: label이 들어있는 pd.Series
        '''
        if len(ngram_names) != len(ngram_ns):
            print('Ngram arguments are wrong!')
        else:
            self.ngram_names = ngram_names
            self.ngram_ns = ngram_ns
        self.max_ngrams = np.max(ngram_ns)
        self.targets = target_series

    def get_doc_term_matrix(self, dataframe, monogram_colname, y_colname):
        '''
        Concept:
            Ngram DataFrame에서 monogram을 추출해 DocumentTermMatrix를 생성

        Inputs:
            - dataframe: content와 ngram들의 값이 담긴 pd.DataFrame
            - monogram_colname: 1gram이 담긴 column의 name
            - y_colname: 분류하려는 target이 담긴 column의 name
            
        Outputs:
            - doc_term_mat: DataFrame 형태의 Document-Term Matrix / binary
        '''
        self.origin_data = dataframe
        self.monogram_colname = monogram_colname
        self.y_colname = y_colname

        monograms_temp = [x for x in dataframe[monogram_colname]]
        monograms_valid = []

        for monograms in monograms_temp:
            monograms_valid += [[word for word in monograms if len(word) > 1]]

        doc_term_mat = pd.DataFrame()
        for monograms_v in monograms_valid:
            doc_term_mat = doc_term_mat.append(pd.Series(Counter(monograms_v)), ignore_index=True)

        self.doc_term_mat = doc_term_mat.fillna(0)
        self.doc_term_mat.index = self.origin_data.index
        self.doc_term_mat[y_colname] = self.targets

        return self.doc_term_mat

    def get_high_y_corr_keywords(self, how_many_words=100):
        '''
        Concept:
            Target label(y)에 대한 Corr이 높은 문서 내 키워드들을 필터링
             - 각 키워드들의 존재유무로 나눈 집단 간 차이에 대한 t-test 진행
             - 이후 Target label과의 corr 계산 및 필터링

        Inputs:
            - how_many_words: 타겟(y)과의 correlation이 높은 키워드 추출 개수
            
        Outputs:
            - keywords_high_cor: Target과의 cor이 높은 단어들의 list
        '''

        # Doing t-test
        score_list = []
        keyword_list = list(set(self.doc_term_mat.columns) - set([self.y_colname]))

        for keyword in keyword_list:
            # 키워드 존재유무에 따라 분류
            yes = self.doc_term_mat[self.doc_term_mat[keyword] > 0]
            non = self.doc_term_mat[self.doc_term_mat[keyword] == 0]

            # t-test 진행을 위한 등분산테스트 진행
            p_1 = stats.levene(yes[self.y_colname], non[self.y_colname]).pvalue

            # 각 키워드들이 yes와 non에 골고루 분포돼있는지에 대한 t-test 진행
            if p_1 < .05:
                p_2 = stats.ttest_ind(yes[self.y_colname], non[self.y_colname], equal_var=False).pvalue
            else:
                p_2 = stats.ttest_ind(yes[self.y_colname], non[self.y_colname], equal_var=True).pvalue

            # t-test 결과에 따라 최종결과에 추가
            if p_2 < .05:
                score_list += [{'keyword': keyword, 'score': p_2}]

        # 결과 정리 후 정렬
        #         print(score_list)
        score_df = pd.DataFrame(score_list).sort_values(by='score')
        keywords_ttest = list(score_df['keyword'])
        self.keywords_ttest = keywords_ttest

        # 타겟(y)과의 correlation이 높은 키워드 추출
        df_corr = self.doc_term_mat.corr().dropna(subset=[self.y_colname])
        keywords_high_cor = list(df_corr.sort_values(by=self.y_colname, ascending=False).index[1:how_many_words + 1])
        self.keywords_high_cor = keywords_high_cor

        return keywords_high_cor

    def make_keyword_based_data(self, given_keywords, combination_num=1):
        '''
        Concept:
            선별된 키워드들의 빈도로 구성된 데이터셋 생성

        Inputs:
            - given_keywords: 추가할 키워드 목록
            - combination_num: 키워드 조합 구성할 숫자
            
        Outputs:
            - keyword_based_df: 원래의 값 + 키워드들의 빈도로 구성된 데이터셋
        '''

        keywords_total = list(set(given_keywords + self.keywords_ttest + self.keywords_high_cor))

        keyword_based_df = self.origin_data[:]

        for keyword in keywords_total:
            keyword_based_df[keyword] = [str(text).count(keyword) for text in self.origin_data[self.monogram_colname]]

        if combination_num > 1:
            for comb_i in range(2, combination_num + 1):
                for a, b in itertools.combinations(keywords_total, comb_i):
                    keyword_based_df[f'{a}+{b}'] = [int((a in str(text)) & (b in str(text))) for text in \
                                                    self.origin_data[self.monogram_colname]]

        self.keyword_based_df = keyword_based_df
        self.keyword_based_df[self.y_colname] = self.targets

        return keyword_based_df

    def get_y_biased_keywords(self):
        '''
        Concept:
            Target label(y)과 관련해 highly biased된 키워드 물색
                (Target label이 존재해야 한다는 한계점 존재)

        Inputs:
            - keyword_based_df: 원래의 값 + 키워드들의 빈도로 구성된 데이터셋
            
        Outputs:
            - keywords_non_biased: Binary target의 한 쪽에만 있는 단어들은 제외한 단어 리스트
        '''
        keyword_based_df_cnt = self.keyword_based_df.groupby([self.y_colname]).sum().T
        keyword_based_df_cnt = keyword_based_df_cnt[list(map(lambda x, y: x != 0 and y != 0,
                                                             keyword_based_df_cnt[0],
                                                             keyword_based_df_cnt[1]))]

        keywords_non_biased = list(keyword_based_df_cnt.index[1:])
        return keywords_non_biased

    def get_high_inter_corr_keywords(self, corr_threshold=.9):
        '''
        Concept:
            키워드들 사이에 highly correlate된 키워드 물색
                (한 쌍의 키워드 중 임의로 한 개 제거)

        Inputs:
            - corr_threshold: highly correlated의 threshold
            
        Outputs:
            - high_corr_pair: [단어, 단어, 상관계수]들로 이뤄진 리스트
            - high_corr: 물색된 단어 리스트 전체
        '''
        keyword_cols = list(self.keyword_based_df.columns)[4:]
        corrs = self.keyword_based_df[keyword_cols].corr()

        high_corr_pair = []
        high_corr = []

        for c1 in keyword_cols:
            for c2 in keyword_cols:
                if (c1 != c2) and (c2 not in high_corr) and (corrs[c1][c2] > corr_threshold):
                    high_corr_pair += [[c1, c2, corrs[c1][c2]]]
                    high_corr.append(c2)

        return high_corr_pair, high_corr

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        '''
            X: 품사 태깅이 된 tuple list 상태의 문서(ex: [('밝', 'VA'), ('안과', 'NNP'), 
                ('수술', 'NNG') ... ])가 담긴 pd.Series
        '''
        x_ngrams_df = add_ngrams_to_ma(X, self.max_ngrams)

        # Document-Term matrix 생성 후 키워드 작업
        doc_term_matrix = self.get_doc_term_matrix(x_ngrams_df, 'content_1gram_1', 'label')

        # keywords_high_cor = self.get_high_y_corr_keywords(how_many_words=100)
        keyword_based_df = self.make_keyword_based_data(given_keywords=[], combination_num=1)

        keywords_non_biased = self.get_y_biased_keywords()
        high_corr_pair, high_corr = self.get_high_inter_corr_keywords(corr_threshold=.9)

        # 최종 컬럼명 설정 및 결과 리턴
        cols_final = list(set(keywords_non_biased) - set(high_corr))
        cols_final.sort()

        df_final = keyword_based_df[cols_final]

        return df_final
