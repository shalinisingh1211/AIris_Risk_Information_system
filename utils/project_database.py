import os
import json
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, String, Integer, Float, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data/project_risk.db")

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)

# Project model
class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True)
    name = Column(String)
    description = Column(String)
    status = Column(String)
    start_date = Column(String)
    end_date = Column(String)
    budget = Column(Float)
    spent = Column(Float)
    team_size = Column(Integer)
    risk_score = Column(Float)
    risk_delta = Column(Float)
    schedule_risk = Column(Float)
    budget_risk = Column(Float)
    resource_risk = Column(Float)
    market_risk = Column(Float)
    technical_risk = Column(Float)
    risk_history = Column(JSON)
    risk_factors = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "budget": self.budget,
            "spent": self.spent,
            "team_size": self.team_size,
            "risk_score": self.risk_score,
            "risk_delta": self.risk_delta,
            "schedule_risk": self.schedule_risk,
            "budget_risk": self.budget_risk,
            "resource_risk": self.resource_risk,
            "market_risk": self.market_risk,
            "technical_risk": self.technical_risk,
            "risk_history": self.risk_history or {},
            "risk_factors": self.risk_factors or [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

# Initialization
def initialize_database():
    Base.metadata.create_all(engine)
    _create_changelog_table()

# Fetch all projects
def get_projects():
    session = Session()
    projects = session.query(Project).all()
    result = [project.to_dict() for project in projects]
    session.close()
    return result

# Fetch one project
def get_project(project_id):
    session = Session()
    project = session.query(Project).filter(Project.id == project_id).first()
    result = project.to_dict() if project else None
    session.close()
    return result

# Changelog table creation
def _create_changelog_table():
    conn = sqlite3.connect("data/project_risk.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS changelog (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id TEXT,
            timestamp TEXT,
            content TEXT
        )
    """)
    conn.commit()
    conn.close()

# Log previous state of a project
def log_changelog(project_id, old_data):
    flat = old_data.copy()
    flat["timestamp"] = datetime.now().isoformat()

    conn = sqlite3.connect("data/project_risk.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO changelog (project_id, timestamp, content) VALUES (?, ?, ?)",
        (project_id, flat["timestamp"], json.dumps(flat))
    )
    conn.commit()
    conn.close()

# Get raw changelog entries
def get_project_changelog(project_id):
    conn = sqlite3.connect("data/project_risk.db")
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, content FROM changelog WHERE project_id = ? ORDER BY timestamp DESC", (project_id,))
    results = cursor.fetchall()
    conn.close()
    return [{"timestamp": row[0], "changes": row[1]} for row in results]

# Get parsed versions of changelog entries
def get_project_changelog_parsed(project_id):
    conn = sqlite3.connect("data/project_risk.db")
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, content FROM changelog WHERE project_id = ? ORDER BY timestamp DESC", (project_id,))
    results = cursor.fetchall()
    conn.close()

    parsed_versions = []
    for row in results:
        try:
            parsed_json = json.loads(row[1])
            parsed_json["timestamp"] = row[0]
            parsed_versions.append(parsed_json)
        except json.JSONDecodeError:
            continue
    return parsed_versions

# Risk search placeholder
def search_similar_risks(risk_query):
    keywords = ["payment", "delay", "budget", "resource", "integration"]
    matches = [k for k in keywords if k in risk_query.lower()]
    if not matches:
        return []
    return [{
        "name": "Delayed Payment",
        "description": "Customer payments are delayed beyond the expected schedule.",
        "category": "budget_risk",
        "impact": 8,
        "likelihood": 7,
        "mitigation": "Follow up with clients and include penalty clauses.",
        "match_score": 9.2
    }]