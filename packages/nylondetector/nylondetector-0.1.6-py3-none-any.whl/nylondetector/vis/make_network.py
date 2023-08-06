import numpy as np
import pandas as pd
from pyvis.network import Network


def make_keyword_table(x_test, y_pred, data_hospital, keywords):
    '''
    Concept:
        Predicted value와 병원명이 포함된 keyword based frequency table 생성
        -> based on test dataset and predicted values
    Input:
        - x_test: 기존에 만들어진 X_fin_test
        - y_pred: X_fin_test로 predict한 값
        - data_hospital: siu_data_preprocess.hospital_prsnl_split()으로 분리한 병원 데이터
        - keywords: x_test 내에 들어있는 키워드 컬럼들
    Output:
        - keyword_table: doc_num(기존 글에서의 인덱스), 키워드, y_pred, 유의병원명이 담긴 pd.DataFrame
    '''
    keyword_table = pd.concat([x_test[keywords].reset_index(drop=False).rename(columns={'index': 'doc_num'}),
                             pd.Series(y_pred).rename('y_pred')], axis=1)
    keyword_table = keyword_table.sort_values('doc_num').reset_index(drop=True)

    # add hospital names
    doubt_hospitals = data_hospital['doubtful_hospital_name'][keyword_table['doc_num']].reset_index(drop=False)
    doubt_hospitals = doubt_hospitals.rename(columns={'index': 'doc_num'})

    keyword_table = pd.merge(keyword_table, doubt_hospitals, how='left', on='doc_num')

    return keyword_table


def reshape_keyword_table(keyword_table, keywords):
    '''
    Concept:
        make_keyword_table()의 결과로 얻어진 pd.DataFrame의 형태 변경
    Input:
        - keyword_table: make_keyword_table()의 결과로 얻어진 pd.DataFrame
    Output:
        - keyword_table_re: reshaped table, pd.DataFrame
    '''
    for i, keyword in enumerate(keywords):
        if i == 0:
            keyword_table_re = pd.concat([
                keyword_table['doc_num'],
                keyword_table['doubtful_hospital_name'],
                pd.Series([keyword] * keyword_table.shape[0]).rename('term'),
                keyword_table[keyword].rename('term_cnt'),
                keyword_table['y_pred'].rename('pred_yn')
            ], axis=1)
        else:
            to_add = pd.concat([
                keyword_table['doc_num'],
                keyword_table['doubtful_hospital_name'],
                pd.Series([keyword] * keyword_table.shape[0]).rename('term'),
                keyword_table[keyword].rename('term_cnt'),
                keyword_table['y_pred'].rename('pred_yn')
            ], axis=1)

            keyword_table_re = pd.concat([keyword_table_re, to_add], axis=0)

    # Delete null hospitals first
    keyword_table_re = keyword_table_re.loc[~keyword_table_re['doubtful_hospital_name'].isnull()]
    keyword_table_re = keyword_table_re.sort_values(by=['doubtful_hospital_name', 'term']).reset_index(drop=True)

    return keyword_table_re


def make_keyword_bool_table(keyword_table_re):
    '''
    Concept:
        make_keyword_table()과 reshape_keyword_table()을 거친 테이블의
        term_cnt 컬럼을 bool 값으로 바꾸는 함수
    Input:
        - keyword_table_re: make_keyword_table()과 reshape_keyword_table()을 거친 pd.DataFrame
    Output:
        - kwyrd_bool_table: term_cnt값이 bool로 처리된 pd.DataFrame
    '''
    keyword_bool_table = keyword_table_re.copy()
    keyword_bool_table['term_cnt'] = keyword_bool_table['term_cnt'].map(lambda x: True if x != 0 else False)

    return keyword_bool_table


def top(dataframe, col, n=3):
    '''
    Concept:
        dataframe의 col 기준 top n개를 추출
    '''
    return dataframe.sort_values(by=col, ascending=False)[:n]


def draw_hospital_keyword_network(keyword_table_re, keyword_bool_table, sig_keywords, k):
    '''
    Concept:
        병원과 키워드 노드로 이뤄진 interactive 네트워크를 그려주는 함수 (pyvis 기반)
    Input:
        - keyword_table_re: make_keyword_table()과 reshape_keyword_table()을 거친 pd.DataFrame
        - kwrd_bool_table:
        _ sig_keywords:
        - k: top() 함수 사용 시의 n
    Output:
        None (show network)
    '''
    # Make grouped table for drawing network
    data_network = keyword_table_re.groupby(['doubtful_hospital_name', 'term']).mean()['term_cnt'].reset_index(drop=False)

    # Some heuristic filtering
    data_network = data_network.loc[data_network['doubtful_hospital_name'] != '신안과']
    data_network = data_network.loc[(data_network['term'] != '수술') & (data_network['term'] != '백내장')]

    data_network = data_network.groupby('doubtful_hospital_name') \
        .apply(top, column='term_cnt', n=k).reset_index(drop=True)

    # Aggregate pred_yn value for hospitals
    hospital_yn_sum = keyword_table_re.drop_duplicates(['doc_num']).groupby('doubtful_hospital_name').sum()['pred_yn']

    # Make list for hospital nodes' characteristics
    hospitals = data_network['doubtful_hospital_name']
    hospitals_color = hospitals.map(lambda x: 'darkred' if hospital_yn_sum[x] > 0 else 'darkgreen')
    hospitals_num_docs = keyword_bool_table['doubtful_hospital_name'].value_counts()[1:].apply(np.sqrt).apply(np.sqrt)

    # Make list for keyword nodes' characteristics
    keywords = data_network['term']
    keywords_color = keywords.map(lambda x: 'indianred' if x in sig_keywords else 'darksalmon')

    # Draw network vis
    net = Network("700px", "700px", notebook=True)

    for i, hospital in enumerate(hospitals):
        # Add hospital node
        net.add_node(hospital, hospital,
                     title=hospital,
                     color=hospitals_color[i],
                     size=hospitals_num_docs[hospital] + 6)

        for j, keyword in enumerate(keywords):
            # Add keyword node
            net.add_node(keyword, keyword,
                         title=keyword,
                         color=keywords_color[j],
                         size=10)

            # Add edges
            try:
                width = data_network.loc[(data_network['doubtful_hospital_name'] == hospital)
                                         & (data_network['term'] == keyword), 'term_cnt'].values[0]
                net.add_edge(source=hospital,
                             to=keyword,
                             width=width,
                             length=10,
                             color='gray')

            except IndexError:
                net.add_edge(source=hospital,
                             to=keyword,
                             length=500,
                             color='silver')

    net.repulsion(node_distance=500, spring_length=200)
    net.show("hospital_keyword_network.html")
