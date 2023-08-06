import os

import pandas as pd

from baram.s3_manager import S3Manager
from baram.kms_manager import KMSManager

from nylondetector.preprocess.expand_files import expand_files
from nylondetector.preprocess.siu_data_preproc import SIUDataPreprocess

doubtful_hospital_list = pd.read_csv(os.path.join('nylondetector', 'preprocess', 'hospital_list.csv'), delimiter='\t')

# ==================
# Download files from s3 to current directory

print(f'Download files to current directory ({os.getcwd()})')
s3_mng = S3Manager('sli-dst-security', KMSManager().get_kms_arn('s3-hydra01-kms'))

dir_list = s3_mng.list_dir(prefix='nylon-detector/crawl_data/')
dir_list = [f'{dir_keyword}contents/' for dir_keyword in dir_list]

file_path = [s3_mng.list_dir(prefix=x)[0] for x in dir_list]
data_dir = os.path.join('nylondetector', 'preprocess', 'data')
down_dest = [f"{data_dir}/{path.split('/')[-1]}" for path in file_path]

# Do this task when there's no file in data directory
# (temporary remedy)
if len(os.listdir(data_dir)) != 0:
    try:
        for i in range(len(file_path)):
            s3_mng.download_file(file_path[i], down_dest[i])
        print(f'{len(file_path)} files downloaded succesfully')
    except:
        print('Something went wrong while downloading')

    # ==================
    # Expand files
    try:
        for i in range(len(down_dest)):
            expand_files(down_dest[i])
        print(f'{len(file_path)} files downloaded succesfully')
    except:
        print('Something went wrong while expanding')

else:
    print('Files are already in directory')

# ==================
# Preprocessing

# tgt_keyword = sys.argv[1]
# tgt_yyyymm = sys.argv[2]
# data_dir = sys.argv[3]

tgt_keyword = 'expanded'
tgt_yyyymm = '2021-11-21'

# if len(sys.argv)!=4:
#     print('Insufficient arguments')

preprocessor = SIUDataPreprocess(target_keyword=tgt_keyword,
                                 target_yyyymm=tgt_yyyymm,
                                 data_directory=data_dir,
                                 text_columns=['name', 'title', 'content'])

preprocessor.load_data_dict()
preprocessor.transform_date()
preprocessor.combine_data_dict()
preprocessor.extract_hashtags(content_col='content',
                              hospital_re_target='.*(안과|병원|의원)$')

data_hospital, data_prsnl = preprocessor.hospital_prsnl_split(hospital_words_list=['병원', '의원', '외과', '안과'],
                                                              non_word_list=['동물', '동물병원'])

# Upload data_hospital and data_prsnl to s3
# TBD
