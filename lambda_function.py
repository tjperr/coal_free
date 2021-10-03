# https://www.elexon.co.uk/documents/training-guidance/bsc-guidance-notes/bmrs-api-and-data-push-user-guide-2/
# Use SAM? https://towardsdatascience.com/using-serverless-and-sam-to-deploy-a-scheduled-lambda-with-packages-ed7efdc73070
import json
import os
import requests
from io import StringIO

import httplib2
import pandas as pd


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

    try:
        df = pd.read_csv(
            StringIO(content),
            skiprows=1,
            skipfooter=2,  # skip footer and total row
            header=None,
        )

        df.columns = [
            "REPORT",
            "TYPE",
            "CURR_MW",
            "CURR_PCT",
            "LHH_MW",
            "LHH_PCT",
            "L24H_MW",
            "L24H_PCT",
        ]
    except:
        raise ValueError(f"BMRS response could not be successfully parsed\n\n{content}")

    coal_24h_percent = df["L24H_PCT"].values[0]
    return {"statusCode": 200, "body": json.dumps(coal_24h_percent)}

if __name__ == "__main__":
    print(lambda_handler(1, 2))
