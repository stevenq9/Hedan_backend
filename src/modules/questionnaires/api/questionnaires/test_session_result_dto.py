from dataclasses import dataclass
from typing import List

@dataclass
class ResultTestSessionDto:
    test_id: int
    child_id: int
    child_name: str
    psychologist_cedula: str
    child_age: int
    scholar_grade: int
    child_sex: str
    test_sender: str
    test_reason: str
    date_time_of_answer: str
    answers_set: List[dict]
    test_results: List[dict]
