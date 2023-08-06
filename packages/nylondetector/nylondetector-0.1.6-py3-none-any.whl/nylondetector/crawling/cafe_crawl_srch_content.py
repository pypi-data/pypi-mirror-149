import requests
from datetime import datetime

import pandas as pd
import ujson as json


from cafe_crawl_srch_url import SearchedCafeCrawler


def get_srch_cafe_df(keyword, period_from, period_to, page_max, optional_words):
    """
    검색창에서 검색해 수집한 카페 Url에 대한 본문 및 댓글이 담긴 pd.DataFrame을 반환하는 함수

    :param keyword: 검색할 단어, string
    :param period_from: 검색할 기간 시작, 문자처리된 string yyyymmdd
                    (ex: '20210113')
    :param period_to: 검색할 기간 끝, 문자처리된 string yyyymmdd
                    (ex: '20220113')
    :param page_max: int
    :param optional_words: include, includeAll, exclude 순서의 string list
                        (ex: ['백내장', '실비', '동물'])
    """
    pages = list(range(1, page_max + 1, 1))
    crawl_url = SearchedCafeCrawler(keyword, period_from, period_to, pages, optional_words)
    crawl_url.crawl_cafe_urls()
    url_list = crawl_url.load_json_as_list()

    cafe_ids = [x['clubid'] for x in url_list]
    article_ids = [x['articleid'] for x in url_list]

    # Make content and comment list based on cafe_id and article_id
    content_list, cmt_list = crawl_srch_cafe_contents(cafe_ids, article_ids)

    # Filter valid comments for expanding
    cmt_list_valid = [x for x in cmt_list if x['cmt_writer_key'] != 'NA']
    cmt_list_nas = [x for x in cmt_list if x['cmt_writer_key'] == 'NA']

    # Make dataframe for merging
    content_df = pd.DataFrame(content_list)
    cmt_df_valid = pd.DataFrame(cmt_list_valid); cmt_df_nas = pd.DataFrame(cmt_list_nas)

    # Explode list elements and concat
    cmt_df_valid = cmt_df_valid.explode([x for x in cmt_df_valid.columns if x not in ['cafe_id', 'article_id']])
    cmt_df_expnd = pd.concat([cmt_df_nas, cmt_df_valid], axis=0).sort_index()

    # Make final dataframe
    url_df = pd.DataFrame(url_list).drop_duplicates()
    url_df.rename(columns={'clubid': 'cafe_id', 'articleid': 'article_id'}, inplace=True)

    content_total_df = pd.merge(content_df, cmt_df_expnd, how='inner', on=['cafe_id', 'article_id'])
    cafe_info_df = pd.merge(url_df, content_total_df, how='inner', on=['cafe_id', 'article_id'])

    return cafe_info_df


def crawl_srch_cafe_contents(cafe_id_list: list, article_id_list: list):
    """
    검색창에서 검색해 수집한 카페 Url들의 본문 및 댓글을 수집하는 함수

    :param cafe_id_list: 카페의 고유id가 담긴 list, crawling_cafe_urls()의 결과 중 하나
    :param article_id_list: 카페글의 고유id가 담긴 list, crawling_cafe_urls()의 결과 중 하나
    """
    list_len = len(cafe_id_list)

    # Load common headers
    with open('hdrs_srch_cmmn.json', 'r') as f_json:
        headers_common = json.load(f_json)

    # Set headers and params for curl
    headers = headers_common
    headers['sec-ch-ua'] = '"(Not(A:Brand";v="8", "Chromium";v="99", "Google Chrome";v="99"'
    headers['origin'] = 'https://cafe.naver.com'
    params = (
        ('query', ''),
        ('art', 'aW'),
        ('useCafeId', 'true'),
        ('requestFrom', 'A'),
    )

    cafe_content_list = []
    cafe_cmt_list = []
    content_k_v = {'writer_id': 'id', 'writer_nick': 'nick',
                 'content': 'contentHtml', 'content_read_cnt': 'readCount',
                 'content_cmnt_cnt': 'commentCount'}
    cmt_k_v = {'cmt_writer_key': 'memberKey', 'cmt_writer_id': 'id', 'cmt_writer_nick': 'nick',
                'cmt_date': 'updateDate', 'cmt_content': 'content'}

    for i in range(list_len):
        # Set referer value for each cafe_id and article_id
        headers['referer'] = f'https://cafe.naver.com/ca-fe/cafes/' \
                             f'{cafe_id_list[i]}/articles/{article_id_list[i]}?art=aW' \
                             f'&oldPath=%2FArticleRead.nhn%3Farticleid%3D5542733%26art%3DaW%26clubid%3D24000254'

        resp_json = requests.get(f'https://apis.naver.com/cafe-web/cafe-articleapi/v2/'
                                 f'cafes/{cafe_id_list[i]}/articles/{article_id_list[i]}',
                                 headers=headers, params=params).json()

        # Set dictionaries (these will be appended to each list) and set initial values
        cafe_content_dict = dict()
        cafe_content_dict['cafe_id'] = cafe_id_list[i]
        cafe_content_dict['article_id'] = article_id_list[i]

        cafe_cmt_dict = dict()
        cafe_cmt_dict['cafe_id'] = cafe_id_list[i]
        cafe_cmt_dict['article_id'] = article_id_list[i]

        resp_whole = resp_json['result']
        try:
            is_open = resp_whole['errorCode']
        except KeyError:
            is_open = True

        if is_open != '0004':  # if url could be opened without log-in
            # -----Content
            # Extract Features about Content
            resp_content = resp_whole['article']
            resp_content_writer = resp_content['writer']

            # Replace initial content related values
            for k in content_k_v.keys():
                if 'writer' in k:
                    cafe_content_dict[k] = resp_content_writer[content_k_v[k]]
                elif k == 'content':
                    cafe_content_dict[k] = get_string_content(resp_content[content_k_v[k]])
                else:
                    cafe_content_dict[k] = resp_content[content_k_v[k]]

            # -----Comment
            # Extract Features about Comments in Content
            resp_cmt = resp_whole['comments']
            resp_cmt_item = resp_cmt['items']

            if len(resp_cmt_item) != 0:  # if comments exists
                for k in cmt_k_v.keys():
                    if 'writer' in k:
                        cafe_cmt_dict[k] = [x['writer'][cmt_k_v[k]] for x in resp_cmt_item]
                    elif k == 'cmt_date':
                        cafe_cmt_dict[k] = [change_cmt_date(x[cmt_k_v[k]]) for x in resp_cmt_item]
                    else:
                        cafe_cmt_dict[k] = [x[cmt_k_v[k]] for x in resp_cmt_item]
            else:
                for k in cmt_k_v.keys():
                    cafe_cmt_dict[k] = 'NA'

        else:  # if url couldn't be opened without log-in
            # -----Content
            for k in content_k_v.keys():
                cafe_content_dict[k] = 'NA'
            # -----Comment
            for k in cmt_k_v.keys():
                cafe_cmt_dict[k] = 'NA'

        # Append dictionary to final list
        cafe_content_list.append(cafe_content_dict)
        cafe_cmt_list.append(cafe_cmt_dict)

    return cafe_content_list, cafe_cmt_list


def get_string_content(content_html: str):
    """
    list로 분리된 본문 내용을 join해 string으로 반환하는 함수

    :param content_html: 글 내용과 관련된 html이 달린 json response
    """
    content_raw = content_html.split('class="se-text-paragraph')[1:]
    result = ' '.join([prgrph.split('</span></p>')[0].split('>')[-1] for prgrph in content_raw])
    return result


def change_cmt_date(cmt_date: str):
    """
    comment의 작성일자 형식 변경

    :param cmt_date: comment 관련된 curl로 수집된 date, str
    """
    result = datetime.fromtimestamp(cmt_date / 1000).strftime('%Y.%m.%d. %I:%M:%S')
    return result
