from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class MaterialItem(BaseModel):
    item_name: str = Field(..., description="Name of the material or component")
    grade: str = Field(..., description="Engineering grade, standard or specification")
    dimensions: str = Field(..., description="Dimensions, thickness, diameter, or sizing")
    quantity: str = Field(..., description="Quantity required with unit")
    purpose: str = Field(..., description="Specific purpose or functional role in the project")
    alternatives: List[str] = Field(default_factory=list, description="Alternative acceptable materials")
    low_budget_option: Optional[str] = Field("", description="Ultra low-budget cost effective substitute")
    unit_cost_inr: float = Field(0.0, description="Exact estimated unit cost in Indian Rupees (INR ₹)")
    total_cost_inr: float = Field(0.0, description="Exact total cost for this item in Indian Rupees (INR ₹)")
    unit_cost_usd: float = Field(0.0, description="Exact estimated unit cost in USD")
    total_cost_usd: float = Field(0.0, description="Exact total cost for this item in USD")
    cost_note: Optional[str] = Field("", description="Pricing basis or supplier estimation note")

class CostOptimizationTip(BaseModel):
    category: str
    tip: str
    estimated_savings_inr: float

class RecommendationReport(BaseModel):
    project_name: str
    project_summary: str
    category: str
    operating_environment: Optional[str] = "General Workshop / Industrial"
    materials: List[MaterialItem]
    tools_and_equipment: List[str]
    manufacturing_processes: List[str]
    safety_precautions: List[str]
    assembly_procedure: List[str]
    raw_material_subtotal_inr: float = 0.0
    estimated_machining_and_labor_inr: float = 0.0
    total_estimated_cost_inr: float = 0.0
    raw_material_subtotal_usd: float = 0.0
    estimated_machining_and_labor_usd: float = 0.0
    total_estimated_cost_usd: float = 0.0
    cost_saving_strategies: List[CostOptimizationTip] = Field(default_factory=list)
    key_design_considerations: List[str]

class RecommendRequest(BaseModel):
    project_name: str
    environment: Optional[str] = "Industrial / Standard Workshop"
    budget_level: Optional[str] = "Standard (Optimal Balance)"

class ProjectRecord(BaseModel):
    id: str
    project_name: str
    category: str
    created_at: str
    report: RecommendationReport

class ChatRequest(BaseModel):
    project_name: str
    project_context: Optional[dict] = None
    question: str
    chat_history: Optional[List[dict]] = []

class ChatResponse(BaseModel):
    answer: str
    suggested_followups: List[str] = []
