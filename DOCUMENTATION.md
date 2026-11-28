# 📚 توثيق Legal Agent - نظام إدارة البيانات القانونية

## المحتويات
- [نظرة عامة](#نظرة-عامة)
- [البدء السريع](#البدء-السريع)
- [البنية الأساسية](#البنية-الأساسية)
- [واجهة API](#واجهة-api)
- [مزامنة GitHub](#مزامنة-github)
- [أمثلة الاستخدام](#أمثلة-الاستخدام)

---

## نظرة عامة

**Legal Agent** هو نظام متقدم لإدارة البيانات القانونية مع تكامل كامل مع GitHub. يوفر:

- ✅ إدارة منظمة للقضايا والعقود والوثائق
- ✅ مزامنة تلقائية مع GitHub
- ✅ تتبع كامل للتغييرات
- ✅ تصدير واستيراد البيانات
- ✅ نظام أمان قوي

---

## البدء السريع

### 1️⃣ التثبيت

```bash
# استنساخ المشروع
git clone https://github.com/albraa80031-max/zealous-galileo.git
cd zealous-galileo

# تثبيت المتطلبات
pip install -r requirements.txt
```

### 2️⃣ التكوين

```bash
# تحرير ملف الإعدادات
nano config.json

# إضافة بيانات GitHub
# github_token: رمز الوصول الشخصي
# repo_owner: اسم المالك
# repo_name: اسم المستودع
```

### 3️⃣ التشغيل الأساسي

```python
from legal_agent import LegalAgent

# إنشاء عامل جديد
agent = LegalAgent("config.json")

# إضافة قضية
case = agent.add_case(
    "CASE_001",
    "قضية عقد عمل",
    "نزاع حول شروط العقد"
)

# إضافة عقد
contract = agent.add_contract(
    "CONTRACT_001",
    "عقد عمل",
    "محتوى العقد...",
    ["الشركة", "الموظف"]
)

# تصدير البيانات
agent.export_to_json("data/legal_data.json")
```

---

## البنية الأساسية

```
legal-agent/
├── legal_agent/
│   ├── __init__.py           # تهيئة الحزمة
│   ├── agent.py              # العامل الرئيسي
│   └── github_sync.py        # مزامنة GitHub
├── data/
│   ├── sample_legal_data.json    # بيانات نموذجية
│   └── legal_data.json           # البيانات المحفوظة
├── tests/
│   └── test_agent.py         # الاختبارات
├── config.json               # الإعدادات
├── requirements.txt          # المتطلبات
└── README.md                # التعريف الأساسي
```

---

## واجهة API

### فئة LegalAgent

#### 1. إضافة قضية
```python
agent.add_case(
    case_id: str,           # معرف فريد للقضية
    title: str,             # عنوان القضية
    description: str,       # وصف القضية
    status: str = "active"  # حالة القضية
) -> Dict
```

**مثال:**
```python
case = agent.add_case(
    "CASE_2026_001",
    "نزاع عقد عمل",
    "نزاع حول تطبيق شروط العقد"
)
```

#### 2. إضافة عقد
```python
agent.add_contract(
    contract_id: str,              # معرف فريد للعقد
    title: str,                    # عنوان العقد
    content: str,                  # محتوى العقد
    parties: List[str],            # الأطراف المعنية
    status: str = "draft"          # حالة العقد
) -> Dict
```

**مثال:**
```python
contract = agent.add_contract(
    "CONTRACT_2026_001",
    "عقد عمل",
    "محتوى العقد...",
    ["شركة الإمارات", "أحمد محمد"]
)
```

#### 3. إضافة وثيقة
```python
agent.add_document(
    doc_id: str,    # معرف الوثيقة
    title: str,     # عنوان الوثيقة
    content: str,   # محتوى الوثيقة
    doc_type: str   # نوع الوثيقة (contract, report, etc.)
) -> Dict
```

#### 4. الحصول على بيانات
```python
# قضية واحدة
case = agent.get_case("CASE_2026_001")

# جميع القضايا
cases = agent.get_all_cases()

# جميع العقود
contracts = agent.get_all_contracts()

# جميع الوثائق
documents = agent.get_all_documents()

# ملخص البيانات
summary = agent.get_summary()
```

#### 5. تحديث البيانات
```python
agent.update_case(
    "CASE_2026_001",
    status="closed",
    title="قضية محسومة"
)
```

#### 6. تصدير واستيراد البيانات
```python
# تصدير إلى JSON
agent.export_to_json("data/export.json")

# استيراد من JSON
agent.import_from_json("data/export.json")
```

---

### فئة GitHubSync

#### 1. إنشاء Issue
```python
from legal_agent import GitHubSync

sync = GitHubSync(token, repo_owner, repo_name)

issue = sync.create_issue(
    title="قضية عمل جديدة",
    body="تفاصيل القضية...",
    labels=["legal", "urgent"]
)
```

#### 2. تحديث Issue
```python
sync.update_issue(
    issue_number=1,
    title="العنوان الجديد",
    body="المحتوى الجديد",
    state="closed"
)
```

#### 3. إنشاء/تحديث ملف
```python
# إنشاء ملف جديد
sync.create_file(
    path="data/cases.json",
    content="محتوى الملف",
    message="إضافة قائمة القضايا"
)

# تحديث ملف موجود
sync.update_file(
    path="data/cases.json",
    content="محتوى مُحدث",
    message="تحديث قائمة القضايا"
)
```

#### 4. مزامنة شاملة
```python
data = {
    "cases": agent.get_all_cases(),
    "contracts": agent.get_all_contracts(),
    "documents": agent.get_all_documents()
}

sync.sync_data(data)
```

---

## مزامنة GitHub

### التكوين

اضبط المتغيرات التالية في `config.json`:

```json
{
  "github_integration": {
    "enabled": true,
    "auto_sync": true,
    "sync_interval": 3600,
    "retry_attempts": 3,
    "timeout": 30
  }
}
```

### المزامنة التلقائية

```python
from legal_agent import LegalAgent, GitHubSync

agent = LegalAgent("config.json")
sync = GitHubSync(
    token=agent.config["github_token"],
    repo_owner=agent.config["repo_owner"],
    repo_name=agent.config["repo_name"]
)

# بيانات دورية للمزامنة
data = {
    "cases": agent.get_all_cases(),
    "contracts": agent.get_all_contracts(),
    "documents": agent.get_all_documents()
}

# مزامنة شاملة
sync.sync_data(data)

# عرض سجل المزامنة
log = sync.get_sync_log()
```

---

## أمثلة الاستخدام

### مثال 1: إنشاء حالة عمل كاملة

```python
from legal_agent import LegalAgent, GitHubSync

# تهيئة العامل
agent = LegalAgent("config.json")

# إضافة قضية
case = agent.add_case(
    "CASE_2026_003",
    "نزاع توظيف",
    "نزاع حول بند الفسخ في العقد"
)

# إضافة وثائق متعلقة
doc1 = agent.add_document(
    "DOC_2026_008",
    "نسخة العقد",
    "محتوى العقد...",
    "contract"
)

# تحديث حالة القضية
agent.update_case("CASE_2026_003", status="in_progress")

# تصدير البيانات
agent.export_to_json()

# مزامنة مع GitHub
sync = GitHubSync(token, owner, repo)
sync.sync_data({
    "cases": agent.get_all_cases(),
    "documents": agent.get_all_documents()
})
```

### مثال 2: استيراد بيانات موجودة

```python
from legal_agent import LegalAgent

agent = LegalAgent()

# استيراد البيانات
agent.import_from_json("data/sample_legal_data.json")

# الحصول على ملخص
summary = agent.get_summary()
print(f"إجمالي القضايا: {summary['total_cases']}")
print(f"القضايا النشطة: {summary['active_cases']}")
```

---

## الاختبارات

```bash
# تشغيل جميع الاختبارات
pytest

# تشغيل اختبار محدد
pytest tests/test_agent.py::TestLegalAgent::test_add_case -v

# مع تقرير التغطية
pytest --cov=legal_agent tests/
```

---

## الترخيص

هذا المشروع مرخص تحت رخصة MIT

---

## التواصل والدعم

- **البريد الإلكتروني**: albraa80031@gmail.com
- **GitHub**: [zealous-galileo](https://github.com/albraa80031-max/zealous-galileo)
- **آخر تحديث**: 2026-08-20

---

**تم الإنشاء بواسطة Claude Code** ✨
