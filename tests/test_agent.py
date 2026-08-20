"""
اختبارات وحدة Legal Agent
"""

import pytest
import json
from pathlib import Path
from legal_agent.agent import LegalAgent


class TestLegalAgent:
    """مجموعة اختبارات العامل القانوني"""

    @pytest.fixture
    def agent(self):
        """إنشاء عامل قانوني للاختبار"""
        return LegalAgent()

    def test_agent_initialization(self, agent):
        """اختبار تهيئة العامل"""
        assert agent is not None
        assert agent.data_dir.exists()
        assert isinstance(agent.cases, list)
        assert isinstance(agent.contracts, list)

    def test_add_case(self, agent):
        """اختبار إضافة قضية"""
        case = agent.add_case(
            "CASE001",
            "قضية عقد موظف",
            "نزاع حول شروط العقد"
        )
        assert case["id"] == "CASE001"
        assert case["title"] == "قضية عقد موظف"
        assert case["status"] == "active"
        assert len(agent.cases) == 1

    def test_add_contract(self, agent):
        """اختبار إضافة عقد"""
        contract = agent.add_contract(
            "CONTRACT001",
            "عقد عمل",
            "هذا عقد عمل بين الطرفين",
            ["الشركة", "الموظف"]
        )
        assert contract["id"] == "CONTRACT001"
        assert contract["title"] == "عقد عمل"
        assert len(contract["parties"]) == 2
        assert len(agent.contracts) == 1

    def test_add_document(self, agent):
        """اختبار إضافة وثيقة"""
        doc = agent.add_document(
            "DOC001",
            "تقرير قانوني",
            "هذا تقرير قانوني شامل",
            "report"
        )
        assert doc["id"] == "DOC001"
        assert doc["type"] == "report"
        assert len(agent.documents) == 1

    def test_get_case(self, agent):
        """اختبار الحصول على قضية"""
        agent.add_case("CASE002", "قضية جديدة", "وصف القضية")
        case = agent.get_case("CASE002")
        assert case is not None
        assert case["title"] == "قضية جديدة"

    def test_update_case(self, agent):
        """اختبار تحديث قضية"""
        agent.add_case("CASE003", "قضية قديمة", "وصف")
        updated = agent.update_case("CASE003", status="closed", title="قضية محسومة")
        assert updated["status"] == "closed"
        assert updated["title"] == "قضية محسومة"

    def test_get_all_cases(self, agent):
        """اختبار الحصول على جميع القضايا"""
        agent.add_case("CASE004", "قضية 1", "وصف 1")
        agent.add_case("CASE005", "قضية 2", "وصف 2")
        cases = agent.get_all_cases()
        assert len(cases) == 2

    def test_export_to_json(self, agent, tmp_path):
        """اختبار تصدير البيانات"""
        agent.add_case("CASE006", "قضية للتصدير", "وصف")
        output_file = str(tmp_path / "export.json")
        result = agent.export_to_json(output_file)
        assert result is True
        assert Path(output_file).exists()
        with open(output_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert len(data["cases"]) == 1

    def test_get_summary(self, agent):
        """اختبار الحصول على ملخص"""
        agent.add_case("CASE007", "قضية", "وصف")
        agent.add_contract("CONTRACT002", "عقد", "محتوى", ["طرف1", "طرف2"])
        summary = agent.get_summary()
        assert summary["total_cases"] == 1
        assert summary["total_contracts"] == 1
        assert summary["active_cases"] == 1
