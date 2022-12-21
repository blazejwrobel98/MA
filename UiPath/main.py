import json
import requests
import config


def authorize():
    endpoint = 'https://orchestrator.test.rpa.azure.assaabloy.net/api/Account/Authenticate'
    body = {'tenancyName': 'default', 'usernameOrEmailAddress': config.user, 'password': config.pw}
    r = requests.post(url=endpoint, json=body)
    bearer = r.json()['result']
    return bearer


def get_new_item(bearer):
    endpoint = "https://orchestrator.test.rpa.azure.assaabloy.net/odata/QueueItems?%24filter=QueueDefinitionId%20eq%20197%20and%20Status%20eq%20'InProgress'"
    h = {'authorization': f'bearer {bearer}', 'X-UIPATH-OrganizationUnitId': str(17)}
    r = requests.get(endpoint, headers=h)
    id = (r.json()['value'][0]['Id'])
    return id


def set_status(bearer, id):
    endpoint = f"https://orchestrator.test.rpa.azure.assaabloy.net/odata/Queues({id})/UiPathODataSvc.SetTransactionResult"
    h = {'authorization': f'bearer {bearer}', 'X-UIPATH-OrganizationUnitId': str(17)}
    body = {
        "transactionResult": {
            "IsSuccessful": "true",
            "ProcessingException": {
                "Reason": "nie dziala",
                "Details": "bo sie zepsulo",
                "Type": "ApplicationException",
                "AssociatedImageFilePath": "string"
            },
            "Output": {},
            "Analytics": {},
            "Progress": "string"
        }
    }

    r = requests.post(endpoint, headers=h, data=json.dumps(body))
    print(r.json())


b = authorize()
id = get_new_item(b)
set_status(b, id)
