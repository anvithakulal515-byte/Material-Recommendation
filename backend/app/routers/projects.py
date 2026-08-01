from fastapi import APIRouter, HTTPException
from typing import List
from app.models.material import ProjectRecord
from app.services.project_service import project_service

router = APIRouter(prefix="/api/projects", tags=["Projects History"])

@router.get("", response_model=List[ProjectRecord])
def list_projects():
    return project_service.get_all_projects()

@router.get("/{project_id}", response_model=ProjectRecord)
def get_project(project_id: str):
    record = project_service.get_project_by_id(project_id)
    if not record:
        raise HTTPException(status_code=404, detail="Project record not found")
    return record

@router.delete("/{project_id}")
def delete_project(project_id: str):
    success = project_service.delete_project(project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project record not found")
    return {"status": "success", "message": f"Project {project_id} deleted"}
