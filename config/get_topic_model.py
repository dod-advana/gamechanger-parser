import boto3
import tarfile 
from io import BytesIO
from pathlib import Path
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

local_destination_location = f'{BASE_DIR}/policy_analytics_parser/topic_extraction/model/'

source_bucket = "advana-data-zone"
source_prefix = "bronze/gamechanger/models/topic_model/v2"
model_zip_name = 'topic_model_20221129162954.tar.gz'
source_key = f"{source_prefix}/{model_zip_name}"

try:
    s3 = boto3.resource('s3')
    s3_obj = s3.Object(source_bucket, source_key)
    body_bytes = s3_obj.get()['Body'].read()
    bytes_obj = BytesIO(body_bytes)
except Exception as e:
    print("Error retrieving model from AWS, are you on VPN? is your AWS SAML active?")
    exit()

try:
    with tarfile.open(fileobj=bytes_obj) as tar:
        print("extracting model files in", local_destination_location)
        for member in tar.getmembers():
            print('member', member)
            if member.isfile():
                member.name = os.path.basename(member.name)
                print('member name', member.name)
                tar.extract(member, local_destination_location)
except Exception as e:
    print("Error extracting tar", e)
finally:
    print("Finished get_topic_model.py")