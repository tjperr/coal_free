import json
import os
from datetime import date

import boto3
import requests
import uuid


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

    if 'detail-type' in event and event['detail-type'] == 'Scheduled Event':
        run_type = 'prod'
    else:
        run_type = 'dev'

    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    table = dynamodb.Table(os.environ["DYNAMODB_NAME"])

    with table.batch_writer() as batch:
        batch.put_item(
            Item={
                "id": str(uuid.uuid4()),
                "date": date.today().isoformat(),
                "run_type": run_type,
                "coal_24h_percent": coal_24h_percent,
            }
        )

    return {"statusCode": 200, "body": coal_24h_percent}
