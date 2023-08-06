import os

from baram.s3_manager import S3Manager
from baram.kms_manager import KMSManager

s3 = S3Manager('sli-dst-security', KMSManager().get_kms_arn('s3-hydra01-kms'))
s3.upload_dir(os.path.join('nylondetector', 'crawling', 'crawl_data'), 'nylon-detector/crawl_data')
