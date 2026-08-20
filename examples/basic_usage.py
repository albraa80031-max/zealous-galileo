"""
أمثلة الاستخدام الأساسي - Legal Agent
"""

import json
from legal_agent import LegalAgent, GitHubSync


def example_1_basic_operations():
    """مثال 1: العمليات الأساسية"""
    print("=" * 50)
    print("مثال 1: العمليات الأساسية")
    print("=" * 50)

    # إنشاء عامل جديد
    agent = LegalAgent("config.json")
    print("✅ تم إنشاء العامل القانوني")

    # إضافة قضية
    case = agent.add_case(
        "CASE_2026_DEMO_001",
        "نزاع عقد عمل",
        "نزاع بين الموظف والشركة حول الراتب"
    )
    print(f"✅ تمت إضافة القضية: {case['id']}")

    # إضافة عقد
    contract = agent.add_contract(
        "CONTRACT_2026_DEMO_001",
        "عقد عمل",
        "اتفاقية توظيف بين الطرفين",
        ["شركة الإمارات", "أحمد محمد"]
    )
    print(f"✅ تمت إضافة العقد: {contract['id']}")

    # إضافة وثيقة
    doc = agent.add_document(
        "DOC_2026_DEMO_001",
        "نسخة العقد الأصلية",
        "محتوى العقد الموقع",
        "contract"
    )
    print(f"✅ تمت إضافة الوثيقة: {doc['id']}")

    # عرض الملخص
    summary = agent.get_summary()
    print(f"\n📊 ملخص البيانات:")
    print(f"  • إجمالي القضايا: {summary['total_cases']}")
    print(f"  • القضايا النشطة: {summary['active_cases']}")
    print(f"  • إجمالي العقود: {summary['total_contracts']}")
    print(f"  • إجمالي الوثائق: {summary['total_documents']}")
    print()


def example_2_update_operations():
    """مثال 2: عمليات التحديث"""
    print("=" * 50)
    print("مثال 2: عمليات التحديث")
    print("=" * 50)

    agent = LegalAgent("config.json")

    # إضافة قضية أولاً
    case = agent.add_case(
        "CASE_2026_DEMO_002",
        "قضية أولية",
        "قضية في المرحلة الأولية"
    )
    print(f"✅ تمت إضافة القضية بحالة: {case['status']}")

    # تحديث حالة القضية
    updated_case = agent.update_case(
        "CASE_2026_DEMO_002",
        status="in_progress",
        title="قضية قيد المعالجة"
    )
    print(f"✅ تم تحديث القضية:")
    print(f"  • الحالة الجديدة: {updated_case['status']}")
    print(f"  • العنوان الجديد: {updated_case['title']}")
    print()


def example_3_data_export_import():
    """مثال 3: تصدير واستيراد البيانات"""
    print("=" * 50)
    print("مثال 3: تصدير واستيراد البيانات")
    print("=" * 50)

    agent = LegalAgent("config.json")

    # إضافة عدة عناصر
    agent.add_case("CASE_EXPORT_001", "قضية للتصدير 1", "وصف 1")
    agent.add_case("CASE_EXPORT_002", "قضية للتصدير 2", "وصف 2")
    agent.add_contract(
        "CONTRACT_EXPORT_001",
        "عقد للتصدير",
        "محتوى",
        ["طرف1", "طرف2"]
    )

    # تصدير البيانات
    if agent.export_to_json("data/demo_export.json"):
        print("✅ تم تصدير البيانات بنجاح")
        with open("data/demo_export.json", "r", encoding="utf-8") as f:
            exported = json.load(f)
        print(f"  • القضايا المصدرة: {len(exported['cases'])}")
        print(f"  • العقود المصدرة: {len(exported['contracts'])}")

    # استيراد البيانات
    agent2 = LegalAgent("config.json")
    if agent2.import_from_json("data/sample_legal_data.json"):
        print("✅ تم استيراد البيانات بنجاح")
        summary = agent2.get_summary()
        print(f"  • القضايا المستوردة: {summary['total_cases']}")
        print(f"  • العقود المستوردة: {summary['total_contracts']}")
    print()


def example_4_data_retrieval():
    """مثال 4: استرجاع البيانات"""
    print("=" * 50)
    print("مثال 4: استرجاع البيانات")
    print("=" * 50)

    agent = LegalAgent("config.json")

    # استيراد بيانات نموذجية
    agent.import_from_json("data/sample_legal_data.json")
    print("✅ تم استيراد البيانات النموذجية")

    # الحصول على جميع القضايا
    cases = agent.get_all_cases()
    print(f"\n📋 القضايا ({len(cases)}):")
    for case in cases:
        status_emoji = "🟢" if case['status'] == "active" else "🟡"
        print(f"  {status_emoji} {case['id']}: {case['title']}")

    # الحصول على جميع العقود
    contracts = agent.get_all_contracts()
    print(f"\n📄 العقود ({len(contracts)}):")
    for contract in contracts:
        print(f"  📌 {contract['id']}: {contract['title']} [{contract['status']}]")

    # الحصول على وثيقة محددة
    if cases:
        case_id = cases[0]['id']
        case = agent.get_case(case_id)
        print(f"\n📑 تفاصيل القضية {case_id}:")
        print(f"  • العنوان: {case['title']}")
        print(f"  • الوصف: {case['description']}")
        print(f"  • الحالة: {case['status']}")
        print(f"  • تاريخ الإنشاء: {case['created_at']}")
    print()


def example_5_github_sync():
    """مثال 5: مزامنة GitHub (بدون توكن حقيقي)"""
    print("=" * 50)
    print("مثال 5: محاكاة مزامنة GitHub")
    print("=" * 50)

    # إنشاء نظام المزامنة (بدون توكن حقيقي)
    sync = GitHubSync(
        token="demo_token_only",
        repo_owner="demo_owner",
        repo_name="demo_repo"
    )
    print("✅ تم إنشاء نظام المزامنة")

    # الحصول على معلومات المستودع
    info = sync.get_repository_info()
    print(f"\n🔗 معلومات المستودع:")
    print(f"  • الرابط: {info['url']}")
    print(f"  • المالك: {info['owner']}")
    print(f"  • الاسم: {info['name']}")

    # محاكاة إنشاء issue
    issue = sync.create_issue(
        title="قضية جديدة - قيد التتبع",
        body="تفاصيل القضية...",
        labels=["legal", "urgent"]
    )
    print(f"\n✅ تم إنشاء issue:")
    print(f"  • العنوان: {issue['title']}")
    print(f"  • الحالة: {issue['state']}")

    # محاكاة إنشاء ملف
    file_info = sync.create_file(
        path="data/legal_data.json",
        content='{"cases": []}',
        message="إضافة ملف البيانات"
    )
    print(f"\n✅ تم إنشاء ملف:")
    print(f"  • المسار: {file_info['path']}")
    print(f"  • الرسالة: {file_info['message']}")

    # عرض سجل المزامنة
    log = sync.get_sync_log()
    print(f"\n📝 سجل المزامنة ({len(log)} عملية):")
    for entry in log:
        print(f"  • {entry['action']} - {entry['timestamp']}")
    print()


def main():
    """تشغيل جميع الأمثلة"""
    print("\n🎓 أمثلة استخدام Legal Agent\n")

    try:
        example_1_basic_operations()
        example_2_update_operations()
        example_3_data_export_import()
        example_4_data_retrieval()
        example_5_github_sync()

        print("=" * 50)
        print("✨ اكتملت جميع الأمثلة بنجاح!")
        print("=" * 50)
    except Exception as e:
        print(f"\n❌ حدث خطأ: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
