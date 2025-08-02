import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from faker import Faker
from backend import database
import random

fake = Faker()

def generate_dummy_lead():
    return {
        "name": fake.name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "location": fake.city(),
        "company": fake.company(),
        "status": random.choice(["New", "Contacted", "Qualified", "Lost", "Converted"]),
        "source": random.choice(["Website", "Referral", "Cold Call", "LinkedIn"]),
        "notes": fake.sentence(),
        "last_contacted": fake.date_this_year().isoformat(),
        "interested_product": random.choice(["CRM Basic", "CRM Pro", "CRM Enterprise"]),
        "budget": random.randint(10000, 100000),
    }

def seed_leads(n=100):
    for _ in range(n):
        lead = generate_dummy_lead()
        database.insert_lead(lead)
    print(f"{n} dummy leads inserted into MongoDB successfully!")

if __name__ == "__main__":
    seed_leads(100)
