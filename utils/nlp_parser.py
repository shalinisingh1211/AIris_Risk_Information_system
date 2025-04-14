import re

def extract_fields_and_projects(query, projects):
    # Normalize text
    query_lower = query.lower()
    
    # Define known fields
    known_fields = [
        "start_date", "end_date", "status", "budget",
        "risk_score", "schedule_risk", "budget_risk",
        "resource_risk", "market_risk", "technical_risk"
    ]

    # Extract matching project names
    matched_projects = []
    for project in projects:
        if project["name"].lower() in query_lower:
            matched_projects.append(project["id"])

    # Extract matching fields
    matched_fields = []
    for field in known_fields:
        if field.replace("_", " ") in query_lower or field in query_lower:
            matched_fields.append(field)

    return {
        "projects": matched_projects,
        "fields": matched_fields
    }
