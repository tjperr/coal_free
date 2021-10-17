import json
import os
from datetime import date

import boto3
import requests


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    print("working")
    print(event)

    session = requests.session()
    response = session.get(
        f"https://api.bmreports.com/BMRS/FUELINSTHHCUR/v1",
        params={
            "APIKey": os.environ["bmrs_key"],
            "FuelType": "COAL",
            "ServiceType": "csv",
        },
    )
    content = response.text
    print(content)

    coal = content.split("\n")[1]  #  extract the COAL row from the reponse
    fields = coal.split(",")

    if len(fields) != 8:
        raise ValueError(
            f"Response from BMRS has unexpected length ({len(fields)}). Expected 8."
        )

    coal_24h_percent = fields[7]

    if "detail-type" in event and event["detail-type"] == "Scheduled Event":
        filename = f"data.json"
    else:
        filename = f"dev-data.json"

    s3 = boto3.resource("s3")
    object = s3.Object(os.environ["bucket_name"], filename)

    try:
        existing_data = json.loads(object.get()["Body"].read())
    except:
        print(f"object {filename} does not exist - creating new object")
        existing_data = {}

    existing_data[str(date.today().isoformat())] = coal_24h_percent
    object.put(Body=json.dumps(existing_data))

    return {"statusCode": 200, "body": coal_24h_percent}
