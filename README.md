# 🤖 Universal Agent - وكيل إدارة المهام الشامل

**الوكيل الذكي الشامل لإدارة جميع المهام الإدارية والعمليات التلقائية**

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()

---

## 📋 المحتويات

- [المميزات](#المميزات)
- [المتطلبات](#المتطلبات)
- [التثبيت](#التثبيت)
- [الاستخدام](#الاستخدام)
- [أمثلة](#أمثلة)
- [الوحدات](#الوحدات)
- [الإعدادات](#الإعدادات)
- [المساهمة](#المساهمة)

---

## ✨ المميزات

### 🎯 إدارة المهام الذكية
- ✅ إنشاء وتتبع المهام
- 📊 نظام أولويات ذكي (حرج، عالي، متوسط، منخفض)
- 📈 تقارير وإحصائيات شاملة
- ⏰ جدولة وتنفيذ المهام المجدولة
- 🔄 إعادة محاولة تلقائية مع backoff exponential

### 📧 إدارة البريد الإلكتروني
- 📮 معالجة الرسائل الواردة
- 📤 إرسال الرسائل تلقائياً
- 🏷️ تنظيم وتصنيف الرسائل
- 🔍 البحث المتقدم
- 📎 معالجة المرفقات

### 📄 معالجة الملفات والمستندات
- 🗂️ معالجة الملفات بأنواعها المختلفة
- 📑 استخراج البيانات من PDFs
- 🖼️ معالجة الصور و OCR
- 📊 معالجة جداول Excel و CSV
- 💾 أرشفة وتخزين ذكية

### 🔄 الأتمتة الشاملة
- ⚡ تنفيذ عمليات معقدة بضغطة زر
- 🔗 ربط العمليات مع بعضها
- 📋 سير العمل القابل للتخصيص
- 🎯 تنفيذ متوازي للمهام
- 🛡️ معالجة الأخطاء التلقائية

### 📊 التقارير والإحصائيات
- 📈 تقارير مفصلة وملخصة
- 📉 رسوم بيانية وإحصائيات
- 📧 إرسال تقارير تلقائية
- 💾 تصدير إلى صيغ متعددة (JSON, PDF, Excel)

### 🔌 التكاملات
- 🏪 Shopify API
- 📱 Google Drive
- 💬 Telegram
- 🎯 Slack
- 📧 Gmail / Outlook
- 🗄️ قواعد البيانات

---

## 🔧 المتطلبات

```
Python 3.8+
pip (مدير الحزم)
```

### المكتبات المطلوبة:
```
requests>=2.28.0
python-dotenv>=0.20.0
schedule>=1.1.9
pdfplumber>=0.7.0
Pillow>=9.0.0
openpyxl>=3.8.0
google-auth>=2.16.0
google-auth-oauthlib>=0.6.0
google-auth-httplib2>=0.1.0
google-api-python-client>=2.70.0
```

---

## 📥 التثبيت

### 1. استنساخ المستودع
```bash
git clone https://github.com/yourusername/universal-agent.git
cd universal-agent
```

### 2. تثبيت المتطلبات
```bash
pip install -r requirements.txt
```

### 3. إعداد الإعدادات
```bash
# نسخ ملف الإعدادات
cp config.json config.local.json

# تحرير الإعدادات حسب احتياجاتك
nano config.local.json
```

### 4. تعيين متغيرات البيئة
```bash
# إنشاء ملف .env
cat > .env << EOF
SHOPIFY_API_KEY=your_key_here
SHOPIFY_API_PASSWORD=your_password_here
GOOGLE_DRIVE_CREDENTIALS_PATH=credentials.json
TELEGRAM_BOT_TOKEN=your_token_here
SLACK_WEBHOOK_URL=your_webhook_url_here
EOF
```

---

## 🚀 الاستخدام

### الاستخدام الأساسي

```python
from universal_agent import UniversalAgent, TaskPriority, TaskStatus

# تهيئة الوكيل
agent = UniversalAgent(config_path="config.json")

# إنشاء مهمة
task_id = agent.create_task(
    task_name="معالجة الفواتير",
    description="معالجة فواتير الشهر الحالي",
    priority=TaskPriority.HIGH
)

# تحديث حالة المهمة
agent.update_task_status(task_id, TaskStatus.IN_PROGRESS)

# عرض المهام
tasks = agent.list_tasks()
for task in tasks:
    print(f"- {task['name']}: {task['status']}")

# إنشاء تقرير
report = agent.generate_report()
print(report)

# حفظ الحالة
agent.save_state()
```

### تشغيل الوكيل

```bash
# تشغيل بدون واجهة تفاعلية
python universal_agent.py

# تشغيل مع واجهة تفاعلية
python -c "from universal_agent import UniversalAgent; agent = UniversalAgent(); agent.interactive_menu()"
```

---

## 💡 أمثلة

### مثال 1: إنشاء وتتبع المهام

```python
from universal_agent import UniversalAgent, TaskPriority, TaskStatus

agent = UniversalAgent()

# إنشاء مهام
task1 = agent.create_task(
    "إرسال تقرير البيع الشهري",
    "إرسال ملخص البيع إلى الإدارة",
    TaskPriority.HIGH,
    tags=["reporting", "monthly"]
)

task2 = agent.create_task(
    "تحديث قاعدة البيانات",
    "تحديث السجلات والبيانات",
    TaskPriority.MEDIUM
)

# تتبع تقدم المهام
agent.update_task_status(task1, TaskStatus.IN_PROGRESS)
time.sleep(2)
agent.update_task_status(task1, TaskStatus.COMPLETED)

# الحصول على الإحصائيات
stats = agent.get_statistics()
print(f"✅ المهام المكتملة: {stats['completed_tasks']}")
```

### مثال 2: معالجة الملفات

```python
# معالجة مجلد كامل
stats = agent.process_files("/path/to/documents")
print(f"تمت معالجة {stats['processed']} ملف")

# استخراج البيانات من PDF
pdf_data = agent.extract_from_pdf("/path/to/document.pdf")
print(pdf_data)
```

### مثال 3: معالجة البريد

```python
# معالجة بريد
email_data = {
    "from": "sender@example.com",
    "subject": "تقرير مهم",
    "body": "محتوى الرسالة",
    "attachments": ["file.pdf"]
}

agent.process_email(email_data)
```

### مثال 4: الأتمتة

```python
# تنفيذ عملية أتمتة معقدة
automation_params = {
    "source": "google_drive",
    "destination": "database",
    "format": "csv",
    "schedule": "daily"
}

agent.execute_automation("sync_data", automation_params)
```

---

## 🧩 الوحدات

### 📧 Email Module
معالجة البريد الإلكتروني والاتصالات

**الوظائف:**
- `process_email()` - معالجة الرسائل
- `send_email()` - إرسال رسائل
- `filter_emails()` - تصفية الرسائل
- `extract_attachments()` - استخراج المرفقات

### 📄 File Processing Module
معالجة الملفات والمستندات

**الوظائف:**
- `process_files()` - معالجة الملفات
- `extract_from_pdf()` - استخراج من PDF
- `process_images()` - معالجة الصور
- `archive_files()` - أرشفة الملفات

### 🔄 Automation Module
تنفيذ العمليات التلقائية

**الوظائف:**
- `execute_automation()` - تنفيذ عملية
- `create_workflow()` - إنشاء سير عمل
- `schedule_automation()` - جدولة عملية

### 📊 Reporting Module
إنشاء التقارير والإحصائيات

**الوظائف:**
- `generate_report()` - إنشاء تقرير
- `get_statistics()` - الحصول على إحصائيات
- `export_report()` - تصدير التقرير

### ⏰ Scheduling Module
جدولة المهام والعمليات

**الوظائف:**
- `schedule_task()` - جدولة مهمة
- `schedule_recurring()` - جدولة مكررة
- `cancel_scheduled()` - إلغاء الجدولة

---

## ⚙️ الإعدادات

### ملف config.json

```json
{
  "agent_name": "Universal Agent",
  "version": "1.0.0",
  "modules": {
    "email": { "enabled": true },
    "file_processing": { "enabled": true },
    "automation": { "enabled": true }
  }
}
```

### تخصيص الإعدادات

```python
# تحميل إعدادات مخصصة
agent = UniversalAgent(config_path="config.local.json")

# تعديل الإعدادات برمجياً
agent.config["modules"]["email"]["enabled"] = True
```

---

## 📚 التوثيق المتقدمة

### إنشاء مهام معقدة مع المهام الفرعية

```python
# المهام الفرعية
subtasks = [
    {"name": "جمع البيانات", "duration": 30},
    {"name": "معالجة البيانات", "duration": 45},
    {"name": "إنشاء التقرير", "duration": 15}
]

task = agent.create_task(
    "مشروع تقرير شامل",
    subtasks=subtasks
)
```

### سير العمل المتقدم

```python
workflow = agent.create_workflow([
    ("download_data", {"source": "google_drive"}),
    ("process_data", {"format": "csv"}),
    ("generate_report", {"template": "monthly"}),
    ("send_email", {"recipients": ["admin@example.com"]})
])

agent.execute_workflow(workflow)
```

---

## 🔐 الأمان

- ✅ تشفير بيانات المرور
- ✅ توثيق الـ API
- ✅ التحقق من الصلاحيات
- ✅ تسجيل النشاطات
- ✅ معالجة الأخطاء الآمنة

---

## 🤝 المساهمة

نرحب بمساهماتك! 

```bash
# 1. Fork المستودع
# 2. إنشاء فرع جديد
git checkout -b feature/my-feature

# 3. عمل التعديلات
git add .
git commit -m "إضافة ميزة جديدة"

# 4. Push
git push origin feature/my-feature

# 5. Open Pull Request
```

---

## 📝 الترخيص

MIT License - انظر [LICENSE](LICENSE) للمزيد

---

## 📧 الدعم والتواصل

- 📧 البريد: support@universalagent.local
- 💬 Telegram: [@universalagentbot](https://t.me/universalagentbot)
- 🌐 الموقع: https://universalagent.local

---

## 🙏 شكر وتقدير

شكر خاص لجميع المساهمين والمستخدمين الذين يساعدون في تطوير هذا المشروع.

---

## 📊 الإحصائيات

- ⭐ **Stars**: ![GitHub stars](https://img.shields.io/github/stars/yourusername/universal-agent)
- 🍴 **Forks**: ![GitHub forks](https://img.shields.io/github/forks/yourusername/universal-agent)
- 👁️ **Watchers**: ![GitHub watchers](https://img.shields.io/github/watchers/yourusername/universal-agent)

---

**آخر تحديث**: 2026-08-22 | **الإصدار**: 1.0.0

صُنع بـ ❤️ لجعل حياتك أسهل
