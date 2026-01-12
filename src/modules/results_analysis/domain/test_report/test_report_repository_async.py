from abc import ABC, abstractmethod

from src.modules.results_analysis.domain.test_report.test_report import TestReport


class TestReportRepositoryAsync(ABC):
    @abstractmethod
    async def add_test_report(self, test_report: TestReport):
        ...

    @abstractmethod
    async def delete_test_report_by_test_session_id(self, test_session_id):
        ...
