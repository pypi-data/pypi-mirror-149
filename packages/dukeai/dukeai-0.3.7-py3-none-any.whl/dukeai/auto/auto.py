import boto3
import json
from dukeai.config import duke_auto_lambda_arn, rpa_auto_lambda_arn, ralock_auto_lambda_arn


def duke_auto(text, arn=None):
    if not arn:
        arn = duke_auto_lambda_arn
    lambda_client = boto3.client('lambda', region_name='us-east-1')

    payload = json.dumps({
                           "local": True,
                           "text": text
                        })

    lambda_response = lambda_client.invoke(
                                            FunctionName=arn,
                                            InvocationType='RequestResponse',
                                            Payload=payload
                                          )

    resp_str = lambda_response['Payload'].read()
    response = json.loads(resp_str)
    return response


def rpa_auto(text, arn=None):
    if not arn:
        arn = rpa_auto_lambda_arn
    lambda_client = boto3.client('lambda', region_name='us-east-1')

    payload = json.dumps({
                            "local": True,
                            "text": text
                        })

    lambda_response = lambda_client.invoke(
                                            FunctionName=arn,
                                            InvocationType='RequestResponse',
                                            Payload=payload
                                          )
    resp_str = lambda_response['Payload'].read()
    response = json.loads(resp_str)
    return response


def ralock_auto(text, arn=None):
    if not arn:
        arn = ralock_auto_lambda_arn
    lambda_client = boto3.client('lambda', region_name='us-east-1')

    payload = json.dumps({
                            "local": True,
                            "text": text
                        })

    lambda_response = lambda_client.invoke(
                                            FunctionName=arn,
                                            InvocationType='RequestResponse',
                                            Payload=payload
                                        )

    resp_str = lambda_response['Payload'].read()
    response = json.loads(resp_str)
    return response
