import ast

import numpy as np
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split


def display_results(model_cv, y_test, y_pred):
    '''
    Concept:
        CV 결과를 프린트해주는 함수

    Inputs:
        - model_cv: 구축돼있던 GridSearchCV 혹은 RandomizedSearchCV
        - y_test
        - y_pred

    Outputs:
        confusion matrix 등이 프린트됨

    '''
    pred_labels = np.unique(y_pred)
    confusion_mat = confusion_matrix(y_test, y_pred, labels=pred_labels)

    print(f'-------Labels: {pred_labels}\n')
    print(f'-------Confusion Matrix\n{confusion_mat}\n')
    print(f'---Accuary: {accuracy_score(y_test, y_pred)}')
    print(f'---F1 Score: {f1_score(y_test, y_pred)}')
    print(f'-------Best Parameters\n{model_cv.best_params_}')


class DocumentEmbedding():

    def __init__(self, ngram_names, ngram_ns, how_ngram):
        '''
        Concept:
            - ngram_names: input으로 들어갈 dataframe의 column 중 ngram들에 대한 column name list.
                           1gram에 해당하는 이름부터 오름차순으로 기재
        
            - ngram_ns: 어떠한 ngram들이 존재하는지에 대한 numeric list
                        -> ngram_names에 해당하는 ngram_n이 순서대로 들어가야함
                    
            - how_ngram: 학습 시 TaggedDocument에 들어갈 text의 ngram 구성
                         (ex: '1_2_3'이면 1gram부터 3gram까지 concat)
                         (concat 방법에 대한 건 추후 추가 필요)
        '''
        # make ngram related variables
        if len(ngram_names) != len(ngram_ns):
            print('Ngram arguments are wrong!')
        else:
            self.ngram_names = ngram_names
            self.ngram_ns = ngram_ns

        # make ngram mapping dictionary
        self.ngram_dict = dict()
        for n in ngram_ns:
            self.ngram_dict[n] = ngram_names[n - 1]

        # make ngram composition
        self.how_ngram = how_ngram

    def select_ngram_col(self, ngram_name, ngram_n, dataframe):
        '''
        Concept:
            dataframe 내의 ngram_name에 해당하는 col을 추출

        Inputs:
            - ngram_name: 추출하려는 ngram이 담긴 column name (str)
            - ngram_n: 추출하려는 ngram의 n (int)
            - dataframe: 값이 담긴 pd.DataFrame
            
        Outputs:
            - result: ngram_name에 해당하는 pd.Series
        '''

        # dataframe 내에 있는지부터 확인
        if (ngram_name not in self.ngram_names) or (ngram_n not in self.ngram_ns):
            print("Error: N-gram doesn't exist in this dataframe")
            return

        # col 추출 후 string이면 타입변환
        result = dataframe[ngram_name]
        if type(result[0]) == str:
            result = result.map(lambda x: ast.literal_eval(x))

        return result

    def make_input(self, dataframe):
        '''
        Concept:
            doc2vec에 들어갈 input 생성, 형태는 list

        Inputs:
            - dataframe: text가 있는 dataframe
            
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

    def doc2vec_cv(self, X, y, pipeline, parameters_dict, save_parameters=False):
        '''
        Concept:
            최적의 parameter조합 및 model.seed()를 찾아 모델을 저장하는 함수
             - gensim.sklearn_api의 D2VTransformer 사용 / sklearn의 GridSearchCV 사용
             - 특정 classifier를 통해 파라미터 조합 획득, classifier는 임의로 설정
        
        Inputs:
            - X: list 형태의 document 모음 / ma는 완료된 상태여야함
            - y: list 형태의 각 document label 모음
            - parameters_dict: CV 시 사용할 parameter들의 dictionary. 
                               사용 전에 pipeline.get_params()로 이름 보고 입력!
            - classifier: sklearn에서 사용하는 classifier (xgb.XGBClassifier() 등)
        
        Outputs:
            display_results()를 통해 결과 프린트
        '''

        X_train, X_test, y_train, y_test = train_test_split(X, y)

        model_cv = GridSearchCV(pipeline, parameters_dict)
        model_cv.fit(X_train, y_train)
        y_pred = model_cv.predict(X_test)

        display_results(model_cv, y_test, y_pred)

        if save_parameters is True:
            return model_cv.best_params_
