# https://www.elexon.co.uk/documents/training-guidance/bsc-guidance-notes/bmrs-api-and-data-push-user-guide-2/
# Use SAM? https://towardsdatascience.com/using-serverless-and-sam-to-deploy-a-scheduled-lambda-with-packages-ed7efdc73070
import httplib2
import os

import json

def lambda_handler(event, context):
    print('working')
    bmrs_key = os.environ['bmrs_key']
    x = post_elexon(
        url=f"https://api.bmreports.com/BMRS/FUELINSTHHCUR/v1?APIKey={bmrs_key}&FuelType=COAL&ServiceType=csv",
    )
    print('working')
    coal_24h_percent = float(str(x).split(',')[8].split('\\n')[0])
    print(coal_24h_percent)
    return {
        'statusCode': 200,
        'body': json.dumps(coal_24h_percent)
    }


def post_elexon(url):
    http_obj = httplib2.Http()
    resp, content = http_obj.request(
    uri=url,
    method='GET',
    headers={'Content-Type': 'application/xml; charset=UTF-8'},
    )
    # print('===Response===')
    # print(resp)
    # print('===Content===')
    # print(content)

    # print('===Finished===')
    return content


if __name__ == "__main__":
    lambda_handler(1, 2)