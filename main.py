from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import List
import requests
app = FastAPI()

class Content(BaseModel):
    name: str
    desc: str
    internaldesc: str

class DataContent(BaseModel):
    id: int
    name: str
    location: str
    image_of_place: bytes
    reviews: str
    description: str
    internaluse_user: str
    ratings: int
    address: str
    place_id: str
    latitude: float
    longitude: float
    next_id: float
    is_check: bool
    phone: str
    is_open_now: bool
    created_at: str
    updated_at: str

class ItemList(BaseModel):
    time:str
    items: List[Content]

class dataList(BaseModel):
    data: List[DataContent]

@app.get("/{openaikey}/{apikey}/{nextid}/{time}")
def searchRecordsWithNextID(nextid,openaikey,apikey,time):
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
    
    #generating prompt
    content = f"""Here are the places :\n"""
    for eachRecord in our_result_records:
        content += f"{eachRecord['Name']},{eachRecord['Description']},{eachRecord['InternalUse_User']}\n"

    content += f"""I want you to plan a romantic date with my partner keeping above places in mind which starts at {time}. It is not necessary to include all the places. You can also come up with alternate plans."""
    prompt = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": content}] 
    }
    gptheaders = {'Content-Type':'application/json',"Authorization":f"Bearer {openaikey}"}
    url='https://api.openai.com/v1/chat/completions'
    responseCHATGPT = requests.post(url,headers=gptheaders,json=prompt)
    return responseCHATGPT.json()
