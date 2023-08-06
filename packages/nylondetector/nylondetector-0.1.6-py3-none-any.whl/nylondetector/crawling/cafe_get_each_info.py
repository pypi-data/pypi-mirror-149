import fire
import pandas as pd
import ujson as json

from cafe_crawl_each import EachCafeCrawler


class GetEachCafeInfo(object):

    def run(self, keyword, period_from, period_to, page_max):
        cafe_info = {'fox5282': '12285441',
                     'suddes': '13067396',
                     'juliett00': '11498714',
                     'feko': '10912875'}

        pages = list(range(1, page_max + 1, 1))

        each_cafe_crawl = EachCafeCrawler(keyword, period_from, period_to, pages, cafe_info)
        each_cafe_crawl.crawl_cafe_urls()
        each_cafe_crawl.crawl_cafe_contents()

        # load and save as json format
        content_list = each_cafe_crawl.load_json('contents')

        content_rslt = pd.DataFrame(content_list).explode(['cmt_writer_id', 'cmt_writer_nick', 'cmt_content', 'cmt_date'])
        content_rslt = content_rslt.reset_index(drop=True).to_dict()

        with open(f'data/cafe_each/cafe_result_from_{period_from}_to_{period_to}_{keyword}.json', 'w') as f_json:
            json.dump(content_rslt, f_json)


if __name__ == '__main__':
    fire.Fire(GetEachCafeInfo)
