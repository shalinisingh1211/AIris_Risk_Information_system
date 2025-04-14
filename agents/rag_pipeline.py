# agents/rag_pipeline.py

import json
from utils.project_database import Session, Project, log_changelog

def run_rag_pipeline(json_path, doc_path=None):
    """
    Ingest a JSON metadata file and optional document file.
    This function triggers the project data insertion pipeline.
    """
    with open(json_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    insert_project_metadata(metadata)

def insert_project_metadata(metadata):
    """
    Insert or update a project in the database.
    Logs old project data into the changelog before updating.
    """
    session = Session()
    project_id = metadata["id"]

    # Check if the project already exists
    existing_project = session.query(Project).filter(Project.id == project_id).first()

    if existing_project:
        # Save current version to changelog before updating
        old_data = existing_project.to_dict()
        log_changelog(project_id, old_data)

        # Update fields with new metadata
        for field, value in metadata.items():
            if hasattr(existing_project, field):
                setattr(existing_project, field, value)

    else:
        # Create and add new project
        new_project = Project(**metadata)
        session.add(new_project)

    session.commit()
    session.close()
