import boto3
import os

# using server side encryption for the bucket make sure that data is encypted on transport and rest
def send_request_to_s3(data):
    script_dir=os.path.dirname('.')
    file_name=os.path.join(script_dir,'data/input.json')
    bucket_name='clouday1-userdata'
    object_name='user-'+data['account_name']+'.json'
    client=boto3.client('s3',region_name=data['region'][0])
    try:
        client.upload_file(file_name,bucket_name,object_name)
    except:
        print('Failed to export to S3')

send_request_to_s3({
    "account_name":"clouday1",
    "aws_access_key_id":"AKIAIOSFODNN7EXAMPLE",
    "aws_secret_access_key":"wJalrXUtnFEMI/K7MDENG/bZ",
    "region":["us-east-1"],
    "aws_sesssion_token":""
})