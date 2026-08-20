#!/usr/bin/env python3
"""
Interactive Legal Agent Query System
يسمح لك بطرح أسئلة واسترجاع الملفات من نظام Legal Agent
"""

import json
from pathlib import Path
from legal_agent import LegalAgent


def load_agent():
    """تحميل Legal Agent وبيانات النظام"""
    agent = LegalAgent()
    agent.import_from_json("data/sample_legal_data.json")
    return agent


def search_cases(agent, query):
    """البحث عن قضايا"""
    cases = agent.get_all_cases()
    results = []

    query_lower = query.lower()
    for case in cases:
        if (query_lower in case.get("title", "").lower() or
            query_lower in case.get("description", "").lower()):
            results.append(case)

    return results


def search_contracts(agent, query):
    """البحث عن عقود"""
    contracts = agent.contracts
    results = []

    query_lower = query.lower()
    for contract in contracts:
        if (query_lower in contract.get("title", "").lower() or
            query_lower in contract.get("type", "").lower()):
            results.append(contract)

    return results


def search_documents(agent, query):
    """البحث عن وثائق"""
    documents = agent.documents
    results = []

    query_lower = query.lower()
    for doc in documents:
        if (query_lower in doc.get("title", "").lower() or
            query_lower in doc.get("type", "").lower() or
            query_lower in " ".join(doc.get("tags", [])).lower()):
            results.append(doc)

    return results


def get_case_details(agent, case_id):
    """الحصول على تفاصيل قضية معينة"""
    return agent.get_case(case_id)


def get_related_documents(agent, case_id):
    """الحصول على الوثائق المرتبطة بقضية"""
    case = agent.get_case(case_id)
    if not case:
        return None

    related_docs = []
    for doc_id in case.get("documents", []):
        for doc in agent.documents:
            if doc["id"] == doc_id:
                related_docs.append(doc)

    return related_docs


def export_case_data(agent, case_id, filename=None):
    """تصدير بيانات قضية إلى ملف JSON"""
    case = agent.get_case(case_id)
    if not case:
        return None

    if filename is None:
        filename = f"export_{case_id}.json"

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(case, f, ensure_ascii=False, indent=2)

    return filename


def print_help():
    """عرض قائمة الأوامر المتاحة"""
    help_text = """
╔════════════════════════════════════════════════════════════════╗
║           Legal Agent Interactive Query System                ║
║         نظام الاستعلام التفاعلي لوكيل الشؤون القانونية      ║
╚════════════════════════════════════════════════════════════════╝

📋 الأوامر المتاحة:

1. search cases <query>        - البحث عن قضايا
   مثال: search cases عقد عمل

2. search contracts <query>    - البحث عن عقود
   مثال: search contracts توظيف

3. search documents <query>    - البحث عن وثائق
   مثال: search documents فاتورة

4. case <CASE_ID>              - عرض تفاصيل قضية
   مثال: case CASE_2026_001

5. documents <CASE_ID>         - عرض الوثائق المرتبطة بقضية
   مثال: documents CASE_2026_001

6. export <CASE_ID>            - تصدير بيانات القضية إلى ملف JSON
   مثال: export CASE_2026_001

7. summary                      - عرض ملخص البيانات
8. help                        - عرض هذه الرسالة
9. exit                        - الخروج من البرنامج

════════════════════════════════════════════════════════════════
    """
    print(help_text)


def main():
    """البرنامج الرئيسي"""
    print("\n🤝 جاري تحميل Legal Agent...")
    agent = load_agent()
    print("✅ تم التحميل بنجاح!\n")

    print_help()

    while True:
        try:
            user_input = input("\n➡️  أدخل أمر: ").strip()

            if not user_input:
                continue

            parts = user_input.split(maxsplit=1)
            command = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""

            # أوامر البحث
            if command == "search":
                search_parts = args.split(maxsplit=1)
                if len(search_parts) < 2:
                    print("❌ صيغة خاطئة. استخدم: search <type> <query>")
                    continue

                search_type = search_parts[0].lower()
                query = search_parts[1]

                if search_type == "cases":
                    results = search_cases(agent, query)
                    if results:
                        print(f"\n✅ وجدت {len(results)} قضية:")
                        for case in results:
                            print(f"  • {case['id']}: {case['title']}")
                    else:
                        print("❌ لم تُعثر على قضايا")

                elif search_type == "contracts":
                    results = search_contracts(agent, query)
                    if results:
                        print(f"\n✅ وجدت {len(results)} عقد:")
                        for contract in results:
                            print(f"  • {contract['id']}: {contract['title']}")
                    else:
                        print("❌ لم تُعثر على عقود")

                elif search_type == "documents":
                    results = search_documents(agent, query)
                    if results:
                        print(f"\n✅ وجدت {len(results)} وثيقة:")
                        for doc in results:
                            print(f"  • {doc['id']}: {doc['title']}")
                    else:
                        print("❌ لم تُعثر على وثائق")
                else:
                    print("❌ نوع بحث غير معروف. استخدم: cases, contracts, أو documents")

            # عرض تفاصيل قضية
            elif command == "case":
                if not args:
                    print("❌ يرجى تحديد معرف القضية")
                    continue

                case = get_case_details(agent, args)
                if case:
                    print(f"\n📋 تفاصيل القضية {args}:")
                    print(json.dumps(case, ensure_ascii=False, indent=2))
                else:
                    print(f"❌ لم يتم العثور على القضية {args}")

            # عرض الوثائق المرتبطة
            elif command == "documents":
                if not args:
                    print("❌ يرجى تحديد معرف القضية")
                    continue

                docs = get_related_documents(agent, args)
                if docs is not None:
                    if docs:
                        print(f"\n📄 الوثائق المرتبطة بـ {args}:")
                        for doc in docs:
                            print(f"  • {doc['id']}: {doc['title']} ({doc['type']})")
                    else:
                        print(f"⚠️  لا توجد وثائق مرتبطة بـ {args}")
                else:
                    print(f"❌ لم يتم العثور على القضية {args}")

            # تصدير البيانات
            elif command == "export":
                if not args:
                    print("❌ يرجى تحديد معرف القضية")
                    continue

                filename = export_case_data(agent, args)
                if filename:
                    print(f"✅ تم تصدير بيانات القضية إلى: {filename}")
                else:
                    print(f"❌ لم يتم العثور على القضية {args}")

            # عرض الملخص
            elif command == "summary":
                summary = agent.get_summary()
                print("\n📊 ملخص البيانات:")
                print(json.dumps(summary, ensure_ascii=False, indent=2))

            # عرض المساعدة
            elif command == "help":
                print_help()

            # الخروج
            elif command == "exit" or command == "quit":
                print("\n👋 شكراً لاستخدامك Legal Agent!")
                break

            else:
                print("❌ أمر غير معروف. اكتب 'help' لعرض الأوامر المتاحة")

        except KeyboardInterrupt:
            print("\n\n👋 تم الخروج!")
            break
        except Exception as e:
            print(f"❌ خطأ: {e}")


if __name__ == "__main__":
    main()
