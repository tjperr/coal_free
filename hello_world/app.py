import json
import os
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

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    print("working")

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

    coal = content.split('\n')[1] # extract the COAL row from the reponse
    fields = coal.split(',')
    if len(fields) != 8:
        raise ValueError(f"Response from BMRS has unexpected length ({len(fields)}). Expected 8.")
    
    coal_24h_percent = fields[7]
    return {"statusCode": 200, "body": coal_24h_percent}
