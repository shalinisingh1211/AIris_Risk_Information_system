from utils.pg_database import Session, Project

def save_project_data(parsed_data: dict):
    session = Session()
    project = Project(**parsed_data)
    session.add(project)
    session.commit()