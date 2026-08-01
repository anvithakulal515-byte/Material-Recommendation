from fastapi import APIRouter, HTTPException
from app.models.material import RecommendRequest, ProjectRecord
from app.services.ai_service import generate_recommendation
from app.services.project_service import project_service

router = APIRouter(prefix="/api", tags=["Recommendation"])

@router.post("/recommend", response_model=ProjectRecord)
def recommend_materials(req: RecommendRequest):
    if not req.project_name or len(req.project_name.strip()) < 2:
        raise HTTPException(status_code=400, detail="Please provide a valid engineering project name.")
    
    report = generate_recommendation(
        project_name=req.project_name,
        environment=req.environment or "Standard Industrial",
        budget_level=req.budget_level or "Standard"
    )
    
    saved_record = project_service.save_project(report)
    return saved_record
