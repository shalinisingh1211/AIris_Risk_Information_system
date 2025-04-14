import streamlit as st
import re
import pandas as pd
from langchain_community.llms import HuggingFaceHub
from agents.rag_pipeline import run_rag_pipeline
from utils.project_database import get_projects, get_project, get_project_changelog_parsed
from utils.vector_store import search_risks
from utils.nlp_parser import extract_fields_and_projects

# Initialize LLM
llm = HuggingFaceHub(
    repo_id="tiiuae/falcon-7b-instruct",
    model_kwargs={"temperature": 0.5, "max_new_tokens": 512}
)

def clean_llm_output(response: str) -> str:
    response = re.sub(r"(?i)project:.*?highest risk:.*?suggest.*?mitigation.*?", "", response, count=1)
    return response.strip().lstrip(":").strip()

def create_chat_interface():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "👋 Hello! I'm your AI Project Risk Management Assistant. You can upload documents or ask questions below."}
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    uploaded_file = st.file_uploader("📄 Upload a project document (PDF, TXT, DOCX)", type=["pdf", "txt", "docx"])
    if uploaded_file is not None:
        with st.spinner("Processing document and extracting project data..."):
            result = run_rag_pipeline(uploaded_file)
            if result.get("success"):
                st.success("✅ Document processed and new project inserted successfully.")
                st.session_state.messages.append({"role": "assistant", "content": "✅ Your file was successfully processed and stored."})
            else:
                st.error("❌ Failed to process document.")
                st.session_state.messages.append({"role": "assistant", "content": "⚠️ Failed to process the uploaded file."})

    if prompt := st.chat_input("Ask a question about project risks..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = process_query(prompt)
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})


# ----------------- QUERY ROUTER ----------------- #
def process_query(query):
    query_lower = query.lower()
    if "compare" in query_lower and "project" in query_lower:
        return handle_comparison_query(query)
    elif "status" in query_lower and "project" in query_lower:
        return handle_project_status_query(query)
    elif "report" in query_lower or "summary" in query_lower:
        return handle_risk_report_query(query)
    elif "mitigation" in query_lower or "strategies" in query_lower or "solve" in query_lower:
        return handle_project_risks_query(query)
    elif "risk" in query_lower and "project" in query_lower:
        return handle_project_risks_query(query)
    else:
        return handle_general_query(query)

# ----------------- COMPARISON QUERY ----------------- #
def handle_comparison_query(query):
    projects = get_projects()
    extracted = extract_fields_and_projects(query, projects)

    if not extracted.get("projects"):
        return "⚠️ I couldn't identify the project in your question."

    project_id = extracted["projects"][0]
    field = extracted["fields"][0] if extracted["fields"] else "risk_score"
    field_title = field.replace("_", " ").title()

    latest = get_project(project_id)
    history = get_project_changelog_parsed(project_id)

    comparison_data = []
    for idx, version in enumerate(reversed(history), start=1):
        value = version.get(field, "N/A")
        comparison_data.append({
            "Version": f"Old v{idx}",
            "Timestamp": version.get("timestamp", "N/A"),
            field_title: value
        })

    comparison_data.append({
        "Version": "Current",
        "Timestamp": latest.get("updated_at", "Now"),
        field_title: latest.get(field, "N/A")
    })

    df = pd.DataFrame(comparison_data)
    st.write(f"📊 Comparison of **{field_title}** for project **{project_id}**:")
    st.table(df)

    return f"✅ Displayed comparison table for **{field_title}** of project **{project_id}**."


# ----------------- RISK QUERY ----------------- #
def handle_project_risks_query(query):
    projects = get_projects()
    extracted = extract_fields_and_projects(query, projects)
    if not extracted.get("projects"):
        return "⚠️ I couldn't identify the project in your question."
    
    project = get_project(extracted["projects"][0])
    risks = {
        "Schedule Risk": project["schedule_risk"],
        "Budget Risk": project["budget_risk"],
        "Resource Risk": project["resource_risk"],
        "Market Risk": project["market_risk"],
        "Technical Risk": project["technical_risk"]
    }

    if extracted["fields"]:
        field = extracted["fields"][0]
        field_title = field.replace("_", " ").title()
        if field in project:
            return f"📌 **{field_title}** for project **{project['name']}**: **{project[field]}/10**"

    highest = max(risks, key=risks.get)
    prompt = (
        f"The project is about: {project['description']} "
        f"What is one concise mitigation strategy for the highest risk in this project? "
        f"Risk Type: {highest}, Risk Score: {risks[highest]}"
    )
    response = llm(prompt)
    return (
        f"📊 Risk Summary for Project **{project['name']}**: " +
        " ".join([f"{k}: {v}/10" for k, v in risks.items()]) +
        f"\n\n💡 Highest Risk: {highest} ({risks[highest]}/10)\n\n" +
        f"💡 Mitigation Suggestion: {clean_llm_output(response)}"
    )

# ----------------- GENERAL QUERY ----------------- #
def handle_general_query(query):
    projects = get_projects()
    extracted = extract_fields_and_projects(query, projects)
    if extracted.get("projects"):
        project = get_project(extracted["projects"][0])
        field_map = {
            "start_date": "Start Date",
            "end_date": "End Date",
            "status": "Status",
            "budget": "Budget",
            "risk_score": "Overall Risk Score",
            "schedule_risk": "Schedule Risk",
            "budget_risk": "Budget Risk",
            "resource_risk": "Resource Risk",
            "market_risk": "Market Risk",
            "technical_risk": "Technical Risk"
        }
        for field in extracted["fields"]:
            if field in project:
                value = project[field]
                label = field_map.get(field, field.replace("_", " ").title())
                return f"📌 **{label}** for project **{project['name']}**: **{value}**"
    try:
        return clean_llm_output(llm(query))
    except:
        return "⚠️ Sorry, I couldn't process your request."

# ----------------- PLACEHOLDER HANDLERS ----------------- #
def handle_project_status_query(query):
    return "📌 Project status functionality coming soon."

def handle_risk_report_query(query):
    return "📝 Risk report generation is under development."

def handle_risk_trend_query(query):
    return "📈 Risk trend analysis module will be available in the next update."
