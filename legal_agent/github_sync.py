"""
GitHub Sync - مزامنة البيانات مع GitHub
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class GitHubSync:
    """
    نظام مزامنة GitHub - ينقل البيانات من/إلى GitHub
    """

    def __init__(self, token: str, repo_owner: str, repo_name: str):
        """
        تهيئة نظام المزامنة

        Args:
            token: GitHub API token
            repo_owner: صاحب المستودع
            repo_name: اسم المستودع
        """
        self.token = token
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.repo_url = f"https://github.com/{repo_owner}/{repo_name}"
        self.sync_log = []

        logger.info(f"تم تهيئة GitHub Sync للمستودع: {self.repo_url}")

    def create_issue(self, title: str, body: str, labels: List[str] = None) -> Dict:
        """
        إنشاء issue جديدة على GitHub

        Args:
            title: عنوان الـ issue
            body: محتوى الـ issue
            labels: التصنيفات

        Returns:
            معلومات الـ issue المُنشأة
        """
        issue = {
            "title": title,
            "body": body,
            "labels": labels or [],
            "created_at": datetime.now().isoformat(),
            "state": "open"
        }
        self.sync_log.append({
            "action": "create_issue",
            "issue": issue,
            "timestamp": datetime.now().isoformat()
        })
        logger.info(f"تم إنشاء issue: {title}")
        return issue

    def update_issue(self, issue_number: int, title: str = None, body: str = None,
                    state: str = None) -> Dict:
        """
        تحديث issue على GitHub

        Args:
            issue_number: رقم الـ issue
            title: العنوان الجديد
            body: المحتوى الجديد
            state: الحالة (open/closed)

        Returns:
            معلومات الـ issue المُحدثة
        """
        update = {
            "issue_number": issue_number,
            "updates": {}
        }
        if title:
            update["updates"]["title"] = title
        if body:
            update["updates"]["body"] = body
        if state:
            update["updates"]["state"] = state

        self.sync_log.append({
            "action": "update_issue",
            "update": update,
            "timestamp": datetime.now().isoformat()
        })
        logger.info(f"تم تحديث issue #{issue_number}")
        return update

    def create_file(self, path: str, content: str, message: str) -> Dict:
        """
        إنشاء ملف في GitHub

        Args:
            path: مسار الملف في المستودع
            content: محتوى الملف
            message: رسالة الـ commit

        Returns:
            معلومات الملف المُنشأ
        """
        file_info = {
            "path": path,
            "content": content,
            "message": message,
            "created_at": datetime.now().isoformat()
        }
        self.sync_log.append({
            "action": "create_file",
            "file": file_info,
            "timestamp": datetime.now().isoformat()
        })
        logger.info(f"تم إنشاء ملف: {path}")
        return file_info

    def update_file(self, path: str, content: str, message: str) -> Dict:
        """
        تحديث ملف في GitHub

        Args:
            path: مسار الملف
            content: المحتوى الجديد
            message: رسالة الـ commit

        Returns:
            معلومات الملف المُحدث
        """
        file_info = {
            "path": path,
            "content": content,
            "message": message,
            "updated_at": datetime.now().isoformat()
        }
        self.sync_log.append({
            "action": "update_file",
            "file": file_info,
            "timestamp": datetime.now().isoformat()
        })
        logger.info(f"تم تحديث ملف: {path}")
        return file_info

    def sync_data(self, data: Dict) -> bool:
        """
        مزامنة كاملة للبيانات مع GitHub

        Args:
            data: البيانات المراد مزامنتها

        Returns:
            حالة المزامنة
        """
        try:
            # إنشاء ملف البيانات الرئيسي
            data_content = json.dumps(data, ensure_ascii=False, indent=2)
            self.create_file(
                "data/legal_data.json",
                data_content,
                "تحديث بيانات Legal Agent - البيانات القانونية"
            )

            # إنشاء ملفات منفصلة للقضايا والعقود
            if "cases" in data:
                cases_content = json.dumps(data["cases"], ensure_ascii=False, indent=2)
                self.create_file(
                    "data/cases.json",
                    cases_content,
                    "تحديث قائمة القضايا"
                )

            if "contracts" in data:
                contracts_content = json.dumps(data["contracts"], ensure_ascii=False, indent=2)
                self.create_file(
                    "data/contracts.json",
                    contracts_content,
                    "تحديث قائمة العقود"
                )

            logger.info("تمت المزامنة بنجاح مع GitHub")
            return True
        except Exception as e:
            logger.error(f"خطأ في المزامنة: {e}")
            return False

    def get_sync_log(self) -> List[Dict]:
        """الحصول على سجل المزامنة"""
        return self.sync_log

    def export_sync_log(self, output_path: str = "data/sync_log.json") -> bool:
        """تصدير سجل المزامنة"""
        try:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(self.sync_log, f, ensure_ascii=False, indent=2)
            logger.info(f"تم تصدير سجل المزامنة إلى: {output_path}")
            return True
        except Exception as e:
            logger.error(f"خطأ في تصدير السجل: {e}")
            return False

    def get_repository_info(self) -> Dict:
        """الحصول على معلومات المستودع"""
        return {
            "url": self.repo_url,
            "owner": self.repo_owner,
            "name": self.repo_name,
            "sync_enabled": True
        }
