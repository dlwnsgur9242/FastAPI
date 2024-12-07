from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import requests

app = FastAPI()

db = [] #데이터베이스
#------------------------------------------------------------------------------
# date models
#------------------------------------------------------------------------------
class City(BaseModel):  #모델
    name: str
    timezone: str


templates = Jinja2Templates(directory="templates")


@app.get("/")
def root():
    return {"message":"Hello World!"}


@app.get('/cities', response_class=HTMLResponse)
def get_cities(request: Request): # Request에 모든 정보를 받게된다.
    context = {}

    rsCity = []

    cnt = 0
    for city in db:
        str = f"http://worldtimeapi.org/api/timezone/{city['timezone']}"
        r = requests.get(str)
        cur_time = r.json()['datetime']

        cnt += 1 
        # 'id': cnt,
        rsCity.append({'id':cnt, 'name':city['name'], 'timezone':city['timezone'], 'current_time':cur_time})

    context['request'] = request
    context['rsCity'] = rsCity

    return templates.TemplateResponse('city_list.html', context)

@app.get('/cities/{city_id}')
def get_city(city_id: int):
    city = db[city_id-1]
    r = f"http://worldtimeapi.org/api/timezone/{city['timezone']}"
    r = requests.get(r)
    cur_time = r.json()['datetime']

    return {'name':city['name'],'timezone':city['timezone'],'current_time':cur_time}


@app.post('/cities')
def create_city(city: City):

    db.append(city.dict())
    
    return db[-1]

@app.delete('/cities/{city_id}')
def delete_city(city_id: int):
    db.pop(city_id-1)
    return {}