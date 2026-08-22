#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مثال على استخدام Universal Agent
Universal Agent Usage Example
"""

from universal_agent import UniversalAgent, TaskPriority, TaskStatus
import time


def example_1_basic_task_management():
    """مثال 1: إدارة المهام الأساسية"""
    print("\n" + "="*60)
    print("  📝 مثال 1: إدارة المهام الأساسية")
    print("="*60)

    agent = UniversalAgent()

    # إنشاء مهام
    print("\n  ✏️  إنشاء مهام...")
    task1 = agent.create_task(
        "إعداد تقرير المبيعات الشهري",
        "تجميع بيانات المبيعات وإعداد التقرير",
        TaskPriority.HIGH,
        tags=["reporting", "monthly", "sales"]
    )

    task2 = agent.create_task(
        "تحديث قاعدة بيانات العملاء",
        "مزامنة بيانات العملاء من النظام",
        TaskPriority.MEDIUM,
        tags=["database", "sync"]
    )

    task3 = agent.create_task(
        "إرسال بيانات المتجر",
        "إرسال البيانات إلى نظام الحفظ",
        TaskPriority.CRITICAL,
        tags=["backup", "important"]
    )

    # تحديث حالات المهام
    print("\n  📊 تحديث حالات المهام...")
    agent.update_task_status(task1, TaskStatus.IN_PROGRESS)
    time.sleep(0.5)
    agent.update_task_status(task2, TaskStatus.PENDING)
    agent.update_task_status(task3, TaskStatus.IN_PROGRESS)
    time.sleep(0.5)
    agent.update_task_status(task1, TaskStatus.COMPLETED)

    # عرض المهام
    print("\n  📋 قائمة المهام:")
    tasks = agent.list_tasks()
    for i, task in enumerate(tasks, 1):
        status_emoji = "✅" if task["status"] == "مكتملة" else "⏳"
        print(f"    {i}. {status_emoji} {task['name']}")
        print(f"       الحالة: {task['status']} | الأولوية: {task['priority']}")


def example_2_task_priority_management():
    """مثال 2: إدارة أولويات المهام"""
    print("\n" + "="*60)
    print("  🎯 مثال 2: إدارة أولويات المهام")
    print("="*60)

    agent = UniversalAgent()

    print("\n  ✏️  إنشاء مهام بأولويات مختلفة...")

    # مهام بأولويات مختلفة
    priorities = [
        ("اجتماع طارئ مع المدير", TaskPriority.CRITICAL),
        ("تحديث الموقع الإلكتروني", TaskPriority.HIGH),
        ("مراجعة المستندات", TaskPriority.MEDIUM),
        ("تنظيف سطح المكتب", TaskPriority.LOW),
        ("الاشتراك في النشرة", TaskPriority.MINIMAL)
    ]

    task_ids = []
    for task_name, priority in priorities:
        task_id = agent.create_task(
            task_name,
            priority=priority
        )
        task_ids.append(task_id)
        time.sleep(0.3)

    # عرض المهام مرتبة حسب الأولوية
    print("\n  🔝 المهام مرتبة حسب الأولوية:")
    tasks = agent.list_tasks()
    for i, task in enumerate(tasks, 1):
        priority_emoji = {
            "CRITICAL": "🔴",
            "HIGH": "🟠",
            "MEDIUM": "🟡",
            "LOW": "🟢",
            "MINIMAL": "⚪"
        }.get(task["priority"], "❓")
        print(f"    {i}. {priority_emoji} {task['name']} [{task['priority']}]")


def example_3_reporting_and_statistics():
    """مثال 3: التقارير والإحصائيات"""
    print("\n" + "="*60)
    print("  📊 مثال 3: التقارير والإحصائيات")
    print("="*60)

    agent = UniversalAgent()

    print("\n  ✏️  إنشاء مهام تجريبية...")

    # إنشاء مهام متنوعة
    for i in range(10):
        priority = [
            TaskPriority.CRITICAL,
            TaskPriority.HIGH,
            TaskPriority.MEDIUM,
            TaskPriority.LOW
        ][i % 4]

        status = [TaskStatus.COMPLETED, TaskStatus.IN_PROGRESS, TaskStatus.PENDING][i % 3]

        task_id = agent.create_task(
            f"مهمة تجريبية رقم {i+1}",
            priority=priority
        )
        agent.update_task_status(task_id, status)
        time.sleep(0.2)

    # إنشاء تقرير
    print("\n  📄 إنشاء تقرير...")
    report = agent.generate_report("detailed")

    print("\n  📊 نتائج التقرير:")
    print(f"    المهام الإجمالية: {report['summary']['total_tasks']}")
    print(f"    المهام المكتملة: {report['summary']['completed']}")
    print(f"    المهام المعلقة: {report['summary']['pending']}")
    print(f"    نسبة الإنجاز: {report['summary']['completion_rate']}")

    # الإحصائيات
    print("\n  📈 الإحصائيات:")
    stats = agent.get_statistics()
    print(f"    إجمالي المهام: {stats['total_tasks']}")
    print(f"    المكتملة: {stats['completed_tasks']}")
    print(f"    المعلقة: {stats['pending_tasks']}")
    print(f"    الفاشلة: {stats['failed_tasks']}")

    # توزيع حسب الأولوية
    if report['task_breakdown']:
        print("\n  🎯 توزيع المهام حسب الأولوية:")
        for priority, count in report['task_breakdown'].items():
            print(f"    {priority}: {count} مهام")


def example_4_file_processing():
    """مثال 4: معالجة الملفات"""
    print("\n" + "="*60)
    print("  📄 مثال 4: معالجة الملفات")
    print("="*60)

    agent = UniversalAgent()

    # محاكاة معالجة الملفات
    print("\n  📂 معالجة مجلد الملفات...")

    # نظراً لأننا في بيئة تجريبية، سنعرض الوظائف المتاحة
    print("""
    الوظائف المتاحة:
    ✅ agent.process_files(directory_path)
       - معالجة جميع الملفات في مجلد

    ✅ agent.extract_from_pdf(pdf_path)
       - استخراج البيانات من ملف PDF

    ✅ agent.process_email(email_data)
       - معالجة رسالة بريد

    مثال:
    """)

    # مثال على البيانات
    example_email = {
        "from": "customer@example.com",
        "subject": "استفسار عن المنتج",
        "body": "أود الاستفسار عن توفر المنتج...",
        "attachments": ["invoice.pdf"]
    }

    print(f"\n  📧 معالجة بريد:")
    print(f"    من: {example_email['from']}")
    print(f"    الموضوع: {example_email['subject']}")
    result = agent.process_email(example_email)
    print(f"    النتيجة: {'✅ نجح' if result else '❌ فشل'}")


def example_5_scheduling():
    """مثال 5: جدولة المهام"""
    print("\n" + "="*60)
    print("  ⏰ مثال 5: جدولة المهام")
    print("="*60)

    agent = UniversalAgent()

    print("\n  ⏰ إنشاء مهام مجدولة...")

    # إنشاء مهام
    task_id = agent.create_task(
        "بث التقرير الدوري",
        "إرسال التقرير كل يوم الجمعة",
        TaskPriority.HIGH
    )

    # جدولة المهام
    print(f"\n  📅 جدولة المهام:")
    schedule_times = [
        "2026-08-25T09:00:00",
        "2026-08-25T14:00:00",
        "2026-08-26T10:00:00"
    ]

    for sched_time in schedule_times:
        result = agent.schedule_task(task_id, sched_time)
        if result:
            print(f"    ✅ تم الجدولة: {sched_time}")

    print("\n  💡 ملاحظة: المهام المجدولة ستنفذ تلقائياً في الوقت المحدد")


def example_6_automation():
    """مثال 6: الأتمتة"""
    print("\n" + "="*60)
    print("  🔄 مثال 6: الأتمتة والعمليات الذكية")
    print("="*60)

    agent = UniversalAgent()

    print("\n  🤖 تنفيذ عمليات أتمتة...")

    automations = [
        ("مزامنة قاعدة البيانات", {"source": "local", "destination": "cloud"}),
        ("تنظيف الملفات القديمة", {"days": 30, "backup": True}),
        ("إنشاء نسخة احتياطية", {"type": "full", "compression": True}),
    ]

    for auto_name, params in automations:
        print(f"\n  🔄 {auto_name}")
        result = agent.execute_automation(auto_name, params)
        status = "✅ نجح" if result else "❌ فشل"
        print(f"     النتيجة: {status}")


def example_7_save_and_load():
    """مثال 7: الحفظ والتحميل"""
    print("\n" + "="*60)
    print("  💾 مثال 7: حفظ وتحميل الحالة")
    print("="*60)

    agent = UniversalAgent()

    print("\n  ✏️  إنشاء مهام...")
    for i in range(3):
        agent.create_task(f"مهمة للحفظ رقم {i+1}")
        time.sleep(0.2)

    # حفظ الحالة
    print("\n  💾 حفظ حالة الوكيل...")
    agent.save_state("agent_state_example.json")
    print("    ✅ تم الحفظ في: agent_state_example.json")

    # عرض ملخص
    print("\n  📊 ملخص الحالة المحفوظة:")
    stats = agent.get_statistics()
    print(f"    المهام الكلية: {stats['total_tasks']}")
    print(f"    الوقت: {stats['uptime']}")


def main():
    """الدالة الرئيسية"""
    print("\n" + "="*60)
    print("  🚀 Universal Agent - أمثلة الاستخدام")
    print("="*60)

    examples = [
        ("إدارة المهام الأساسية", example_1_basic_task_management),
        ("إدارة الأولويات", example_2_task_priority_management),
        ("التقارير والإحصائيات", example_3_reporting_and_statistics),
        ("معالجة الملفات", example_4_file_processing),
        ("جدولة المهام", example_5_scheduling),
        ("الأتمتة", example_6_automation),
        ("الحفظ والتحميل", example_7_save_and_load),
    ]

    print("\n  اختر مثالاً:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"    [{i}] {name}")
    print(f"    [{len(examples)+1}] تشغيل جميع الأمثلة")
    print(f"    [0] خروج")

    choice = input("\n  اختيارك: ").strip()

    try:
        choice = int(choice)
        if choice == 0:
            print("\n  👋 وداعاً!")
            return
        elif choice == len(examples) + 1:
            for _, example_func in examples:
                example_func()
                time.sleep(1)
        elif 1 <= choice <= len(examples):
            examples[choice - 1][1]()
        else:
            print("  ❌ اختيار غير صحيح")
    except ValueError:
        print("  ❌ الرجاء إدخال رقم صحيح")

    print("\n  ✅ انتهت الأمثلة!")
    print("  للمزيد، اطلع على README.md\n")


if __name__ == "__main__":
    main()
