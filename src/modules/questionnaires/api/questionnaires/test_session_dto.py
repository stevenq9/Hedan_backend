from dataclasses import dataclass
from typing import List


@dataclass
class TestSessionDto:
    test_id: int
    child_name: str
    child_age: int
    scholar_grade: int
    child_sex: str
    date_time_of_answer: str
    token: str
    isTokenValid: bool


