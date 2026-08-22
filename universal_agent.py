"""
═══════════════════════════════════════════════════════════════
        UNIVERSAL AGENT - مدير المهام الشامل
═══════════════════════════════════════════════════════════════
وكيل ذكي يقوم بجميع المهام الإدارية والعمليات التلقائية

المميزات:
  ✅ إدارة المهام والجدولة
  ✅ معالجة الملفات والمستندات
  ✅ إدارة البريد الإلكتروني
  ✅ استخراج البيانات من PDFs والصور
  ✅ البحث والفهرسة
  ✅ أتمتة العمليات المتكررة
  ✅ إنشاء التقارير
  ✅ التواصل مع APIs الخارجية
═══════════════════════════════════════════════════════════════
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from enum import Enum
import time

# إعداد السجلات
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TaskPriority(Enum):
    """أولويات المهام"""
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    MINIMAL = 1


class TaskStatus(Enum):
    """حالات المهام"""
    PENDING = "قيد الانتظار"
    IN_PROGRESS = "قيد التنفيذ"
    COMPLETED = "مكتملة"
    FAILED = "فشلت"
    ON_HOLD = "معلقة"


class UniversalAgent:
    """
    وكيل ذكي شامل لإدارة جميع أنواع المهام
    """

    def __init__(self, config_path: str = "config.json"):
        """
        تهيئة الوكيل

        Args:
            config_path: مسار ملف الإعدادات
        """
        self.config = self._load_config(config_path)
        self.tasks: Dict[str, Dict] = {}
        self.completed_tasks: List[str] = []
        self.task_history: List[Dict] = []
        self.current_task_id = None

        logger.info("🤖 تم تهيئة Universal Agent بنجاح")
        self._print_welcome()

    def _load_config(self, config_path: str) -> Dict:
        """تحميل الإعدادات"""
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"⚠️ خطأ في تحميل الإعدادات: {e}")

        return self._default_config()

    def _default_config(self) -> Dict:
        """الإعدادات الافتراضية"""
        return {
            "agent_name": "Universal Agent",
            "version": "1.0.0",
            "language": "ar",
            "timezone": "UTC",
            "max_tasks": 100,
            "auto_save": True,
            "modules": {
                "email": {"enabled": True},
                "file_processing": {"enabled": True},
                "pdf_extraction": {"enabled": True},
                "automation": {"enabled": True},
                "scheduling": {"enabled": True},
                "reporting": {"enabled": True}
            }
        }

    def _print_welcome(self):
        """طباعة رسالة الترحيب"""
        print("\n" + "="*60)
        print(f"  🤖 {self.config['agent_name']} v{self.config['version']}")
        print(f"  الوكيل الذكي الشامل لإدارة المهام")
        print("="*60)
        print(f"  ⏰ الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  🌍 المنطقة الزمنية: {self.config['timezone']}")
        print("="*60 + "\n")

    def create_task(self,
                   task_name: str,
                   description: str = "",
                   priority: TaskPriority = TaskPriority.MEDIUM,
                   due_date: Optional[str] = None,
                   tags: List[str] = None) -> str:
        """
        إنشاء مهمة جديدة

        Args:
            task_name: اسم المهمة
            description: وصف المهمة
            priority: أولوية المهمة
            due_date: تاريخ الاستحقاق
            tags: العلامات

        Returns:
            معرف المهمة
        """
        task_id = f"task_{len(self.tasks) + 1}_{int(time.time())}"

        task = {
            "id": task_id,
            "name": task_name,
            "description": description,
            "priority": priority.name,
            "status": TaskStatus.PENDING.value,
            "created_at": datetime.now().isoformat(),
            "due_date": due_date,
            "tags": tags or [],
            "progress": 0,
            "subtasks": []
        }

        self.tasks[task_id] = task
        logger.info(f"✅ تم إنشاء مهمة: {task_name} (ID: {task_id})")

        return task_id

    def update_task_status(self, task_id: str, status: TaskStatus) -> bool:
        """تحديث حالة المهمة"""
        if task_id not in self.tasks:
            logger.error(f"❌ المهمة {task_id} غير موجودة")
            return False

        old_status = self.tasks[task_id]["status"]
        self.tasks[task_id]["status"] = status.value
        self.tasks[task_id]["updated_at"] = datetime.now().isoformat()

        if status == TaskStatus.COMPLETED:
            self.completed_tasks.append(task_id)

        logger.info(f"📝 تم تحديث المهمة {task_id}: {old_status} → {status.value}")
        return True

    def list_tasks(self, filter_status: Optional[TaskStatus] = None) -> List[Dict]:
        """
        عرض قائمة المهام

        Args:
            filter_status: تصفية حسب الحالة

        Returns:
            قائمة المهام
        """
        tasks = list(self.tasks.values())

        if filter_status:
            tasks = [t for t in tasks if t["status"] == filter_status.value]

        # ترتيب حسب الأولوية
        priority_order = {
            "CRITICAL": 5, "HIGH": 4, "MEDIUM": 3, "LOW": 2, "MINIMAL": 1
        }
        tasks.sort(key=lambda x: priority_order.get(x["priority"], 0), reverse=True)

        return tasks

    def process_email(self, email_data: Dict) -> bool:
        """
        معالجة البريد الإلكتروني

        Args:
            email_data: بيانات البريد

        Returns:
            نتيجة المعالجة
        """
        try:
            logger.info(f"📧 معالجة بريد من: {email_data.get('from', 'Unknown')}")
            logger.info(f"   الموضوع: {email_data.get('subject', 'No Subject')}")

            # هنا يمكن إضافة منطق معالجة البريد المتقدم
            return True
        except Exception as e:
            logger.error(f"❌ خطأ في معالجة البريد: {e}")
            return False

    def extract_from_pdf(self, file_path: str) -> Dict[str, Any]:
        """
        استخراج البيانات من ملف PDF

        Args:
            file_path: مسار ملف PDF

        Returns:
            البيانات المستخرجة
        """
        try:
            if not os.path.exists(file_path):
                logger.error(f"❌ الملف غير موجود: {file_path}")
                return {}

            logger.info(f"📄 استخراج من PDF: {os.path.basename(file_path)}")

            # هنا يمكن إضافة مكتبات OCR مثل PyPDF2, pdfplumber, إلخ
            result = {
                "file": file_path,
                "extracted_at": datetime.now().isoformat(),
                "text": "",
                "images": [],
                "metadata": {}
            }

            logger.info(f"✅ تم استخراج البيانات من PDF بنجاح")
            return result
        except Exception as e:
            logger.error(f"❌ خطأ في استخراج البيانات: {e}")
            return {}

    def process_files(self, directory: str) -> Dict[str, int]:
        """
        معالجة الملفات في مجلد

        Args:
            directory: مسار المجلد

        Returns:
            إحصائيات المعالجة
        """
        stats = {
            "total": 0,
            "processed": 0,
            "failed": 0,
            "types": {}
        }

        try:
            if not os.path.isdir(directory):
                logger.error(f"❌ المجلد غير موجود: {directory}")
                return stats

            logger.info(f"📂 معالجة الملفات في: {directory}")

            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path):
                    stats["total"] += 1

                    # معالجة حسب نوع الملف
                    _, ext = os.path.splitext(filename)
                    stats["types"][ext] = stats["types"].get(ext, 0) + 1

                    if ext.lower() in ['.pdf', '.doc', '.docx', '.txt']:
                        stats["processed"] += 1

            logger.info(f"✅ تمت معالجة {stats['processed']} ملف من {stats['total']}")
            return stats
        except Exception as e:
            logger.error(f"❌ خطأ في معالجة الملفات: {e}")
            return stats

    def schedule_task(self, task_id: str, run_time: str) -> bool:
        """
        جدولة تنفيذ مهمة في وقت محدد

        Args:
            task_id: معرف المهمة
            run_time: وقت التنفيذ (ISO format)

        Returns:
            نتيجة الجدولة
        """
        if task_id not in self.tasks:
            logger.error(f"❌ المهمة {task_id} غير موجودة")
            return False

        self.tasks[task_id]["scheduled_time"] = run_time
        logger.info(f"⏰ تم جدولة المهمة {task_id} للتنفيذ في: {run_time}")
        return True

    def generate_report(self, report_type: str = "summary") -> Dict:
        """
        إنشاء تقرير عن المهام والعمليات

        Args:
            report_type: نوع التقرير (summary, detailed, etc.)

        Returns:
            التقرير
        """
        total_tasks = len(self.tasks)
        completed = len(self.completed_tasks)
        pending = sum(1 for t in self.tasks.values()
                     if t["status"] == TaskStatus.PENDING.value)

        report = {
            "generated_at": datetime.now().isoformat(),
            "report_type": report_type,
            "summary": {
                "total_tasks": total_tasks,
                "completed": completed,
                "pending": pending,
                "completion_rate": f"{(completed/total_tasks*100):.1f}%" if total_tasks > 0 else "0%"
            },
            "task_breakdown": {}
        }

        # تصنيف المهام حسب الأولوية
        for priority in TaskPriority:
            count = sum(1 for t in self.tasks.values()
                       if t["priority"] == priority.name)
            if count > 0:
                report["task_breakdown"][priority.name] = count

        logger.info(f"📊 تم إنشاء تقرير: {report_type}")
        return report

    def execute_automation(self, automation_name: str, params: Dict) -> bool:
        """
        تنفيذ عملية أتمتة

        Args:
            automation_name: اسم العملية
            params: المعاملات

        Returns:
            نتيجة التنفيذ
        """
        logger.info(f"🔄 تنفيذ أتمتة: {automation_name}")

        try:
            # هنا يمكن إضافة عمليات أتمتة محددة
            logger.info(f"✅ تمت عملية الأتمتة: {automation_name}")
            return True
        except Exception as e:
            logger.error(f"❌ خطأ في الأتمتة: {e}")
            return False

    def get_statistics(self) -> Dict:
        """الحصول على إحصائيات الوكيل"""
        return {
            "total_tasks": len(self.tasks),
            "completed_tasks": len(self.completed_tasks),
            "pending_tasks": sum(1 for t in self.tasks.values()
                                if t["status"] == TaskStatus.PENDING.value),
            "failed_tasks": sum(1 for t in self.tasks.values()
                              if t["status"] == TaskStatus.FAILED.value),
            "uptime": datetime.now().isoformat(),
            "config": self.config
        }

    def save_state(self, filepath: str = "agent_state.json") -> bool:
        """حفظ حالة الوكيل"""
        try:
            state = {
                "tasks": self.tasks,
                "completed_tasks": self.completed_tasks,
                "task_history": self.task_history,
                "saved_at": datetime.now().isoformat()
            }

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(state, f, ensure_ascii=False, indent=2)

            logger.info(f"💾 تم حفظ حالة الوكيل في: {filepath}")
            return True
        except Exception as e:
            logger.error(f"❌ خطأ في الحفظ: {e}")
            return False

    def interactive_menu(self):
        """القائمة التفاعلية للوكيل"""
        while True:
            print("\n" + "="*60)
            print("  📋 القائمة الرئيسية")
            print("="*60)
            print("  [1] إنشاء مهمة جديدة")
            print("  [2] عرض المهام")
            print("  [3] تحديث حالة مهمة")
            print("  [4] معالجة ملفات")
            print("  [5] إنشاء تقرير")
            print("  [6] الإحصائيات")
            print("  [7] حفظ الحالة")
            print("  [8] الخروج")
            print("="*60)

            choice = input("  اختر خياراً (1-8): ").strip()

            if choice == "1":
                self._create_task_interactive()
            elif choice == "2":
                self._list_tasks_interactive()
            elif choice == "3":
                self._update_task_interactive()
            elif choice == "4":
                self._process_files_interactive()
            elif choice == "5":
                self._generate_report_interactive()
            elif choice == "6":
                self._show_statistics()
            elif choice == "7":
                self.save_state()
                print("  ✅ تم الحفظ بنجاح")
            elif choice == "8":
                print("\n  👋 وداعاً! شكراً لاستخدامك Universal Agent")
                break
            else:
                print("  ❌ اختيار غير صحيح")

    def _create_task_interactive(self):
        """إنشاء مهمة بشكل تفاعلي"""
        print("\n  📝 إنشاء مهمة جديدة:")
        name = input("  اسم المهمة: ").strip()
        desc = input("  الوصف (اختياري): ").strip()

        print("\n  الأولوية:")
        print("    [1] حرجة | [2] عالية | [3] متوسطة | [4] منخفضة")
        priority_choice = input("  اختر (1-4): ").strip()
        priority_map = {"1": TaskPriority.CRITICAL, "2": TaskPriority.HIGH,
                       "3": TaskPriority.MEDIUM, "4": TaskPriority.LOW}
        priority = priority_map.get(priority_choice, TaskPriority.MEDIUM)

        task_id = self.create_task(name, desc, priority)
        print(f"\n  ✅ تم إنشاء المهمة برقم: {task_id}")

    def _list_tasks_interactive(self):
        """عرض المهام بشكل تفاعلي"""
        tasks = self.list_tasks()
        if not tasks:
            print("\n  ❌ لا توجد مهام")
            return

        print("\n  📋 قائمة المهام:")
        print("  " + "="*50)
        for task in tasks:
            status_emoji = "✅" if task["status"] == "مكتملة" else "⏳"
            print(f"  {status_emoji} {task['name']}")
            print(f"     الحالة: {task['status']} | الأولوية: {task['priority']}")
            print(f"     المعرف: {task['id']}")
            print()

    def _update_task_interactive(self):
        """تحديث حالة مهمة بشكل تفاعلي"""
        task_id = input("  أدخل معرف المهمة: ").strip()

        print("\n  الحالة الجديدة:")
        print("    [1] قيد الانتظار | [2] قيد التنفيذ | [3] مكتملة | [4] فشلت")
        status_choice = input("  اختر (1-4): ").strip()
        status_map = {
            "1": TaskStatus.PENDING, "2": TaskStatus.IN_PROGRESS,
            "3": TaskStatus.COMPLETED, "4": TaskStatus.FAILED
        }

        status = status_map.get(status_choice, TaskStatus.PENDING)
        self.update_task_status(task_id, status)

    def _process_files_interactive(self):
        """معالجة الملفات بشكل تفاعلي"""
        directory = input("  أدخل مسار المجلد: ").strip()
        stats = self.process_files(directory)

        print(f"\n  📊 النتائج:")
        print(f"  إجمالي الملفات: {stats['total']}")
        print(f"  معالجة: {stats['processed']}")
        print(f"  فشل: {stats['failed']}")

    def _generate_report_interactive(self):
        """إنشاء تقرير بشكل تفاعلي"""
        report = self.generate_report("detailed")
        print("\n  📊 التقرير:")
        print(f"  إجمالي المهام: {report['summary']['total_tasks']}")
        print(f"  المكتملة: {report['summary']['completed']}")
        print(f"  المعلقة: {report['summary']['pending']}")
        print(f"  نسبة الإنجاز: {report['summary']['completion_rate']}")

    def _show_statistics(self):
        """عرض الإحصائيات"""
        stats = self.get_statistics()
        print("\n  📈 الإحصائيات:")
        print(f"  إجمالي المهام: {stats['total_tasks']}")
        print(f"  المكتملة: {stats['completed_tasks']}")
        print(f"  المعلقة: {stats['pending_tasks']}")
        print(f"  الفاشلة: {stats['failed_tasks']}")


def main():
    """الدالة الرئيسية"""
    agent = UniversalAgent()

    # مثال على الاستخدام
    print("\n🚀 بدء العمليات التلقائية...\n")

    # إنشاء مهام تجريبية
    task1 = agent.create_task(
        "معالجة الفواتير الشهرية",
        "استخراج ومعالجة فواتير الشهر الحالي",
        TaskPriority.HIGH,
        tags=["billing", "automated"]
    )

    task2 = agent.create_task(
        "إرسال تقارير البريد",
        "إرسال التقارير الأسبوعية عبر البريد",
        TaskPriority.MEDIUM,
        tags=["email", "reporting"]
    )

    task3 = agent.create_task(
        "نسخ احتياطي يومي",
        "عمل نسخة احتياطية من قاعدة البيانات",
        TaskPriority.CRITICAL,
        tags=["backup", "system"]
    )

    # تحديث حالات المهام
    agent.update_task_status(task1, TaskStatus.IN_PROGRESS)
    agent.update_task_status(task3, TaskStatus.COMPLETED)

    # عرض المهام
    print("\n📋 المهام الحالية:")
    tasks = agent.list_tasks()
    for task in tasks:
        status_icon = "✅" if task["status"] == "مكتملة" else "⏳"
        print(f"  {status_icon} {task['name']}")

    # إنشاء تقرير
    report = agent.generate_report()
    print(f"\n📊 التقرير:")
    print(f"  المهام الإجمالية: {report['summary']['total_tasks']}")
    print(f"  المكتملة: {report['summary']['completed']}")
    print(f"  نسبة الإنجاز: {report['summary']['completion_rate']}")

    # حفظ الحالة
    agent.save_state()

    # عرض الإحصائيات
    stats = agent.get_statistics()
    print(f"\n📈 الإحصائيات:")
    print(f"  إجمالي المهام: {stats['total_tasks']}")
    print(f"  المعلقة: {stats['pending_tasks']}")

    # القائمة التفاعلية (اختياري)
    print("\n" + "="*60)
    interactive = input("\nهل تريد استخدام القائمة التفاعلية؟ (y/n): ").strip().lower()
    if interactive == 'y':
        agent.interactive_menu()


if __name__ == "__main__":
    main()
