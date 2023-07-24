from fastapi import FastAPI
from redis_om import get_redis_connection, HashModel
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from pydantic import BaseModel
import redis
from starlette.requests import Request
import requests
from fastapi.background import BackgroundTasks
import time


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

@app.get('/')
def check():
    return {"Message":"Checked"}
@app.post('/orders')
async def create(request: Request, background_tasks: BackgroundTasks):  # id, quantity
    body = await request.json()

    req = requests.get('http://localhost:8000/products/%s' % body['id'])
    product = req.json()

    order = Order(
        product_id=body['id'],
        price=product['price'],
        fee=0.2 * product['price'],
        total=1.2 * product['price'],
        quantity=body['quantity'],
        status='pending'
    )
    order.save()

    background_tasks.add_task(order_completed, order)

    return order


def order_completed(order: Order):
    order.status = 'completed'
    order.save()



