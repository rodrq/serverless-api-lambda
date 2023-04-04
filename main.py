from fastapi import FastAPI, HTTPException
from boto3.dynamodb.conditions import Key
from mangum import Mangum

app = FastAPI()

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('your_table_name')

@app.get("/")
async def root():
    return {"message": "Hello world"}

@app.get("/get-fare/{day}") #Gets all fares from day
async def get_fare(day: str):
    response = table.query(KeyConditionExpression=Key('date').eq(day))
    items = response.get("Items")
    if not items:
        raise HTTPException(status_code=404, detail=f"Fare not found for {day} at {hour}")
    return items

@app.get("/get-fare/{day}/{hour}") #Gets certain hour fare
async def get_fare(day: str, hour: str):
    response = table.query(
            KeyConditionExpression=Key('date').eq(day) & Key('time').eq(hour)
        )
    items = response.get("Items")
    if not items:
        raise HTTPException(status_code=404, detail=f"Fare not found for {day} at {hour}")
    return items

handler = Mangum(app)