import json
from database import insert_lead

# Full absolute path to the JSON file
file_path = "/Users/ayushtripathi/ChatBot/crm-chatbot-assistant/data/demo_leads.json"

with open(file_path, "r") as f:
    leads = json.load(f)

inserted_count = 0
for lead in leads:
    lead.pop("id", None)  # remove 'id' if present (MongoDB creates its own)
    insert_lead(lead)
    inserted_count += 1

print(f"✅ Inserted {inserted_count} leads into MongoDB")
