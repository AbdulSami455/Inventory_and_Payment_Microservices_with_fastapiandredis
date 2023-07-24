from fastapi import FastAPI
from redis_om import get_redis_connection, HashModel
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from pydantic import BaseModel
import redis
from starlette.requests import Request
import requests
# Replace 'your_redis_hostname' with the hostname or IP address of your online Redis server
# Replace 'your_redis_port' with the port number of your online Redis server
# Replace 'your_redis_password' with the password for the online Redis server (if applicable)
r = get_redis_connection(
    host='redis-12992.c239.us-east-1-2.ec2.cloud.redislabs.com',
    port=12992,
    password='SexaJKNvTACCea53G4aoY3ARyQe6c5bs',
    decode_responses=True
)

class Order(HashModel):
    productid:str
    price:float
    fee:float
    total:float
    quantity:float
    status :str

    class Meta:
        database=redis
app=FastAPI()


app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

@app.post('/orders')
def create(request:Request):
    body=await request.json()
    req = requests.get('http://localhost:8000/products/%s' % body['id'])
    return  req.json()


