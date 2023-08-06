import base64
import boto3
import json
import os
from getpass import getpass
from dukeai.config import img_ocr_function_arn, pdf_ocr_function_arn


def duke_ocr(file_directory, crop=None):
    """
        This is the ocr funtion which extracts text out of IMAGEs and PDFs

        Requirements:
            Define "AWS_ACCESS_KEY_ID" and "AWS_SECRET_ACCESS_KEY" as environement variable

        Code:
            import os
            os.environ['AWS_ACCESS_KEY_ID'] = "--AWS_ACCESS_KEY_ID--"
            os.environ['AWS_SECRET_ACCESS_KEY'] = "--AWS_SECRET_ACCESS_KEY--"

        Args:
            file_directory (string): file directory you want the ocr from
        Returns:
            return1 (dic): {'text': 'Dummy PDF file\n\x0c'}
    z

    """
    
    if "AWS_ACCESS_KEY_ID" not in os.environ:
        print('AWS_ACCESS_KEY_ID key not found')
        os.environ['AWS_ACCESS_KEY_ID'] = getpass('Enter AWS_ACCESS_KEY_ID ')

    if "AWS_SECRET_ACCESS_KEY" not in os.environ:
        print('AWS_SECRET_ACCESS_KEY key not found')
        os.environ['AWS_SECRET_ACCESS_KEY'] = getpass('Enter AWS_SECRET_ACCESS_KEY')

    if "AWS_ACCESS_KEY_ID" in os.environ and "AWS_SECRET_ACCESS_KEY" in os.environ:
        try:
            lambda_client = boto3.client('lambda', region_name='us-east-1')

            if crop:
                payload = json.dumps({
                                       "local": True,
                                       "crop": True,
                                       "body": base64.b64encode(open(file_directory, 'rb').read()).decode('utf-8'),
                                    })
            else:
                payload = json.dumps({
                                        "local": True,
                                        "body": base64.b64encode(open(file_directory, 'rb').read()).decode('utf-8'),
                                    })

            if file_directory.split('.')[-1].lower() in ['pdf']:
                lambda_response = lambda_client.invoke(
                                                        FunctionName=pdf_ocr_function_arn,
                                                        InvocationType='RequestResponse',
                                                        Payload=payload
                                                      )
                resp_str = lambda_response['Payload'].read()
                response = json.loads(resp_str)
                return response

            if file_directory.split('.')[-1].lower() in ['jpeg', 'jpg', 'png']:
                lambda_response = lambda_client.invoke(
                                                        FunctionName=img_ocr_function_arn,
                                                        InvocationType='RequestResponse',
                                                        Payload=payload
                                                      )

                resp_str = lambda_response['Payload'].read()
                response = json.loads(resp_str)
                return response

        except Exception as e:
            print(str(e))
    else:
        return None
