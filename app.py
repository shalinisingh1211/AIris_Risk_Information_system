# app.py
import streamlit as st
import os
import pandas as pd
from components.chat_interface import create_chat_interface
from components.dashboard import create_dashboard
from utils.project_database import initialize_database, get_projects, get_project_changelog_parsed
from agents.rag_pipeline import run_rag_pipeline

# Configure Streamlit page
st.set_page_config(page_title="AI Project Risk Management", layout="wide")
initialize_database()

# Sidebar UI
st.sidebar.title("TEAM S-QUAD")
st.sidebar.image(r"C:\Users\shrey\Downloads\donedone\asset\ChatGPT Image Apr 14, 2025, 12_47_41 AM.png", width=250)


# Upload project document + metadata
with st.sidebar.expander("📄 Upload Project Document & Metadata"):
    uploaded_doc = st.file_uploader("Upload Project Document (TXT, PDF, DOCX)", type=["pdf", "docx", "txt"])
    uploaded_meta = st.file_uploader("Upload Project Metadata (JSON)", type=["json"])

    if uploaded_meta and st.button("Run AI Agents"):
        with st.spinner("Analyzing files..."):
            os.makedirs("uploads", exist_ok=True)
            doc_path = None
            if uploaded_doc:
                doc_path = os.path.join("uploads", uploaded_doc.name)
                with open(doc_path, "wb") as f:
                    f.write(uploaded_doc.read())

            meta_path = os.path.join("uploads", uploaded_meta.name)
            with open(meta_path, "wb") as f:
                f.write(uploaded_meta.read())

            run_rag_pipeline(json_path=meta_path, doc_path=doc_path)
            st.success("✅ Document processed and project stored!")

# Navigation tabs
page = st.sidebar.radio("Navigation", ["Dashboard", "Chat Interface", "Project Details", "Settings"])

if page == "Dashboard":
    st.title("📊 Project Risk Dashboard")
    projects = get_projects()
    create_dashboard(projects)

elif page == "Chat Interface":
    st.title("🤖 Risk Management Assistant")
    create_chat_interface()

elif page == "Project Details":
    st.title("📁 Project Details")
    projects = get_projects()
    if not projects:
        st.warning("No projects found.")
    else:
        selected = st.selectbox("Choose a project", [p["name"] for p in projects])
        project = next((p for p in projects if p["name"] == selected), None)
        if project:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Project Info")
                for k in ["id", "name", "description", "status", "start_date", "end_date", "budget"]:
                    st.write(f"**{k.replace('_', ' ').title()}:** {project.get(k)}")

            with col2:
                st.subheader("Risk Metrics")
                st.metric("Overall Risk", f"{project.get('risk_score', 0)}/10", delta=project.get("risk_delta", 0))
                for k in ["schedule_risk", "budget_risk", "resource_risk", "market_risk", "technical_risk"]:
                    st.write(f"**{k.replace('_', ' ').title()}:** {project.get(k, 0)}/10")

            # Changelog viewer (Improved UI)
            st.subheader("🕘 Version History / Changelog")
            changelog = get_project_changelog_parsed(project["id"])
            if changelog:
                for idx, entry in enumerate(changelog):
                    with st.expander(f"🔁 Version {len(changelog)-idx} — {entry['timestamp']}"):
                        st.markdown(f"**Status:** {entry.get('status', 'N/A')}")
                        st.markdown(f"**Budget:** ${entry.get('budget', 'N/A'):,}")
                        st.markdown(f"**Start - End:** {entry.get('start_date', 'N/A')} to {entry.get('end_date', 'N/A')}")
                        st.markdown(f"**Risk Score:** {entry.get('risk_score', 'N/A')} | Risk Delta: {entry.get('risk_delta', 'N/A')}")

                        risks = {
                            "Schedule Risk": entry.get("schedule_risk", "N/A"),
                            "Budget Risk": entry.get("budget_risk", "N/A"),
                            "Resource Risk": entry.get("resource_risk", "N/A"),
                            "Market Risk": entry.get("market_risk", "N/A"),
                            "Technical Risk": entry.get("technical_risk", "N/A")
                        }
                        st.table(pd.DataFrame(risks.items(), columns=["Risk Type", "Score"]))

                        factors = entry.get("risk_factors", [])
                        if factors:
                            st.markdown("### 🧠 Risk Factors")
                            for factor in factors:
                                st.markdown(f"- **{factor['name']}** ({factor['category']})")
                                st.markdown(f"  - Description: {factor['description']}")
                                st.markdown(f"  - Impact: {factor['impact']} | Likelihood: {factor['likelihood']}")
                                st.markdown(f"  - Mitigation: {factor['mitigation']}")
                        else:
                            st.markdown("No risk factors recorded.")

                        history = entry.get("risk_history", {})
                        if history:
                            st.markdown("### 📈 Historical Risk Timeline")
                            hist_df = pd.DataFrame(list(history.items()), columns=["Date", "Risk Score"])
                            st.line_chart(hist_df.set_index("Date"))
            else:
                st.info("No changelog available yet for this project.")

elif page == "Settings":
    st.title("⚙️ Settings")
    st.info("Settings coming soon.")
