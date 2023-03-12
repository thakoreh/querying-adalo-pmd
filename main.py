from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import List
import requests
app = FastAPI()

class Content(BaseModel):
    name: str
    desc: str
    internaldesc: str

class ItemList(BaseModel):
    time:str
    items: List[Content]

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



@app.post("/askchatgpt",status_code=201)
async def makePlanWithGPT(data:ItemList=Body(...,embed=True),status_code=201):
    content = f"""Here are the places :\n"""
    for d in data.items:
        content += f"{d.name},{d.desc},{d.internaldesc}\n"
    content += f"""I want you to plan a romantic date with my wife keeping above places in mind which starts at {data.time}. It is not necessary to include all the places. You can also come up with alternate plans."""
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": f"{content}"}] 
    }
    return data
