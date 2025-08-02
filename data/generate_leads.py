from faker import Faker
import json
from random import choice, randint
from datetime import datetime, timedelta

fake = Faker()
statuses = ["New", "Contacted", "Interested", "Not Interested", "Converted"]
cities = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata", "Pune"]

leads = []

for i in range(120):
    lead = {
        "id": i + 1,
        "name": fake.first_name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "city": choice(cities),
        "status": choice(statuses),
        "created_at": (datetime.today() - timedelta(days=randint(0, 30))).strftime('%Y-%m-%d')
    }
    leads.append(lead)

with open("demo_leads.json", "w") as f:
    json.dump(leads, f, indent=2)

print("✅ Generated 120 demo leads in demo_leads.json")
