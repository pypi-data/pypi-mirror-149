import os

import ujson as json

from baram.s3_manager import S3Manager
from baram.kms_manager import KMSManager

s3 = S3Manager('sli-dst-security', KMSManager().get_kms_arn('s3-hydra01-kms'))
s3.download_file('nylon-detector/train_test/train.csv', 'train.csv')

with open('train.csv') as r:
    input_list = []
    for c in r.readline().split(","):
        c = c.strip()
        if 'label' == c:
            continue
        if 'embed' in c:
            input_list.append({'name': c, 'type': 'DECIMAL'})
        else:
            input_list.append({'name': c, 'type': 'INTEGER'})
    obj = {'inputContentType': 'CSV',
           'outputContentType': 'CSV'}
    obj['input'] = input_list
    obj['output'] = [{'name': 'label', 'type': 'INTEGER'}]
    obj['description'] = 'nylon-detector'
    obj['version'] = 'v1'
    obj['instanceCount'] = 1
    obj['instanceTypes'] = ['ml.c5.2xlarge']
    obj['defaultInstanceType'] = 'ml.c5.2xlarge'

    with open('quicksight_schema.json', 'w') as f:
        f.write(json.dumps(obj, indent=4))

os.remove('train.csv')
