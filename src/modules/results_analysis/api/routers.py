from typing import List

from fastapi import APIRouter

from src.modules.results_analysis.api.test_reports.test_reports_router import router as test_reports_router

routers: List[APIRouter] = [
    test_reports_router
]
