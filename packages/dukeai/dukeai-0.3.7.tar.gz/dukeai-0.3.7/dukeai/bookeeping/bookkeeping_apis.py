# import os
# import boto3
# import base64
# import requests
# from getpass import getpass
# from dukeai.config import bookkeeping_endpoint
# from dukeai.bookeeping.bookeeping_categories import get_new_categories
#
#
# AnnotatorBucketName = "duke-web-applications"
# AnnotatorBucket = boto3.resource('s3').Bucket(AnnotatorBucketName)
#
#
# class BookkeepingApi:
#     def __init__(self):
#         self.bookkeeping_endpoint = bookkeeping_endpoint
#         self.access_token, self.customer_id = self.get_access_token()
#
#     def get_access_token(self):
#         try:
#             if "ACCESS_TOKEN" not in os.environ and "CUSTOMER_ID" not in os.environ:
#                 print('Enter Credentials to get access token')
#                 customer_id = getpass('Enter Customer ID').upper()
#                 password = getpass('Enter Customer Password')
#
#                 url = "https://api.duke.ai/token/get_token"
#                 headers = {
#                     'username': customer_id,
#                     'password': password
#                 }
#                 response = requests.get(url, headers=headers).json()
#
#                 if response['success'] is False:
#                     print(response['message'])
#                     access_token, customer_id = self.get_access_token()
#                     return access_token, customer_id
#
#                 access_token = response['data']['id_token']
#                 os.environ['ACCESS_TOKEN'], os.environ['CUSTOMER_ID'] = access_token, customer_id
#                 print('Successful !!')
#                 return access_token, customer_id
#             else:
#                 print('You already have a "ACCESS_TOKEN" and "CUSTOMER_ID" in your environment')
#                 access_token = os.environ['ACCESS_TOKEN']
#                 customer_id = os.environ['CUSTOMER_ID']
#                 return access_token, customer_id
#         except Exception as e:
#             print('Error !!')
#             print(e)
#             del os.environ['ACCESS_TOKEN']
#             del os.environ['CUSTOMER_ID']
#             access_token, customer_id = self.get_access_token()
#             return access_token, customer_id
#
#     def del_env_variable(self):
#         if "ACCESS_TOKEN" in os.environ and "CUSTOMER_ID" in os.environ:
#             del os.environ['ACCESS_TOKEN']
#             del os.environ['CUSTOMER_ID']
#             print(self.customer_id)
#             print('Removed "ACCESS_TOKEN" and "CUSTOMER_ID" from the environment')
#         else:
#             print('Variable "ACCESS_TOKEN" and "CUSTOMER_ID" not found in the environment')
#
#     def get_tax_info(self, tax_info):
#         """
#         tax_info: type of information should be as following - "tax_info","assets_info","cash_info".
#         "tax_info" for income deduction.
#         "assets_info" for assets deduction and "
#         cash_info" for Cash/Liability
#         """
#
#         url = bookkeeping_endpoint + f'/{self.customer_id}/tax_info/{tax_info}'
#
#         headers = {
#             'Authorization': self.access_token
#         }
#         response = requests.request("GET", url, headers=headers)
#
#         return response.json()
#
#     def update_tax_info(self, tax_info, payload):
#         """
#             payload =   {
#                           "Filling_Status": "string",
#                           "Pre_tax_deduction": {
#                             "status": true,
#                             "amount": 0
#                           },
#                           "Tax_credit": {
#                             "status": true,
#                             "amount": 0
#                           },
#                           "Standard_Deduction": {
#                             "status": true
#                           },
#                           "Itemize_Deduction": {
#                             "status": true,
#                             "amount": 0
#                           },
#                           "Other_Income": 0
#                         }
#         """
#
#         url = bookkeeping_endpoint + f'/{self.customer_id}/tax_info/{tax_info}'
#
#         headers = {
#             'Authorization': self.access_token,
#             'Content-Type': 'application/json'
#         }
#
#         response = requests.request("POST", url, headers=headers, data=payload)
#
#         return response.text
#
#     def get_financial_summary(self, payload):
#         """
#         payload={"from": "2021-1-1", "to": "2021-3-3"}
#         """
#         url = bookkeeping_endpoint + f'/{self.customer_id}/summary'
#
#         headers = {
#             'Authorization': self.access_token,
#             'Content-Type': 'application/json'
#         }
#
#         response = requests.post(url, headers=headers, json=payload)
#         print(response.text)
#         return response.json()
#
#     def generate_financial_report(self, payload):
#         """
#
#         {
#             from(string): Start time of request data time period. yyyy-MM-dd format. UTC.
#
#             to(string): End time of request data time period. yyyy-MM-dd format. UTC.
#
#             period(string): The time period of request data.
#             Support "Last Week", "Last Month", "Last Quarter" and "Year To Date"
#
#             report_type(string):Requested report type.
#             Support "Balance Sheet", "Expense", "YTD Tax Liability", "Profit&Loss", "Liabilities", "IFTA" and "POD"
#         }
#
#         Example Value
#         payload={
#                  "from": "2021-1-1",
#                  "to": "2021-3-3",
#                  "period": "<string>",
#                  "report_type": "<string>"
#                  }
#
#         """
#         url = bookkeeping_endpoint + f'/{self.customer_id}/gen_report'
#
#         headers = {
#             'Authorization': self.access_token,
#             'Content-Type': 'application/json'
#         }
#
#         response = requests.post(url, headers=headers, json=payload)
#         print(response.text)
#         return response.json()
#
#         pass
#
#     def get_ifta_trip_id(self):
#
#         url = bookkeeping_endpoint + f'/{self.customer_id}/ifta'
#
#         headers = {
#             'Authorization': self.access_token
#         }
#
#         response = requests.request("GET", url, headers=headers)
#
#         return response.json()
#
#     def send_ifta_data(self):
#         """
#         payload = {
#                       "positionList": [
#                         {
#                           "timestamp": "string",
#                           "state": "string",
#                           "longitude": "string",
#                           "latitude": "string"
#                         }
#                       ],
#                       "tripId": "c9c3cf65-e8fd-42b1-b600-a09bf2bf8838",
#                       "status": "new"
#                     }
#         """
#         url = bookkeeping_endpoint + f'/{self.customer_id}/ifta'
#
#         headers = {
#             'Authorization': self.access_token,
#             'Content-Type': 'application/json'
#         }
#
#         response = requests.request("POST", url, headers=headers)
#
#         return response.json()
#
#     def upload_files(self, file_dir):
#         url = f"https://api.duke.ai/api/{self.customer_id}/multiupload"
#
#         files = list()
#         payload = dict()
#         file_count = list()
#
#         for dir_ in file_dir:
#             file_name = dir_.split('/')[-1]
#             with open(dir_, "rb") as file:
#                 str1 = base64.b64encode(file.read())
#
#             payload.update({file_name: str(str1)[2:]})
#             file_count.append(1)
#
#             files.append((file_name, open(dir_, 'rb')))
#
#         payload.update({'fileCount': str(file_count)})
#
#         headers = {'Authorization': os.environ['ACCESS_TOKEN']}
#
#         response = requests.post(url, headers=headers, data=payload, files=files)
#
#         return response.json()
#
#     def get_file_status(self, payload):
#         """
#         payload="{\n    \"from\": \"<string>\",\n    \"to\": \"<string>\",\n    \"num_doc\": \"<number>\"\n}"
#
#         """
#         url = f"https://api.duke.ai/api/{self.customer_id}/status"
#
#         headers = {
#             'Authorization': os.environ['ACCESS_TOKEN'],
#             'Content-Type': 'application/json'
#         }
#
#         response = requests.post(url, headers=headers, json=payload)
#
#         return response.json()
#
#     def get_file_from_database(self, file_name):
#
#         url = f"https://api.duke.ai/api/{self.customer_id}/{file_name}"
#
#         headers = {
#             "Authorization": os.environ["ACCESS_TOKEN"],
#             "Content-Type": "application/octet-stream"
#         }
#
#         response = requests.get(url, headers=headers)  # , data=payload)
#
#         return response
#
#     def delete_file(self, file_sha):
#
#         url = f"https://api.duke.ai/api/{self.customer_id}/{file_sha}/fromuser"
#
#         headers = {
#             "Authorization": os.environ["ACCESS_TOKEN"],
#         }
#
#         response = requests.delete(url, headers=headers)
#         print(response.text)
#         return response.json()
#
#     def update_user_device_token(self, payload):
#         """
#         payload=  {
#                     "DeviceTk": "<string>",
#                     "OS": "<string>",
#                     "promoCode": "<string>"
#                  }
#
#         """
#         url = f"{bookkeeping_endpoint}/{self.customer_id}"
#         headers = {
#             "Authorization": os.environ["ACCESS_TOKEN"],
#             "Content-Type": "application/json"
#         }
#
#         response = requests.put(url, headers=headers, json=payload)
#         print(response.text)
#         return response.json()
#
#     def delete_user_device_token(self, payload):
#
#         """
#
#         """
#         url = f"{bookkeeping_endpoint}/{self.customer_id}"
#         headers = {
#             "Authorization": os.environ["ACCESS_TOKEN"],
#             "Content-Type": "application/json"
#         }
#
#         response = requests.delete(url, headers=headers, json=payload)
#         print(response.text)
#         return response.json()
#
#     def delete_unconfirmed_cust_id(self):
#         url = f"{bookkeeping_endpoint}/{self.customer_id}/unconfirmed"
#
#         headers = {
#             "Authorization": os.environ["ACCESS_TOKEN"],
#         }
#
#         response = requests.delete(url, headers=headers)
#         print(response.text)
#         return response.json()
#
#     def check_promocode(self, payload):
#         """
#         payload={"promoCode": "<string>"}
#
#         """
#         print(self.customer_id)
#         url = f"{bookkeeping_endpoint}/promocodecheck"
#
#         headers = {
#             "Authorization": os.environ["ACCESS_TOKEN"],
#             "Content-Type": "application/json"
#         }
#
#         response = requests.post(url, headers=headers, json=payload)
#         print(response.text)
#         return response.json()
#
#     def get_duke_categories(self):
#         print('Loading Categories')
#         return get_new_categories
