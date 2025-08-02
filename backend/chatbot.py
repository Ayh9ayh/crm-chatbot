from backend.database import get_leads_from_db

from collections import Counter
import re

def process_query(query: str):
    print(f"User query: {query}")
    query_lower = query.lower()
    leads = get_leads_from_db()


    if not leads:
        return {"message": "No leads available."}

    known_cities = ["delhi", "mumbai", "pune", "bangalore", "chennai", "hyderabad", "noida", "kolkata"]
    known_statuses = ["new", "interested", "pending", "converted", "not contacted", "yet to be contacted"]

    # CASE 1: Show/List leads (filtered by city or status)
    if "lead" in query_lower and ("show" in query_lower or "list" in query_lower):
        city_found = next((city for city in known_cities if city in query_lower), None)
        if city_found:
            filtered_leads = [lead for lead in leads if lead.get('city', 'unknown').lower() == city_found]
            return {
                "message": f"Found {len(filtered_leads)} leads from {city_found.title()}",
                "leads": filtered_leads
            } if filtered_leads else {"message": f"No leads found in {city_found.title()}."}

        status_found = next((status for status in known_statuses if status in query_lower), None)
        if status_found:
            filtered_leads = [lead for lead in leads if lead.get('status', 'unknown').lower() == status_found]
            return {
                "message": f"Found {len(filtered_leads)} leads with status '{status_found}'",
                "leads": filtered_leads
            } if filtered_leads else {"message": f"No leads with status '{status_found}' found."}

        return {"message": f"Found {len(leads)} total leads", "leads": leads}

    # CASE 2: Count leads (total or by status/city) - Updated patterns
    if "how many" in query_lower or "count" in query_lower:
        # Count of leads by city
        if ("by city" in query_lower) or ("per city" in query_lower) or ("count of leads by city" in query_lower):
            city_counter = Counter(lead.get("city", "Unknown") for lead in leads)
            return {
                "message": "Lead count by city",
                "data": dict(city_counter)
            }
        
        # How many leads per status
        if ("per status" in query_lower) or ("by status" in query_lower) or ("how many leads per status" in query_lower):
            status_counter = Counter(lead.get("status", "Unknown").lower() for lead in leads)
            return {
                "message": "Lead count by status",
                "data": dict(status_counter)
            }

        if "lead" in query_lower:
            for status in known_statuses:
                if status in query_lower:
                    count = sum(1 for lead in leads if lead.get("status", "unknown").lower() == status)
                    return {"message": f"There are {count} leads with status '{status}'."}

            return {"message": f"There are {len(leads)} leads in total."}

    # CASE 3: City reports or unique cities - Updated patterns
    if ("city" in query_lower or "cities" in query_lower) and "lead" in query_lower:
        # Top cities with most leads
        if ("top cities" in query_lower) or ("top" in query_lower and "most" in query_lower):
            city_counter = Counter(lead.get("city", "Unknown") for lead in leads)
            top_cities = city_counter.most_common(3)
            return {
                "message": "Top cities with most leads",
                "data": dict(top_cities)
            }

        if "count" in query_lower or "how many" in query_lower or "per" in query_lower:
            city_counter = Counter(lead.get("city", "Unknown") for lead in leads)
            return {
                "message": f"There are {sum(city_counter.values())} leads across {len(city_counter)} cities.",
                "data": dict(city_counter)
            }

        cities = sorted(set(lead.get("city", "Unknown") for lead in leads))
        return {
            "message": f"Leads are from the following cities: {', '.join(cities)}."
        }

    # CASE 4: Summary - Updated pattern
    if ("summary" in query_lower) or ("summary of all leads" in query_lower):
        city_counter = Counter(lead.get("city", "Unknown") for lead in leads)
        status_counter = Counter(lead.get("status", "Unknown").lower() for lead in leads)
        total_leads = len(leads)
        return {
            "message": "📊 Summary of all leads",
            "data": {
                "total_leads": total_leads,
                "status_distribution": dict(status_counter),
                "city_distribution": dict(city_counter)
            }
        }

    # CASE 5: Interested leads
    if "interested" in query_lower:
        interested = [lead for lead in leads if lead.get("status", "unknown").lower() == "interested"]
        return {
            "message": f"Found {len(interested)} interested lead(s).",
            "leads": interested
        }
    # CASE 6: City with highest converted leads
    if "highest converted" in query_lower or "most converted" in query_lower:
        converted_city_counter = Counter(
            lead.get("city", "Unknown") for lead in leads if lead.get("status", "unknown").lower() == "converted"
        )
        if not converted_city_counter:
            return {"message": "No converted leads found."}
        top_city, top_count = converted_city_counter.most_common(1)[0]
        return {
            "message": f"{top_city} has the highest number of converted leads ({top_count})."
        }

    # CASE 6: Leads from a specific city (improved detection)
    city_match = re.search(r"leads?\s+(from|in)\s+([a-zA-Z\s]+)", query_lower)
    if city_match:
        city_name = city_match.group(2).strip().title()
        matched_leads = [lead for lead in leads if lead.get("city", "").title() == city_name]
        if matched_leads:
            return {
                "message": f"Found {len(matched_leads)} lead(s) from {city_name}",
                "data": matched_leads
            }
        else:
            return {
                "message": f"No leads found from {city_name}"
            }

    # CASE 7: Fallback
    return {
        "message": "I didn't understand that. Try asking something like:\n"
                "- 'Show leads from Noida'\n"
                "- 'How many leads are pending?'\n"
                "- 'Summary of all leads'\n"
                "- 'Top cities with most leads'\n"
                "- 'Count of leads by city'\n"
    }