from fastapi import APIRouter
from app.models.material import ChatRequest, ChatResponse
from app.services.ai_service import generate_chat_answer

router = APIRouter(prefix="/api", tags=["Engineering Chatbot"])

@router.post("/chat", response_model=ChatResponse)
def engineering_chat(req: ChatRequest):
    result = generate_chat_answer(
        project_name=req.project_name,
        question=req.question,
        report_summary=str(req.project_context or "")
    )
    return ChatResponse(**result)
