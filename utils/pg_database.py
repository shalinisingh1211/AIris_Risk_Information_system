import os
from datetime import datetime
from sqlalchemy import (
    Column, Float, String, Integer, ForeignKey,
    JSON, DateTime, create_engine
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# --- Database Setup ---
DATABASE_URL = os.environ.get("DATABASE_URL") or "sqlite:///data/project_risk.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# --- Models ---
class Project(Base):
    __tablename__ = 'projects'
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
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
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    risk_factors = relationship("RiskFactor", back_populates="project", cascade="all, delete-orphan")
    risk_history = relationship("RiskHistory", back_populates="project", cascade="all, delete-orphan")
    risk_reports = relationship("RiskReport", back_populates="project", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'status': self.status,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'budget': self.budget,
            'spent': self.spent,
            'team_size': self.team_size,
            'risk_score': self.risk_score,
            'risk_delta': self.risk_delta,
            'schedule_risk': self.schedule_risk,
            'budget_risk': self.budget_risk,
            'resource_risk': self.resource_risk,
            'market_risk': self.market_risk,
            'technical_risk': self.technical_risk,
            'risk_factors': [rf.to_dict() for rf in self.risk_factors],
            'risk_history': [rh.to_dict() for rh in self.risk_history],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class RiskFactor(Base):
    __tablename__ = 'risk_factors'
    id = Column(Integer, primary_key=True)
    project_id = Column(String, ForeignKey("projects.id"))
    name = Column(String)
    description = Column(String)
    category = Column(String)
    impact = Column(Float)
    likelihood = Column(Float)
    mitigation = Column(String)
    project = relationship("Project", back_populates="risk_factors")

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'impact': self.impact,
            'likelihood': self.likelihood,
            'mitigation': self.mitigation
        }

class RiskHistory(Base):
    __tablename__ = 'risk_history'
    id = Column(Integer, primary_key=True)
    project_id = Column(String, ForeignKey("projects.id"))
    date = Column(String)
    risk_score = Column(Float)
    project = relationship("Project", back_populates="risk_history")

    def to_dict(self):
        return {
            'date': self.date,
            'risk_score': self.risk_score
        }

class RiskReport(Base):
    __tablename__ = 'risk_reports'
    id = Column(String, primary_key=True)
    project_id = Column(String, ForeignKey("projects.id"))
    date = Column(String)
    risk_score = Column(Float)
    content = Column(JSON)
    project = relationship("Project", back_populates="risk_reports")

    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'date': self.date,
            'risk_score': self.risk_score,
            'content': self.content
        }

class ProjectVersion(Base):
    __tablename__ = 'project_versions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    version_data = Column(JSON)

    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'timestamp': self.timestamp.isoformat(),
            'version_data': self.version_data
        }

# --- Initialization and Utility Methods ---

def initialize_database():
    """Create all tables in the database."""
    Base.metadata.create_all(engine)

def get_projects():
    """Returns all projects as dicts."""
    session = Session()
    projects = session.query(Project).all()
    result = [project.to_dict() for project in projects]
    session.close()
    return result

def get_project(project_id):
    """Returns a specific project by ID."""
    session = Session()
    project = session.query(Project).filter(Project.id == project_id).first()
    result = project.to_dict() if project else None
    session.close()
    return result
