# ☁️ Google Drive Integration - دليل التكامل مع Google Drive

تطبيق Legal Agent الآن يتزامن تلقائياً مع Google Drive!

---

## 🎯 الميزات الرئيسية

### 📤 المزامنة التلقائية
- مزامنة البيانات تلقائياً مع Google Drive
- تحديث البيانات في الوقت الفعلي
- سجل كامل لجميع عمليات المزامنة

### 💾 النسخ الاحتياطية
- إنشاء نسخ احتياطية دورية
- حفظ البيانات في Google Drive بشكل آمن
- استرجاع البيانات القديمة عند الحاجة

### 🔄 التزامن الدائم
- متزامن مع Google Drive في جميع الأوقات
- الوصول إلى البيانات من أي مكان
- شارك البيانات بسهولة

### 📊 المراقبة المباشرة
- عرض حالة المزامنة الحالية
- تتبع آخر تحديث
- إحصائيات مفصلة عن كل عملية

---

## 🚀 البدء السريع

### 1️⃣ تثبيت المتطلبات

```bash
pip install -r requirements.txt
```

### 2️⃣ تشغيل التطبيق المحسّن

```bash
python app_with_drive.py
```

### 3️⃣ فتح في المتصفح

```
http://localhost:5000
```

---

## 📁 هيكل مجلدات Google Drive

عند تفعيل المزامنة، سيتم إنشاء هيكل المجلدات التالي:

```
My Drive/
├── Legal Agent Data/
│   ├── Cases/                      # القضايا
│   │   ├── cases.json
│   │   └── cases_backup.json
│   │
│   ├── Contracts/                  # العقود
│   │   ├── contracts.json
│   │   └── contracts_backup.json
│   │
│   ├── Documents/                  # الوثائق
│   │   ├── documents.json
│   │   └── documents_backup.json
│   │
│   └── Backups/                    # النسخ الاحتياطية
│       ├── backup_2026-08-20_12-00-00.json
│       ├── backup_2026-08-20_13-00-00.json
│       └── backup_2026-08-20_14-00-00.json
```

---

## 🔌 API Endpoints للمزامنة

### الحصول على حالة المزامنة
```http
GET /api/sync/status
```

**الرد:**
```json
{
  "is_synced": true,
  "sync_info": {
    "last_sync": "2026-08-20T12:34:56",
    "total_operations": 42,
    "status": "synced"
  },
  "drive_structure": {
    "folder_name": "Legal Agent Data",
    "structure": {...}
  }
}
```

### تنفيذ مزامنة فورية
```http
POST /api/sync/now
```

**الرد:**
```json
{
  "success": true,
  "message": "✅ تمت المزامنة بنجاح",
  "timestamp": "2026-08-20T12:34:56",
  "status": {...}
}
```

### إنشاء نسخة احتياطية
```http
POST /api/sync/backup
```

**الرد:**
```json
{
  "success": true,
  "message": "✅ تم إنشاء النسخة الاحتياطية بنجاح",
  "backup_size": 2048,
  "timestamp": "2026-08-20T12:34:56"
}
```

### الحصول على سجل المزامنة
```http
GET /api/sync/log
```

**الرد:**
```json
{
  "total_operations": 42,
  "recent_operations": [
    {
      "timestamp": "2026-08-20T12:34:56",
      "action": "sync_all_data",
      "status": "completed",
      "details": {...}
    }
  ],
  "status": {...}
}
```

### جدولة مزامنة دورية
```http
POST /api/sync/schedule

{
  "interval": 3600
}
```

**الرد:**
```json
{
  "success": true,
  "message": "✅ تم جدولة المزامنة كل 3600 ثانية",
  "interval": 3600,
  "next_sync": "2026-08-20T13:34:56"
}
```

---

## 📱 استخدام التطبيق

### 1. البحث والعرض
- استخدم الواجهة الرئيسية للبحث عن القضايا والعقود
- عرض التفاصيل الكاملة مع الوثائق المرتبطة

### 2. إضافة بيانات جديدة
```bash
POST /api/case/add

{
  "id": "CASE_2026_003",
  "title": "قضية جديدة",
  "description": "وصف القضية",
  "status": "active",
  "priority": "high",
  "parties": ["الطرف الأول", "الطرف الثاني"]
}
```

**النتيجة:** تتم المزامنة مع Google Drive تلقائياً! ✨

### 3. تحديث البيانات الموجودة
```bash
POST /api/case/CASE_2026_001/update

{
  "status": "closed",
  "priority": "low",
  "notes": "تم حل القضية بنجاح"
}
```

**النتيجة:** يتم التحديث والمزامنة فوراً! ⚡

---

## 🔐 الأمان والخصوصية

### حماية البيانات
- ✅ تشفير البيانات أثناء النقل
- ✅ حفظ آمن على خوادم Google
- ✅ مراقبة جميع عمليات المزامنة

### التحكم في الوصول
- 🔑 تحكم كامل في صلاحيات المشاركة
- 👥 شارك الملفات مع فريقك
- 🔒 تحديد من يمكنه الوصول

---

## 📊 مثال عملي كامل

### السيناريو:
إضافة قضية جديدة ومزامنتها مع Google Drive

### الخطوات:

**1️⃣ إضافة القضية**
```bash
curl -X POST http://localhost:5000/api/case/add \
  -H "Content-Type: application/json" \
  -d '{
    "id": "CASE_2026_003",
    "title": "قضية عمل جديدة",
    "description": "نزاع بخصوص الراتب",
    "status": "pending",
    "priority": "high",
    "parties": ["الموظف", "الشركة"]
  }'
```

**الرد:**
```json
{
  "success": true,
  "message": "✅ تمت إضافة القضية بنجاح",
  "case_id": "CASE_2026_003"
}
```

**2️⃣ التحقق من المزامنة**
```bash
curl http://localhost:5000/api/sync/status
```

**الرد:**
```json
{
  "is_synced": true,
  "sync_info": {
    "last_sync": "2026-08-20T12:34:56",
    "total_operations": 43,
    "status": "synced"
  }
}
```

**3️⃣ فتح Google Drive**
- انتقل إلى Google Drive
- تحقق من مجلد "Legal Agent Data"
- ستجد القضية الجديدة مضافة تلقائياً!

---

## ⚙️ الإعدادات المتقدمة

### تغيير اسم المجلد
```python
drive_sync = GoogleDriveSync(folder_name="بيانات الشؤون القانونية")
```

### تغيير فترة المزامنة
```python
drive_manager.sync_interval = 1800  # 30 دقيقة
```

### تعطيل المزامنة التلقائية
```python
# عدم تنفيذ auto_sync في كل عملية
# استخدم /api/sync/now للمزامنة اليدوية
```

---

## 🆘 استكشاف الأخطاء

### المشكلة: المزامنة لا تعمل

**الحل:**
1. تأكد من تثبيت Flask بشكل صحيح
2. تحقق من اتصال الإنترنت
3. تحقق من سجلات الأخطاء: `sync_log.json`

### المشكلة: النسخ الاحتياطية كبيرة جداً

**الحل:**
1. احذف النسخ الاحتياطية القديمة من Google Drive
2. قلل عدد الوثائق المخزنة محلياً
3. استخدم ضغط البيانات

### المشكلة: بطء المزامنة

**الحل:**
1. قلل حجم البيانات
2. زد فترة المزامنة
3. تحقق من سرعة الإنترنت

---

## 📞 الدعم والمساعدة

### الموارد المتاحة:
- 📚 [WEB_INTERFACE.md](WEB_INTERFACE.md) - دليل الواجهة الأمامية
- 📖 [DOCUMENTATION.md](DOCUMENTATION.md) - التوثيق الكامل
- 🚀 [QUICKSTART.md](QUICKSTART.md) - البدء السريع

### الأسئلة الشائعة:

**س: هل يمكن استخدام التطبيق بدون Google Drive؟**
ج: نعم، يعمل بدون Google Drive لكن بدون مزامنة.

**س: كم عدد النسخ الاحتياطية المخزنة؟**
ج: يحتفظ النظام بآخر 10 نسخ احتياطية فقط.

**س: هل البيانات محمية؟**
ج: نعم، تشفير أثناء النقل وتخزين آمن على Google.

---

**آخر تحديث:** 2026-08-20  
**الإصدار:** 2.0.0 (مع Google Drive Integration)
