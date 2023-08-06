import fire

from cafe_crawl_srch_content import get_srch_cafe_df


class GetSrchCafeInfo(object):

    def get_df(self, keyword, period_from, period_to, page_max):
        optional_words = ['백내장', '실비', '동물']

        result = get_srch_cafe_df(keyword, period_from, period_to, page_max, optional_words)
        print(result)


if __name__ == '__main__':
    fire.Fire(GetSrchCafeInfo)
