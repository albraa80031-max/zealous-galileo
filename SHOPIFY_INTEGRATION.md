# 🚀 دليل الربط الكامل - تكامل Shopify مع Vantory Agent

## 📋 نظرة عامة

هذا الدليل يشرح كيفية استخدام النظام المتكامل الذي يربط متجر Shopify الخاص بك مع وكيل Vantory الذكي للإدارة الآلية الكاملة.

---

## 🏗️ بنية النظام

```
الهيكل الكامل للنظام:
│
├─ shopify_connector.py
│  └─ الاتصال المباشر بـ Shopify API
│
├─ vantory_agent.py
│  └─ معالجة الطلبات والمخزون محلياً
│
├─ advanced_vantory_agent.py
│  └─ دمج كامل بين Shopify و Vantory
│  └─ مزامنة ثنائية الاتجاه
│  └─ معالجة آلية للطلبات
│
├─ auto_manager.py
│  └─ إدارة تلقائية 24/7
│  └─ جدولة المهام
│  └─ التقارير التلقائية
│
└─ live_dashboard.py
   └─ لوحة مراقبة حية
   └─ إحصائيات فورية
   └─ تنبيهات الوقت الفعلي
```

---

## 🔧 المكونات الرئيسية

### 1. **ShopifyConnector** (`shopify_connector.py`)
الاتصال المباشر بـ Shopify API

```python
from shopify_connector import ShopifyConnector

# إنشاء الاتصال
connector = ShopifyConnector(
    shop_url="uk1msh-1p.myshopify.com",
    api_token="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"
)

# سحب الطلبات
orders = connector.get_new_orders(status="unfulfilled")

# سحب المنتجات
products = connector.get_products()

# إنشاء fulfillment
connector.create_fulfillment(order_id, line_items)

# الحصول على إحصائيات المتجر
stats = connector.get_store_stats()
```

**المميزات:**
- ✅ التحقق التلقائي من الاتصال
- ✅ معالجة الأخطاء الذكية
- ✅ سجلات مفصلة
- ✅ دعم API 2024-01

---

### 2. **AdvancedVantoryAgent** (`advanced_vantory_agent.py`)
الدمج الكامل بين Shopify والوكيل

```python
from advanced_vantory_agent import AdvancedVantoryAgent

# إنشاء الوكيل المتقدم
agent = AdvancedVantoryAgent()

# مزامنة واحدة شاملة
result = agent.sync_with_shopify()

# بدء المراقبة المستمرة
agent.start_continuous_monitoring(sync_interval=300)

# الحصول على الحالة الكاملة
status = agent.get_full_status()

# إنشاء تقرير متقدم
report = agent.generate_advanced_report()
```

**المميزات:**
- ✅ معالجة تلقائية للطلبات الجديدة
- ✅ مزامنة المخزون الفورية
- ✅ إنشاء fulfillments تلقائياً
- ✅ تتبع الطلبات المعالجة (لمنع المعالجة المكررة)
- ✅ مراقبة مستمرة بخيط منفصل

---

### 3. **AutoManager** (`auto_manager.py`)
الإدارة الآلية 24/7

```python
from auto_manager import AutoManager

# إنشاء المدير
manager = AutoManager()

# بدء الإدارة التلقائية
manager.start()

# عرض الحالة
status = manager.get_status()
```

**المهام الآلية المجدولة:**

| المهمة | التكرار | الوصف |
|--------|--------|-------|
| معالجة الطلبات | كل ساعة | سحب ومعالجة الطلبات من Shopify |
| فحص المخزون | كل 6 ساعات | التحقق من المخزون المنخفض |
| مزامنة المخزون | كل 6 ساعات | تحديث حالة المخزون |
| إنشاء الفواتير | كل 30 دقيقة | إنشاء فواتير للطلبات الجديدة |
| جدولة الشحن | كل ساعة | جدولة الشحن للطلبات المعالجة |
| التقرير اليومي | الساعة 23:00 | إنشاء تقرير شامل يومي |
| حفظ الحالة | كل ساعة | حفظ جميع البيانات |
| التحقق من الاتصال | كل 30 دقيقة | التحقق من الاتصال بـ Shopify |

---

### 4. **LiveDashboard** (`live_dashboard.py`)
لوحة مراقبة حية

```python
from live_dashboard import LiveDashboard

# إنشاء لوحة المراقبة
dashboard = LiveDashboard()

# بدء المراقبة الحية (تحديث كل 30 ثانية)
dashboard.start_live_monitoring(interval=30)

# تصدير تقرير فوري
filename = dashboard.export_report()
```

**المعلومات المعروضة:**
- 📊 إحصائيات المبيعات الحية
- 📦 حالة المخزون الفورية
- 💰 الإيرادات اليومية
- 🚚 حالة الشحنات
- 👥 آخر الطلبات
- ⚠️ التنبيهات والتحذيرات
- 🔌 حالة الاتصال بـ Shopify

---

## 🚀 البدء السريع

### الخطوة 1: التثبيت

```bash
# تثبيت المتطلبات
pip install -r requirements.txt
```

### الخطوة 2: الإعدادات

تأكد من أن بيانات الاتصال صحيحة:

```python
# في أي ملف:
SHOP = "uk1msh-1p.myshopify.com"
TOKEN = "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"
```

### الخطوة 3: التشغيل

#### الخيار 1: الإدارة التلقائية 24/7
```bash
python auto_manager.py
```

#### الخيار 2: لوحة المراقبة الحية
```bash
python live_dashboard.py
```

#### الخيار 3: الوكيل المتقدم (برمجياً)
```bash
python advanced_vantory_agent.py
```

---

## 📊 الاستخدام المتقدم

### السيناريو 1: معالجة طلب واحد يدوياً

```python
from advanced_vantory_agent import AdvancedVantoryAgent

agent = AdvancedVantoryAgent()

# معالجة طلب محدد
shopify_order = {
    "id": 12345,
    "customer": {"email": "customer@example.com"},
    "line_items": [
        {"title": "Product", "sku": "SKU-001", "quantity": 1, "price": "299.00"}
    ],
    "total_price": "299.00"
}

agent._process_shopify_order(shopify_order)
```

### السيناريو 2: مزامنة شاملة مع تقرير

```python
# مزامنة شاملة
result = agent.sync_with_shopify()

# عرض النتائج
print(f"الطلبات المعالجة: {result['orders']['processed']}")
print(f"الفulfillments المنشأة: {result['fulfillments']['created']}")

# إنشاء تقرير
report = agent.generate_advanced_report()

# حفظ التقرير
with open("sync_report.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
```

### السيناريو 3: مراقبة مستمرة مع التحكم

```python
agent = AdvancedVantoryAgent()

# بدء المراقبة (في خيط منفصل)
agent.start_continuous_monitoring(sync_interval=300)

# الآن يمكن القيام بعمليات أخرى
while True:
    status = agent.get_full_status()
    
    if status["monitoring"]:
        print("✅ المراقبة نشطة")
    
    # يمكن إيقاف المراقبة في أي وقت
    # agent.stop_continuous_monitoring()
    
    time.sleep(60)
```

---

## 🔍 المراقبة والتشخيص

### عرض السجلات

```python
# السجلات تُكتب إلى stdout و auto_manager.log
# كل عملية تُسجل مع الوقت والحالة والتفاصيل

# مثال:
# 2026-08-22 14:30:45 - [AUTO-MANAGER] - INFO - 🔄 [معالجة الطلبات] بدء العملية...
# 2026-08-22 14:30:47 - [AUTO-MANAGER] - INFO - 📋 [معالجة الطلبات] ✅ نجحت: تمت معالجة 3 طلب
```

### مراقبة الأداء

```python
# عرض حالة النظام الكاملة
status = agent.get_full_status()

print(f"المراقبة نشطة: {status['monitoring']}")
print(f"الطلبات المعالجة: {status['store_stats']['processed_unique_orders']}")
print(f"الإيرادات الكلية: {status['store_stats']['total_revenue']}")
print(f"منتجات قليلة المخزون: {status['inventory']['low_stock_count']}")
print(f"منتجات حرجة المخزون: {status['inventory']['critical_stock_count']}")
```

---

## ⚠️ معالجة الأخطاء والمشاكل

### المشكلة: فقدان الاتصال بـ Shopify

**الحل:**
```python
# يتم إعادة المحاولة تلقائياً كل 30 ثانية
# السجلات تعرض حالة الاتصال

# يمكن التحقق اليدوي:
if not agent.shopify.is_connected:
    print("❌ فقدان الاتصال!")
    # سيتم إعادة المحاولة في المزامنة القادمة
```

### المشكلة: معالجة نفس الطلب مرتين

**الحل:**
```python
# يتم تتبع الطلبات المعالجة تلقائياً
# لا يتم معالجة نفس الطلب مرتين

# البيانات تُحفظ في processed_orders.json
# عند إعادة تشغيل النظام، يتم تحميلها تلقائياً
```

### المشكلة: المخزون غير متطابق

**الحل:**
```python
# يتم مزامنة المخزون تلقائياً كل 6 ساعات
# يمكن فرض مزامنة يدوية:

result = agent.sync_with_shopify()
agent._sync_inventory_from_shopify(result['products'])
```

---

## 📈 الإحصائيات والتقارير

### التقرير اليومي (تلقائي)

يُنشأ تلقائياً الساعة 23:00 ويحتوي على:

```json
{
  "date": "2026-08-22",
  "summary": {
    "total_orders": 15,
    "total_items_sold": 42,
    "total_revenue": 8500,
    "average_order_value": 567
  },
  "inventory": {
    "total_items": 250,
    "low_stock_items": {...}
  },
  "profit_estimate": 4250,
  "shopify_integration": {
    "connected": true,
    "orders_synced": 15,
    "fulfillments_created": 12
  }
}
```

### التقرير المخصص

```python
# إنشاء تقرير في أي وقت
report = agent.generate_advanced_report()

# تصدير إلى ملف JSON
with open("custom_report.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2, default=str)
```

---

## 🔐 الأمان

### توكن API

- **الموقع الآمن:** احفظ التوكن في متغيرات البيئة أو ملف إعدادات آمن
- **عدم المشاركة:** لا تشارك التوكن في الكود العام
- **التجديد الدوري:** جدّد التوكن كل 90 يوماً

### البيانات

- **الحفظ الآمن:** جميع البيانات تُحفظ محلياً في JSON
- **النسخ الاحتياطية:** أنشئ نسخاً احتياطية من البيانات يومياً
- **التشفير:** استخدم HTTPS عند نقل البيانات

---

## 🛠️ الصيانة الدورية

### يومياً

- ✅ مراجعة لوحة المراقبة
- ✅ التحقق من التنبيهات
- ✅ فحص الطلبات الجديدة

### أسبوعياً

- ✅ مراجعة التقارير
- ✅ التحقق من حالة المخزون
- ✅ تحديث الأسعار إن لزم الأمر

### شهرياً

- ✅ تحليل البيانات الشهرية
- ✅ تحديث الإعدادات إذا لزم
- ✅ مراجعة الأداء والنتائج

---

## 📚 أمثلة عملية

### مثال 1: يوم عمل كامل

```python
from advanced_vantory_agent import AdvancedVantoryAgent
import json

# إنشاء الوكيل
agent = AdvancedVantoryAgent()

# 1. مزامنة الصباح (الساعة 9:00)
result = agent.sync_with_shopify()
print(f"✅ تمت معالجة {result['orders']['processed']} طلبات")

# 2. فحص المخزون (الساعة 12:00)
low_items = {sku: qty for sku, qty in agent.inventory.items() if qty < 20}
print(f"⚠️  {len(low_items)} منتجات قليلة المخزون")

# 3. تقرير الظهيرة (الساعة 15:00)
report = agent.generate_daily_report()
print(f"💰 الإيرادات حتى الآن: {report['summary']['total_revenue']} ريال")

# 4. التقرير النهائي (الساعة 23:00)
final_report = agent.generate_advanced_report()
with open("daily_report.json", "w", encoding="utf-8") as f:
    json.dump(final_report, f, ensure_ascii=False, indent=2, default=str)

# 5. حفظ الحالة
agent.save_state()
print("✅ تم حفظ جميع البيانات")
```

### مثال 2: التشغيل المستمر

```bash
# بدء المدير التلقائي
python auto_manager.py

# اختر: [1] بدء المدير (التشغيل)
# سيعمل 24/7 بدون تدخل
```

### مثال 3: المراقبة الحية مع التقارير

```bash
# افتح نافذة أولى: لوحة المراقبة
python live_dashboard.py

# افتح نافذة ثانية: المدير التلقائي
python auto_manager.py
```

---

## 🎯 الخطوات التالية

1. **تشغيل الاختبار الأول**
   ```bash
   python advanced_vantory_agent.py
   # اختر: [1] مزامنة واحدة مع Shopify
   ```

2. **تفعيل المراقبة المستمرة**
   ```bash
   python auto_manager.py
   # اختر: [1] بدء المدير (التشغيل)
   ```

3. **مراقبة الأداء**
   ```bash
   python live_dashboard.py
   # اختر: [1] عرض لوحة المراقبة الحية
   ```

---

## 📞 الدعم والمساعدة

| الموضوع | الحل |
|--------|------|
| أسئلة عامة | اطّلع على هذا الدليل |
| مشاكل الاتصال | تحقق من التوكن ورابط المتجر |
| أخطاء في المعالجة | راجع ملف `auto_manager.log` |
| مشاكل أداء | قلل فترة المزامنة أو أضف موارد أكثر |

---

## 📄 الملفات المرتبطة

- 📖 `VANTORY_GUIDE.md` - دليل Vantory الشامل
- 💻 `vantory_agent.py` - وكيل Vantory الأساسي
- 🔌 `shopify_connector.py` - الاتصال بـ Shopify
- 🚀 `advanced_vantory_agent.py` - التكامل الكامل
- 🤖 `auto_manager.py` - الإدارة الآلية
- 📊 `live_dashboard.py` - لوحة المراقبة
- ⚙️ `vantory_config.json` - الإعدادات

---

**آخر تحديث:** 2026-08-22  
**الإصدار:** 2.0.0 - مع الربط الكامل بـ Shopify  
**الحالة:** جاهز للإنتاج ✅

صُنع بـ ❤️ لنجاح متجرك!
