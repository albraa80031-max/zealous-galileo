"""
Legal Agent - العامل القانوني الرئيسي
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class LegalAgent:
    """
    العامل القانوني - يدير البيانات القانونية ويزامنها مع GitHub
    """

    def __init__(self, config_path: str = "config.json"):
        """
        تهيئة العامل القانوني

        Args:
            config_path: مسار ملف الإعدادات
        """
        self.config_path = Path(config_path)
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)

        self.config = self._load_config()
        self.cases = []
        self.contracts = []
        self.documents = []

        logger.info("تم تهيئة العامل القانوني بنجاح")

    def _load_config(self) -> Dict:
        """تحميل الإعدادات"""
        if self.config_path.exists():
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "github_token": "",
            "repo_owner": "",
            "repo_name": "",
            "auto_sync": True,
            "sync_interval": 3600
        }

    def add_case(self, case_id: str, title: str, description: str, status: str = "active") -> Dict:
        """إضافة قضية جديدة"""
        case = {
            "id": case_id,
            "title": title,
            "description": description,
            "status": status,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "documents": []
        }
        self.cases.append(case)
        logger.info(f"تمت إضافة القضية: {case_id}")
        return case

    def add_contract(self, contract_id: str, title: str, content: str,
                    parties: List[str], status: str = "draft") -> Dict:
        """إضافة عقد جديد"""
        contract = {
            "id": contract_id,
            "title": title,
            "content": content,
            "parties": parties,
            "status": status,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        self.contracts.append(contract)
        logger.info(f"تمت إضافة العقد: {contract_id}")
        return contract

    def add_document(self, doc_id: str, title: str, content: str, doc_type: str) -> Dict:
        """إضافة وثيقة جديدة"""
        doc = {
            "id": doc_id,
            "title": title,
            "content": content,
            "type": doc_type,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        self.documents.append(doc)
        logger.info(f"تمت إضافة الوثيقة: {doc_id}")
        return doc

    def get_case(self, case_id: str) -> Optional[Dict]:
        """الحصول على تفاصيل قضية"""
        for case in self.cases:
            if case["id"] == case_id:
                return case
        return None

    def update_case(self, case_id: str, **kwargs) -> Optional[Dict]:
        """تحديث بيانات القضية"""
        for case in self.cases:
            if case["id"] == case_id:
                case.update({**kwargs, "updated_at": datetime.now().isoformat()})
                logger.info(f"تم تحديث القضية: {case_id}")
                return case
        return None

    def get_all_cases(self) -> List[Dict]:
        """الحصول على جميع القضايا"""
        return self.cases

    def get_all_contracts(self) -> List[Dict]:
        """الحصول على جميع العقود"""
        return self.contracts

    def get_all_documents(self) -> List[Dict]:
        """الحصول على جميع الوثائق"""
        return self.documents

    def export_to_json(self, output_path: str = "data/export.json") -> bool:
        """تصدير البيانات إلى ملف JSON"""
        try:
            data = {
                "cases": self.cases,
                "contracts": self.contracts,
                "documents": self.documents,
                "exported_at": datetime.now().isoformat()
            }
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"تم تصدير البيانات إلى: {output_path}")
            return True
        except Exception as e:
            logger.error(f"خطأ في التصدير: {e}")
            return False

    def import_from_json(self, input_path: str) -> bool:
        """استيراد البيانات من ملف JSON"""
        try:
            with open(input_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.cases = data.get("cases", [])
            self.contracts = data.get("contracts", [])
            self.documents = data.get("documents", [])
            logger.info(f"تم استيراد البيانات من: {input_path}")
            return True
        except Exception as e:
            logger.error(f"خطأ في الاستيراد: {e}")
            return False

    def get_summary(self) -> Dict:
        """الحصول على ملخص البيانات"""
        return {
            "total_cases": len(self.cases),
            "total_contracts": len(self.contracts),
            "total_documents": len(self.documents),
            "active_cases": len([c for c in self.cases if c["status"] == "active"]),
            "draft_contracts": len([c for c in self.contracts if c["status"] == "draft"])
        }
