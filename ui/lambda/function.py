from watson_machine_learning_client import WatsonMachineLearningAPIClient
import os


def lambda_handler(event, context):
    # List of Feature lists [[...,...,...],[...,...,...]]
    features = event["features"]

    wml_credentials={
        'url': os.getenv("IBM_URL"),
        'username': os.getenv("IBM_USERNAME"),
        'password': os.getenv("IBM_PASSWORD"),
        'instance_id': os.getenv("IBM_INSTANCE_ID"),
        'apikey': os.getenv("IBM_API_KEY"),
        'iam_apikey_name': os.getenv("IBM_API_KEY_NAME"),
        'iam_role_crn': os.getenv("IBM_ROLE_CRN"),
        'iam_serviceid_crn': os.getenv("IBM_SERVICE_ID_CRN")
    }

    client = WatsonMachineLearningAPIClient(wml_credentials)

    scoring_url = 'https://us-south.ml.cloud.ibm.com/v3/wml_instances/cc2d5c29-9b6a-4e09-a82c-8279e879d544/deployments/5a9d3cb5-aae1-49bc-be7f-26539c9e7ec5/online'
    payload_scoring = {'fields': ['acousticness','loudness','instrumentalness','danceability','valence','energy','duration_ms'],
                    'values': features}

    res = client.deployments.score(scoring_url, payload_scoring)
    return res