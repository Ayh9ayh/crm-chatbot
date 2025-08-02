from pymongo import MongoClient
from bson.objectid import ObjectId
import os
import json

# MongoDB connection string
MONGO_URI = "mongodb+srv://ayush_user:Ayh9ayh@cluster0.dh4poxl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Initialize MongoDB client and database
client = MongoClient(MONGO_URI)
db = client["crmdb"]
leads_collection = db["leads"]

# Fetch all leads (excluding _id)
def get_all_leads():
    return list(leads_collection.find({}, {"_id": 0}))

# Add the missing function that chatbot.py expects
def get_leads_from_db():
    """Alias for get_all_leads to match chatbot.py expectations"""
    return get_all_leads()

# Insert a new lead
def insert_lead(lead_data):
    result = leads_collection.insert_one(lead_data)
    return str(result.inserted_id)

# Get lead by ID
def get_lead_by_id(lead_id):
    return leads_collection.find_one({"_id": ObjectId(lead_id)})

# Update lead by ID
def update_lead(lead_id, update_data):
    result = leads_collection.update_one(
        {"_id": ObjectId(lead_id)},
        {"$set": update_data}
    )
    return result.modified_count > 0

# Delete lead by ID
def delete_lead(lead_id):
    result = leads_collection.delete_one({"_id": ObjectId(lead_id)})
    return result.deleted_count > 0

# Search leads by any key-value pair (e.g., name, status, email)
def search_leads_by_field(field, value):
    return list(leads_collection.find({field: {"$regex": value, "$options": "i"}}, {"_id": 0}))
def add_new_lead(lead_data):
    try:
        leads_collection.insert_one(lead_data)
        return True
    except Exception as e:
        print("Insert failed:", e)
        return False
