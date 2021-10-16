import json
import os
import boto3

def lambda_handler(event, context):
    """Read all historic data from the s3 datastore"""

    print("working")
    
    s3 = boto3.resource('s3')
    object = s3.Object(os.environ['bucket_name'], "data.json")
    data = json.loads(object.get()['Body'].read())

    print(data)
    return {"statusCode": 200, "body": str(data)}
