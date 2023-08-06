# import boto3
# import json
# AnnotatorBucketName = "duke-web-applications"
# AnnotatorBucket = boto3.resource('s3').Bucket(AnnotatorBucketName)
#
#
# def get_new_categoryInfo():
#     with open('/tmp/receiptSubcategoryToCategoryDict.json', 'wb') as data:
#         AnnotatorBucket.download_fileobj('receiptSubcategoryToCategoryDict.json', data)
#     file_path = "/tmp/receiptSubcategoryToCategoryDict.json"
#     f = open(file_path, 'r')
#     receiptSubcategoryToCategoryDict = json.load(f)
#     f.close()
#
#     receiptSubcategoryTocategoryList = list(receiptSubcategoryToCategoryDict.keys())
#     receiptSubcategoryTocategoryList.sort(key=lambda s: len(s), reverse=True)
#
#     with open('/tmp/invoiceSubcategoryToCategoryDict.json', 'wb') as data:
#         AnnotatorBucket.download_fileobj('invoiceSubcategoryToCategoryDict.json', data)
#     file_path = "/tmp/invoiceSubcategoryToCategoryDict.json"
#     f = open(file_path, 'r')
#     invoiceSubcategoryToCategoryDict = json.load(f)
#     f.close()
#
#     invoiceSubcategoryToCategoryList = list(invoiceSubcategoryToCategoryDict.keys())
#     invoiceSubcategoryToCategoryList.sort(key=lambda s: len(s), reverse=True)
#
#     with open('/tmp/subcatToAssetDict.json', 'wb') as data:
#         AnnotatorBucket.download_fileobj('subcatToAssetDict.json', data)
#     file_path = "/tmp/subcatToAssetDict.json"
#     f = open(file_path, 'r')
#     subcatToAssetDict = json.load(f)
#     f.close()
#
#     subcatToAssetList = list(subcatToAssetDict.keys())
#     subcatToAssetList.sort(key=lambda s: len(s), reverse=True)
#
#     return invoiceSubcategoryToCategoryDict, invoiceSubcategoryToCategoryList, receiptSubcategoryToCategoryDict, receiptSubcategoryTocategoryList, subcatToAssetDict, subcatToAssetList
#
#
# invoiceSubcategoryToCategoryDict, invoiceSubcategoryToCategoryList, receiptSubcategoryToCategoryDict, receiptSubcategoryTocategoryList, subcatToAssetDict, subcatToAssetList = get_new_categoryInfo()
#
#
# def get_new_asset(subcategory):
#     for asset_type in subcatToAssetList:
#         if asset_type.upper() in subcategory.upper():
#             return subcatToAssetDict[asset_type]
#     return "TODO"
#
#
# def get_new_categories(subcategory, type_of_doc):
#     if type_of_doc == "invoice":
#         for cat in invoiceSubcategoryToCategoryList:
#             if cat.upper() in subcategory.upper():
#                 asset_type = get_new_asset(cat)
#                 return cat, invoiceSubcategoryToCategoryDict[cat], asset_type
#     if type_of_doc == "receipt":
#         for cat in receiptSubcategoryTocategoryList:
#             if cat.upper() in subcategory.upper():
#                 asset_type = get_new_asset(cat)
#                 return cat, receiptSubcategoryToCategoryDict[cat], asset_type
#
#     return "TODO", "TODO", "TODO"
#
# # class Bookkeeping_categories:
# #     def __init__(self):
# #         return get_new_categories
