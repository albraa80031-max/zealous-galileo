# 📁 مجلد البيانات - Legal Data Directory

هذا المجلد يحتوي على جميع البيانات القانونية المنظمة والمرتبة.

## 📂 محتويات المجلد

### ملفات البيانات الرئيسية

```
📊 cases.json              - قائمة القضايا القانونية (2 قضية)
📋 contracts.json          - قائمة العقود (2 عقد)
📑 documents.json          - قائمة الوثائق (7 وثائق)
```

### ملفات المراجع والتوثيق

```
📄 sample_legal_data.json  - البيانات النموذجية الكاملة (للنسخ الاحتياطية)
📘 INDEX.md               - فهرس شامل لجميع البيانات
📗 README.md              - هذا الملف
```

---

## 🎯 البنية التنظيمية

### 1. cases.json - القضايا

**محتويات الملف:**
- معرف فريد (ID)
- عنوان القضية
- وصف مفصل
- حالة القضية (active, pending, closed)
- الأولوية (high, medium, low)
- تواريخ الإنشاء والتحديث
- الأطراف المعنية
- الوثائق المرتبطة
- ملاحظات إضافية
- الفئة (employment, commercial, etc.)

**مثال:**
```json
{
  "id": "CASE_2026_001",
  "title": "قضية عقد عمل - عدم الامتثال للشروط",
  "status": "active",
  "priority": "high",
  "parties": ["شركة", "فرد"],
  "documents": ["DOC_001", "DOC_002"]
}
```

### 2. contracts.json - العقود

**محتويات الملف:**
- معرف فريد (ID)
- عنوان العقد
- نوع العقد (employment, supply, service, etc.)
- حالة العقد (active, draft, expired, terminated)
- الأطراف الموقعة
- الشروط والأحكام
  - المدة
  - القيمة
  - تاريخ البداية والنهاية
- الوثائق المرتبطة

**مثال:**
```json
{
  "id": "CONTRACT_2026_001",
  "title": "عقد عمل",
  "type": "employment",
  "status": "active",
  "terms": {
    "duration": "2 سنة",
    "salary": 5000,
    "currency": "AED"
  }
}
```

### 3. documents.json - الوثائق

**محتويات الملف:**
- معرف فريد (ID)
- عنوان الوثيقة
- نوع الوثيقة (contract, report, invoice, etc.)
- القضية المرتبطة (إن وجدت)
- العقد المرتبط (إن وجد)
- تاريخ الإنشاء
- حالة الوثيقة (filed, draft, archived)
- حجم الملف (إذا كان موجوداً)
- مسار الملف
- الكلمات المفتاحية (Tags)

**مثال:**
```json
{
  "id": "DOC_2026_001",
  "title": "نسخة من عقد التوظيف",
  "type": "contract",
  "related_case": "CASE_2026_001",
  "status": "filed"
}
```

---

## 📊 الإحصائيات الحالية

| النوع | العدد | التفاصيل |
|------|-------|---------|
| القضايا | 2 | 1 نشطة، 1 قيد الانتظار |
| العقود | 2 | 1 نشط، 1 مسودة |
| الوثائق | 7 | 5 مرفوع، 2 مسودة |

---

## 🔄 كيفية الاستخدام

### 1. استيراد البيانات في Python

```python
import json
from pathlib import Path

# تحميل البيانات
with open('data/cases.json', 'r', encoding='utf-8') as f:
    cases_data = json.load(f)

for case in cases_data['cases']:
    print(f"القضية: {case['title']}")
```

### 2. استخدام Legal Agent

```python
from legal_agent import LegalAgent

agent = LegalAgent()

# استيراد البيانات النموذجية
agent.import_from_json("data/sample_legal_data.json")

# الحصول على ملخص
summary = agent.get_summary()
print(f"القضايا النشطة: {summary['active_cases']}")
```

### 3. المزامنة مع GitHub

```python
from legal_agent import GitHubSync

sync = GitHubSync(token, owner, repo)

# قراءة البيانات المحلية
with open('data/sample_legal_data.json') as f:
    data = json.load(f)

# مزامنة مع GitHub
sync.sync_data(data)
```

---

## 🔗 الروابط والعلاقات

### نموذج الربط

```
القضية ← → الوثائق
   ↓
العقد ← → الوثائق
```

**مثال:**
- CASE_2026_001 مرتبطة بـ CONTRACT_2026_001
- كلاهما مرتبط بـ DOC_2026_001 و DOC_2026_002

---

## ✅ قائمة التحقق

- [x] تنظيم البيانات في ملفات منفصلة
- [x] إضافة معرفات فريدة لكل عنصر
- [x] ربط البيانات ببعضها البعض
- [x] إنشاء فهرس شامل
- [x] توثيق كامل للبيانات
- [ ] إضافة بيانات جديدة (قيد الانتظار)
- [ ] مزامنة مع GitHub Issues (قيد الانتظار)

---

## 🔐 ملاحظات الأمان

⚠️ **تحذير:** هذه البيانات تحتوي على معلومات حساسة وشخصية.

- استخدم `.gitignore` لحماية البيانات الحساسة
- لا تشارك البيانات علناً
- احتفظ بنسخ احتياطية آمنة
- قيد الوصول للمخولين فقط

---

## 📞 المساعدة والدعم

للحصول على معلومات إضافية، انظر إلى:
- 📘 [INDEX.md](INDEX.md) - فهرس شامل
- 📗 [DOCUMENTATION.md](../DOCUMENTATION.md) - التوثيق الكاملة
- 🚀 [QUICKSTART.md](../QUICKSTART.md) - البدء السريع

---

**آخر تحديث:** 2026-08-20  
**الإصدار:** 1.0.0
