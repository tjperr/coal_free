# https://www.elexon.co.uk/documents/training-guidance/bsc-guidance-notes/bmrs-api-and-data-push-user-guide-2/
# Use SAM? https://towardsdatascience.com/using-serverless-and-sam-to-deploy-a-scheduled-lambda-with-packages-ed7efdc73070
import json
import os
import requests
from io import StringIO

import httplib2


def lambda_handler(event, context):
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
    return {"statusCode": 200, "body": json.dumps(coal_24h_percent)}

if __name__ == "__main__":
    print(lambda_handler(1, 2))
