from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
import os
from datetime import date, datetime
from pydantic import BaseModel, validator

class JobApplication(BaseModel):
    role: str
    company: str
    application_date: date

    # Validator to convert date to datetime
    @validator('application_date', pre=True, always=True)
    def convert_date_to_datetime(cls, v):
        if isinstance(v, date) and not isinstance(v, datetime):
            return datetime(v.year, v.month, v.day)
        return v


app = FastAPI()

# MongoDB client setup
client = AsyncIOMotorClient(os.getenv("MONGO_URL", "mongodb://localhost:27017"))
db = client["job_app_tracker"]  # Database name
collection = db["applications"]  # Collection name

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = client
    app.mongodb = db

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

@app.post("/applications/")
async def add_application(application: JobApplication):
    # Ensure application is a dict with datetime converted for MongoDB
    app_data = application.dict()
    app_data['application_date'] = application.convert_date_to_datetime(application.application_date)
    new_app = await collection.insert_one(app_data)
    return {"message": "Application added successfully", "id": str(new_app.inserted_id)}


@app.get("/applications/")
async def get_applications():
    applications = []
    async for application in collection.find():
        applications.append(JobApplication(**application))
    return applications

@app.get("/applications/count")
async def count_applications():
    count = await collection.count_documents({})
    return {"total_applications": count}


