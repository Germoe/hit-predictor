from watson_machine_learning_client import WatsonMachineLearningAPIClient
import os


def lambda_handler(event, context):
    # List of Feature lists [[...,...,...],[...,...,...]]
    features = event["features"]

    wml_credentials={
        'url': os.getenv("IBM_URL"),
        'username': os.getenv("IBM_USERNAME"),
        'password': os.getenv("IBM_PASSWORD"),
        'instance_id': os.getenv("IBM_INSTANCE_ID")
    }

    client = WatsonMachineLearningAPIClient(wml_credentials)

    scoring_url = 'https://us-south.ml.cloud.ibm.com/v3/wml_instances/cc2d5c29-9b6a-4e09-a82c-8279e879d544/deployments/5a9d3cb5-aae1-49bc-be7f-26539c9e7ec5/online'
    payload_scoring = {'fields': ['acousticness','loudness','instrumentalness','danceability','valence','energy','duration_ms'],
                    'values': features}

    res = client.deployments.score(scoring_url, payload_scoring)
    return {
       "Number1": number1,
       "Number2": number2,
       "Sum": sum,
       "Product": product,
       "Difference": difference,
       "Quotient": quotient
   }