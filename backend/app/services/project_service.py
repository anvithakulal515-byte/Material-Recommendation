import os
import json
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from app.models.material import RecommendationReport, ProjectRecord
from app.config import settings

# Path for persistent JSON backup store if MongoDB is not running locally
DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "projects_store.json")

class ProjectService:
    def __init__(self):
        self._memory_store: Dict[str, Dict[str, Any]] = {}
        self._load_from_disk()

    def _load_from_disk(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self._memory_store = json.load(f)
            except Exception:
                self._memory_store = {}

    def _save_to_disk(self):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self._memory_store, f, indent=2)
        except Exception:
            pass

    def save_project(self, report: RecommendationReport) -> ProjectRecord:
        proj_id = str(uuid.uuid4())[:8]
        record_dict = {
            "id": proj_id,
            "project_name": report.project_name,
            "category": report.category,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "report": report.model_dump()
        }
        self._memory_store[proj_id] = record_dict
        self._save_to_disk()
        return ProjectRecord(**record_dict)

    def get_all_projects(self) -> List[ProjectRecord]:
        records = list(self._memory_store.values())
        # Sort by creation date descending
        records.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return [ProjectRecord(**r) for r in records]

    def get_project_by_id(self, project_id: str) -> Optional[ProjectRecord]:
        data = self._memory_store.get(project_id)
        if data:
            return ProjectRecord(**data)
        return None

    def delete_project(self, project_id: str) -> bool:
        if project_id in self._memory_store:
            del self._memory_store[project_id]
            self._save_to_disk()
            return True
        return False

project_service = ProjectService()
