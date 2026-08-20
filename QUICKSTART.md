# 🚀 البدء السريع - Legal Agent

## الخطوات الأساسية الثلاث

### 1️⃣ التثبيت والإعداد

```bash
# 1. تثبيت المتطلبات
pip install -r requirements.txt

# 2. نسخ ملف الإعدادات
cp config.json config.local.json

# 3. تعديل الإعدادات بـ GitHub الخاص بك
nano config.local.json
```

### 2️⃣ استخدام بسيط

```python
# افتح Python REPL
python3

# ثم أدخل الأكواد التالية:

from legal_agent import LegalAgent

# إنشاء عامل جديد
agent = LegalAgent("config.json")

# إضافة قضية جديدة
case = agent.add_case(
    "CASE_2026_NEW",
    "قضيتي الأولى",
    "وصف القضية الجديدة"
)
print(f"✅ تمت إضافة القضية: {case['id']}")

# إضافة عقد جديد
contract = agent.add_contract(
    "CONTRACT_NEW",
    "عقدي الأول",
    "محتوى العقد",
    ["أنا", "الطرف الآخر"]
)
print(f"✅ تمت إضافة العقد: {contract['id']}")

# عرض ملخص البيانات
summary = agent.get_summary()
print(f"\n📊 ملخص البيانات:")
print(f"  • القضايا: {summary['total_cases']}")
print(f"  • العقود: {summary['total_contracts']}")
print(f"  • الوثائق: {summary['total_documents']}")

# حفظ البيانات
agent.export_to_json("data/my_data.json")
print("✅ تم حفظ البيانات!")
```

### 3️⃣ مزامنة مع GitHub

```python
from legal_agent import LegalAgent, GitHubSync

# إنشاء العامل
agent = LegalAgent("config.json")

# استخدام بيانات نموذجية
agent.import_from_json("data/sample_legal_data.json")

# إنشاء نظام المزامنة
sync = GitHubSync(
    token="ghp_YOUR_TOKEN_HERE",
    repo_owner="your_username",
    repo_name="zealous-galileo"
)

# مزامنة كاملة
data = {
    "cases": agent.get_all_cases(),
    "contracts": agent.get_all_contracts(),
    "documents": agent.get_all_documents()
}

if sync.sync_data(data):
    print("✅ تمت المزامنة بنجاح!")
else:
    print("❌ فشلت المزامنة")
```

---

## 📋 قائمة الأوامر السريعة

### عرض البيانات
```python
# جميع القضايا
cases = agent.get_all_cases()
print(f"📑 عدد القضايا: {len(cases)}")

# قضية محددة
case = agent.get_case("CASE_2026_001")
print(f"📄 القضية: {case['title']}")

# جميع العقود
contracts = agent.get_all_contracts()
for contract in contracts:
    print(f"📋 {contract['title']} - {contract['status']}")
```

### تحديث البيانات
```python
# تحديث حالة القضية
agent.update_case("CASE_2026_001", status="closed")

# إضافة وثيقة
doc = agent.add_document(
    "NEW_DOC",
    "وثيقة جديدة",
    "محتوى الوثيقة",
    "report"
)
```

### تصدير واستيراد
```python
# تصدير إلى JSON
agent.export_to_json("backup.json")

# استيراد من JSON
agent.import_from_json("backup.json")
```

---

## 🧪 تشغيل الاختبارات

```bash
# تشغيل جميع الاختبارات
pytest -v

# اختبار واحد فقط
pytest tests/test_agent.py::TestLegalAgent::test_add_case -v

# مع تقرير التغطية
pytest --cov=legal_agent
```

---

## 📦 متغيرات البيئة

إنشاء ملف `.env`:

```env
# GitHub Configuration
GITHUB_TOKEN=ghp_your_token_here
GITHUB_OWNER=your_username
GITHUB_REPO=zealous-galileo

# App Configuration
LOG_LEVEL=INFO
DEBUG=False
```

---

## 🔧 استكشاف الأخطاء

### المشكلة: فشل الاتصال بـ GitHub
```python
# تحقق من البيانات:
sync = GitHubSync(token, owner, repo)
info = sync.get_repository_info()
print(info)  # تحقق من صحة البيانات
```

### المشكلة: البيانات لا تُحفظ
```python
# تأكد من وجود مجلد data
import os
os.makedirs("data", exist_ok=True)

# ثم حاول مرة أخرى
agent.export_to_json()
```

---

## 📚 مراجع إضافية

- [التوثيق الكاملة](DOCUMENTATION.md)
- [ملف README](README.md)
- [الاختبارات](tests/)

---

**جاهز للبدء؟** 🎉  
ابدأ الآن بـ: `pip install -r requirements.txt`

