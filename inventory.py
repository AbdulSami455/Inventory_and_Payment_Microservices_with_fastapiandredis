from fastapi import FastAPI
from redis_om import get_redis_connection,HashModel
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from pydantic import BaseModel
import redis

# Replace 'your_redis_hostname' with the hostname or IP address of your online Redis server
# Replace 'your_redis_port' with the port number of your online Redis server
# Replace 'your_redis_password' with the password for the online Redis server (if applicable)
r = get_redis_connection(
    host='redis-12992.c239.us-east-1-2.ec2.cloud.redislabs.com',
    port=12992,
    password='SexaJKNvTACCea53G4aoY3ARyQe6c5bs',
    decode_responses=True
)

# Test the connection
try:
    response = r.ping()
    if response:
        print("Successfully connected to Redis!")
except redis.exceptions.ConnectionError as e:
    print("Failed to connect to Redis:", e)

class Product(BaseModel):
    name: str
    price: float
    quantity: int
    class Meta:
        database=redis

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello Everyone"}

# Applying middleware
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])


@app.post("/products")
def addproducts(product:Product):
    return product.save()
