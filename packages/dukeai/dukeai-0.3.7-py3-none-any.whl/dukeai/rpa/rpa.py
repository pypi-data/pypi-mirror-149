# import requests
# from magic import Magic
# from dukeai.config import rpa_endpoint
#
#
# def upload_document(client_id: str, doc_id: str, file_dir: str, api_key: str):
#     mime = Magic(mime=True)
#     url = f"{rpa_endpoint}/client/multiupload/{client_id}?doc_id={doc_id}"
#     # url = f"https://kr67bvc0ih.execute-api.us-east-1.amazonaws.com/api/client/multiupload/{client_id}?doc_id={doc_id}"
#     file_name = file_dir.split('/')[-1]
#     mime_type = mime.from_file(file_dir)
#     files = [('file', (file_name, open(file_dir, 'rb'), mime_type, None))]
#     headers = {'x-api-key': api_key}
#     response = requests.request("POST", url, headers=headers, files=files)
#     return response.json()
