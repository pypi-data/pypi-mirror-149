import numpy as np

from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin

from nylondetector.preprocess.text_handling import add_ngrams_to_ma


class D2VInputTransformer(BaseEstimator, TransformerMixin):

    def __init__(self, tagger, pos_list, stopwords, ngram_names, ngram_ns, how_ngram):
        '''
        Input:
            - tagger: pos를 태깅할 tagger

            - pos_list: 보려고 하는 품사의 list

            - stopwords: 불용어 리스트

            - ngram_names: input으로 들어갈 dataframe의 column 중 ngram들에 대한 column name list.
                           1gram에 해당하는 이름부터 오름차순으로 기재

            - ngram_ns: 어떠한 ngram들이 존재하는지에 대한 numeric list
                        -> ngram_names에 해당하는 ngram_n이 순서대로 들어가야함

            - how_ngram: 학습 시 TaggedDocument에 들어갈 text의 ngram 구성
                         (ex: '1_2_3'이면 1gram부터 3gram까지 concat)
                         (concat 방법에 대한 건 추후 추가 필요)

        '''
        self.tagger = tagger
        self.pos_list = pos_list
        self.stopwords = stopwords
        if len(ngram_names) != len(ngram_ns):
            print('Ngram arguments are wrong!')
        else:
            self.ngram_names = ngram_names
            self.ngram_ns = ngram_ns

        self.how_ngram = how_ngram
        self.max_ngrams = np.max(ngram_ns)

    def select_ngram_col(self, ngram_name, ngram_n, dataframe):
        '''
        Concept:
            dataframe 내의 ngram_name에 해당하는 col을 추출

        Inputs:
            - ngram_name: 추출하려는 ngram이 담긴 column name (str)
            - ngram_n: 추출하려는 ngram의 n (int)
            - dataframe: content와 ngram들의 값이 담긴 pd.DataFrame

        Outputs:
            - result: ngram_name에 해당하는 pd.Series
        '''

        # dataframe 내에 있는지부터 확인
        if (ngram_name not in self.ngram_names) or (ngram_n not in self.ngram_ns):
            print("Error: N-gram doesn't exist in this dataframe")
            return

        # col 추출 후 string이면 타입변환
        result = dataframe[ngram_name]
        #         if type(result[0])==str:
        #             result = result.map(lambda x: ast.literal_eval(x))

        return result

    def make_input(self, dataframe):
        '''
        Concept:
            doc2vec에 들어갈 input 생성, 형태는 list

        Inputs:
            - dataframe: content와 ngram들의 값이 담긴 pd.DataFrame

        Outputs:
            - input_result: 해당하는 ngram들을 concat시킨 list

        '''
        ngram_values = dict()

        # 각 ngram의 n에 해당하는 값을 매핑해주는 dict 생성
        for n in self.ngram_ns:
            ngram_values[n] = self.select_ngram_col(self.ngram_names[n - 1], n, dataframe)

        # how_ngram 변수에 따른 인풋 생성
        if self.how_ngram == '1':
            input_result = ngram_values[1]
        elif self.how_ngram == '2':
            input_result = ngram_values[2]
        elif self.how_ngram == '3':
            input_result = ngram_values[3]
        elif self.how_ngram == '1_2':
            input_result = ngram_values[1] + ngram_values[2]
        elif self.how_ngram == '1_3':
            input_result = ngram_values[1] + ngram_values[3]
        elif self.how_ngram == '2_3':
            input_result = ngram_values[2] + ngram_values[3]
        elif self.how_ngram == '1_2_3':
            input_result = ngram_values[1] + ngram_values[2] + ngram_values[3]

        # 이게 doc2vec의 최종 input
        self.input_result = input_result.tolist()

        return self.input_result

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        '''
            X: 품사 태깅이 된 tuple list 상태의 문서(ex: [('밝', 'VA'), ('안과', 'NNP'), 
                ('수술', 'NNG') ... ])가 담긴 pd.Series
        '''

        x_ngrams_df = add_ngrams_to_ma(x, self.max_ngrams)
        x_d2v_input = self.make_input(x_ngrams_df)

        return x_d2v_input
