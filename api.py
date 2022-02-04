import requests
from loguru import logger
import json


logger.add("logging.log", format="{time}, {level}, {message}", level="DEBUG", encoding="UTF-8")

headers = {
    'X-ACCESS-KEY': "KEY",
    'X-SECRET-KEY': "KEY"
}

URL = 'https://api.bemob.com/v1/campaigns'
url_workspaces_id = 'https://api.bemob.com/v1/user/workspaces'

querystring = {'status': 'active', 'workspaceIds': 'ID}

def get_campaings(campaigns):
    response = requests.request("GET", URL, headers=headers, params=querystring)
    data = json.loads(response.text)
    result_dict = dict()
    for item in data['payload']:
        if item['nameFull'] == campaigns:
            result_dict["workspaceId"] = item["workspaceId"]
            result_dict['trafficSourceId'] = item['trafficSourceId']
            result_dict['name'] = item['name']
            result_dict['countryId'] = item['countryId']
            result_dict['trackingDomainId'] = item['trackingDomainId']
            result_dict['redirectDomainId'] = item['redirectDomainId']
            result_dict['trafficLossPercent'] = item['trafficLossPercent']
            result_dict['postbackPercent'] = item['postbackPercent']
            result_dict['redirectMode'] = item['redirectMode']
            result_dict['costValue'] = float(item['costValue'])
            result_dict['costModel'] = item['costModel']
            result_dict['currencyId'] = item['currencyId']
            result_dict['destinationType'] = item['destinationType']
            result_dict['flowId'] = item['flowId']
            result_dict['destinationUrl'] = item['destinationUrl']
            result_dict['status'] = item['status']
            result_dict['flowInline'] = item['flowInline']
            result_dict["uniquenessPeriod"] = 86400
            result_dict['enableSixthSense'] = True
            result_dict['setCustomUniqueness'] = True
            flow = result_dict['flowId']
            url_flow = f'https://api.bemob.com/v1/flows'
            response_get_flow =  requests.request("GET", url_flow, headers=headers)
            data_flow = json.loads(response_get_flow.text)
            with open('data_flow.txt', 'w', encoding='UTF-8') as file:
                json.dump(data_flow, file, indent=4, ensure_ascii=False)
            for item in data_flow['payload']:
                if item['id'] == result_dict['flowId']:
                    result_dict['flowInline']['rules'] = item['rules']

    with open('data.txt', 'w', encoding='UTF-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    return result_dict


@logger.catch()
def post_create_campaigns(data: dict):
    URL = "URL"
    logger.info(data)
    response = requests.request("POST", URL, json=data)
    print(response.status_code)
    if response.status_code == 200:
        logger.info(response.text)
        data = json.loads(response.text)
        with open('data_country.txt', 'w', encoding='UTF-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        url_campaign = []
        url_cam = data['payload']['campaignUrl']
        name = data['payload']['nameFull']
        url_campaign.append(url_cam)
        url_campaign.append(name)
        return url_campaign
    else:
        logger.info(data)
        logger.info(response.text)
        logger.info(response.status_code)
