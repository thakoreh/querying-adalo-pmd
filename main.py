from fastapi import FastAPI
import requests
app = FastAPI()

@app.get("/{apikey}/{nextid}")
def searchRecordsWithNextID(nextid,apikey):
    our_result_records = []
    apiURL = "https://api.adalo.com/v0/apps/8dbf054c-3069-4216-a8b3-4ece69d7625a/collections/t_8voklgehc3pmpv1vs24tut1p1"
    headers = {'Content-Type':'application/json',"Authorization":f"Bearer {apikey}"}
    response = requests.get(apiURL,headers=headers)
    responseJSON = response.json()
    recordsPresent = responseJSON["records"]
    our_result_records.extend(list(filter(lambda x:float(x['NextId'])==float(nextid) and x['is_check']==True,recordsPresent)))
    while 'offset' in responseJSON:
        apiURL = f"https://api.adalo.com/v0/apps/8dbf054c-3069-4216-a8b3-4ece69d7625a/collections/t_8voklgehc3pmpv1vs24tut1p1?offset={responseJSON['offset']}"
        response = requests.get(apiURL,headers=headers)
        responseJSON = response.json()
        recordsPresent = responseJSON["records"]
        our_result_records.extend(list(filter(lambda x:float(x['NextId'])==float(nextid) and x['is_check']==True,recordsPresent)))
    return our_result_records