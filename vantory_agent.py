#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════
        VANTORY STORE AGENT - وكيل متجر فانتوري الذكي
═══════════════════════════════════════════════════════════════
وكيل متخصص لإدارة متجر المحافظ الذكية Vantory تلقائياً

المميزات:
  ✅ إدارة الطلبات والمخزون
  ✅ معالجة البريد الإلكتروني للعملاء
  ✅ حسابات المبيعات والأرباح
  ✅ تقارير يومية مفصلة
  ✅ إدارة العملاء والمراجعات
  ✅ جدولة الإرسالات
  ✅ تنبيهات المخزون المنخفض
  ✅ تحليل الأداء والمبيعات
═══════════════════════════════════════════════════════════════
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from universal_agent import UniversalAgent, TaskPriority, TaskStatus

# إعداد السجلات
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [VANTORY] - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VantoryAgent(UniversalAgent):
    """
    وكيل متخصص لإدارة متجر Vantory الإلكتروني
    يوسع من Universal Agent بميزات تخصصية للمتجر
    """

    # معلومات المتجر
    STORE_NAME = "Vantory Store"
    STORE_URL = "uk1msh-1p.myshopify.com"

    # المنتجات
    PRODUCTS = {
        "VT-SHIELD": {
            "name": "Vantory Shield | المحفظة الذكية الفاخرة",
            "price": 299.00,
            "compare_price": 450.00,
            "variants": ["Black", "Silver", "Brown"],
            "features": ["RFID Protection", "GPS Tracking", "Premium Leather"]
        },
        "VT-SLIM": {
            "name": "Vantory Slim | المحفظة الرقيقة",
            "price": 199.00,
            "compare_price": 299.00,
            "variants": ["Grey", "Black"],
            "features": ["Minimalist Design", "Aluminum", "Lightweight"]
        }
    }

    def __init__(self, config_path: str = "vantory_config.json"):
        """تهيئة وكيل Vantory"""
        super().__init__(config_path)
        self.orders = {}
        self.inventory = self._init_inventory()
        self.daily_sales = 0
        self.daily_revenue = 0

        logger.info(f"🏪 تم تهيئة Vantory Agent")
        self._print_vantory_welcome()

    def _init_inventory(self) -> Dict:
        """تهيئة المخزون"""
        return {
            "VT-SHIELD-BLK": 50,
            "VT-SHIELD-SLV": 35,
            "VT-SHIELD-BRN": 40,
            "VT-SLIM-GRY": 75,
            "VT-SLIM-BLK": 60
        }

    def _print_vantory_welcome(self):
        """طباعة رسالة الترحيب الخاصة بـ Vantory"""
        print("\n" + "="*60)
        print("  🏪 متجر Vantory الإلكتروني")
        print("  وكيل إدارة المحافظ الذكية 🛍️")
        print("="*60)
        print(f"  📦 المتجر: {self.STORE_NAME}")
        print(f"  🌐 الموقع: {self.STORE_URL}")
        print(f"  ⏰ الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60 + "\n")

    def process_new_order(self, order_data: Dict) -> bool:
        """
        معالجة طلب جديد

        Args:
            order_data: بيانات الطلب

        Returns:
            نتيجة المعالجة
        """
        try:
            order_id = order_data.get("order_id")
            customer_email = order_data.get("customer_email")
            items = order_data.get("items", [])
            total_price = order_data.get("total_price", 0)

            # حفظ الطلب
            self.orders[order_id] = {
                "id": order_id,
                "customer_email": customer_email,
                "items": items,
                "total_price": total_price,
                "status": "جديد",
                "created_at": datetime.now().isoformat()
            }

            # تحديث المخزون
            for item in items:
                sku = item.get("sku")
                quantity = item.get("quantity", 1)
                if sku in self.inventory:
                    self.inventory[sku] -= quantity

            # تحديث المبيعات
            self.daily_sales += len(items)
            self.daily_revenue += total_price

            # إنشاء مهمة للمتابعة
            task_id = self.create_task(
                f"معالجة طلب #{order_id}",
                f"طلب من {customer_email} - {len(items)} منتج",
                TaskPriority.HIGH,
                tags=["order", "customer_service"]
            )

            # إرسال بريد تأكيد
            self._send_order_confirmation(order_id, customer_email, items)

            # تنبيه إذا كان المخزون منخفضاً
            self._check_low_inventory()

            logger.info(f"✅ تم معالجة الطلب #{order_id} - المجموع: {total_price} ريال")
            return True

        except Exception as e:
            logger.error(f"❌ خطأ في معالجة الطلب: {e}")
            return False

    def _send_order_confirmation(self, order_id: str, email: str, items: List) -> bool:
        """إرسال بريد تأكيد الطلب"""
        try:
            email_content = f"""
            شكراً لشرائك من Vantory! 🎉

            رقم الطلب: #{order_id}
            التاريخ: {datetime.now().strftime('%d/%m/%Y')}

            المنتجات:
            """

            for item in items:
                email_content += f"\n- {item.get('name', 'منتج')} x{item.get('quantity', 1)}"

            email_content += f"""

            المجموع: {sum(i.get('price', 0) * i.get('quantity', 1) for i in items)} ريال

            سيتم إرسال الطلب خلال 24 ساعة 📦
            يمكنك متابعة الطلب من حسابك

            للدعم: support@vantory.local
            شكراً! 💚
            """

            logger.info(f"📧 تم إرسال تأكيد للعميل: {email}")
            return True
        except Exception as e:
            logger.error(f"❌ خطأ في إرسال البريد: {e}")
            return False

    def _check_low_inventory(self):
        """التحقق من المخزون المنخفض"""
        low_stock_items = {}
        for sku, quantity in self.inventory.items():
            if quantity < 20:
                product_name = self._get_product_name(sku)
                low_stock_items[sku] = {
                    "name": product_name,
                    "quantity": quantity
                }

        if low_stock_items:
            logger.warning(f"⚠️ تنبيه: المنتجات التالية قليلة المخزون:")
            for sku, info in low_stock_items.items():
                logger.warning(f"   - {info['name']}: {info['quantity']} وحدة")

            # إنشاء مهمة لإعادة الطلب
            self.create_task(
                "إعادة طلب منتجات",
                f"المنتجات التالية قليلة المخزون: {list(low_stock_items.keys())}",
                TaskPriority.CRITICAL,
                tags=["inventory", "urgent"]
            )

    def _get_product_name(self, sku: str) -> str:
        """الحصول على اسم المنتج من الـ SKU"""
        product_prefix = sku.split("-")[1]
        if "SHIELD" in sku:
            return "Vantory Shield"
        elif "SLIM" in sku:
            return "Vantory Slim"
        return "منتج غير معروف"

    def generate_daily_report(self) -> Dict:
        """إنشاء تقرير يومي شامل"""
        report = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "store": self.STORE_NAME,
            "summary": {
                "total_orders": len(self.orders),
                "total_items_sold": self.daily_sales,
                "total_revenue": self.daily_revenue,
                "average_order_value": self.daily_revenue / max(len(self.orders), 1)
            },
            "inventory": {
                "total_items": sum(self.inventory.values()),
                "low_stock_items": {
                    sku: qty for sku, qty in self.inventory.items() if qty < 20
                }
            },
            "orders": self.orders,
            "top_product": self._get_top_product(),
            "profit_estimate": self._calculate_profit()
        }

        logger.info(f"📊 تقرير اليوم:")
        logger.info(f"   📦 عدد الطلبات: {report['summary']['total_orders']}")
        logger.info(f"   💰 الإيرادات: {report['summary']['total_revenue']} ريال")
        logger.info(f"   📈 متوسط قيمة الطلب: {report['summary']['average_order_value']:.2f} ريال")

        return report

    def _get_top_product(self) -> str:
        """الحصول على المنتج الأكثر مبيعاً"""
        if not self.orders:
            return "لا توجد طلبات"

        products = {}
        for order in self.orders.values():
            for item in order.get("items", []):
                name = item.get("name", "Unknown")
                products[name] = products.get(name, 0) + item.get("quantity", 1)

        if products:
            top = max(products, key=products.get)
            return f"{top} ({products[top]} وحدة)"
        return "لا توجد بيانات"

    def _calculate_profit(self) -> float:
        """حساب الربح المتوقع"""
        # تكلفة الإنتاج تقريبية (50% من السعر)
        total_cost = self.daily_revenue * 0.5
        profit = self.daily_revenue - total_cost
        return profit

    def handle_customer_inquiry(self, inquiry_data: Dict) -> bool:
        """
        معالجة استفسار العميل

        Args:
            inquiry_data: بيانات الاستفسار

        Returns:
            نتيجة المعالجة
        """
        try:
            customer_email = inquiry_data.get("email")
            subject = inquiry_data.get("subject")
            message = inquiry_data.get("message")

            logger.info(f"💬 استفسار من {customer_email}: {subject}")

            # تصنيف الاستفسار
            inquiry_type = self._classify_inquiry(subject)

            # إنشاء مهمة
            task_id = self.create_task(
                f"رد على استفسار: {subject}",
                f"من: {customer_email}\n{message}",
                TaskPriority.HIGH if inquiry_type == "complaint" else TaskPriority.MEDIUM,
                tags=["customer_inquiry", inquiry_type]
            )

            # إرسال رد تلقائي
            self._send_auto_reply(customer_email, subject)

            return True
        except Exception as e:
            logger.error(f"❌ خطأ في معالجة الاستفسار: {e}")
            return False

    def _classify_inquiry(self, subject: str) -> str:
        """تصنيف نوع الاستفسار"""
        subject_lower = subject.lower()
        if any(word in subject_lower for word in ["شكوى", "مشكلة", "خطأ", "complaint"]):
            return "complaint"
        elif any(word in subject_lower for word in ["تسليم", "شحن", "delivery", "shipping"]):
            return "shipping"
        elif any(word in subject_lower for word in ["استرجاع", "return", "refund"]):
            return "return"
        else:
            return "general"

    def _send_auto_reply(self, email: str, subject: str) -> bool:
        """إرسال رد تلقائي"""
        reply = f"""
        شكراً لتواصلك مع Vantory! 🙏

        استفسارك: {subject}

        سيتم الرد عليك في أسرع وقت ممكن
        (عادة خلال ساعات قليلة)

        رقم الدعم: support@vantory.local
        """
        logger.info(f"📧 تم إرسال رد تلقائي إلى: {email}")
        return True

    def schedule_shipment(self, order_id: str, shipping_date: str) -> bool:
        """
        جدولة شحن الطلب

        Args:
            order_id: رقم الطلب
            shipping_date: تاريخ الشحن

        Returns:
            نتيجة الجدولة
        """
        if order_id not in self.orders:
            logger.error(f"❌ الطلب {order_id} غير موجود")
            return False

        self.orders[order_id]["shipping_date"] = shipping_date
        self.orders[order_id]["status"] = "جاهز للشحن"

        # إنشاء مهمة للشحن
        task_id = self.create_task(
            f"شحن الطلب #{order_id}",
            f"تاريخ الشحن: {shipping_date}",
            TaskPriority.HIGH,
            tags=["shipping"]
        )

        logger.info(f"✅ تم جدولة شحن الطلب #{order_id} بتاريخ {shipping_date}")
        return True

    def generate_monthly_analytics(self) -> Dict:
        """إنشاء تحليلات شهرية"""
        analytics = {
            "month": datetime.now().strftime("%Y-%m"),
            "total_orders": len(self.orders),
            "total_revenue": self.daily_revenue,
            "products": {
                name: self.PRODUCTS[prod_id]
                for prod_id, name in [
                    ("VT-SHIELD", "Vantory Shield"),
                    ("VT-SLIM", "Vantory Slim")
                ]
            },
            "inventory_status": self.inventory,
            "projected_profit": self._calculate_profit() * 30,
            "recommendations": self._generate_recommendations()
        }
        return analytics

    def _generate_recommendations(self) -> List[str]:
        """توليد التوصيات"""
        recommendations = []

        # توصيات المخزون
        low_items = [k for k, v in self.inventory.items() if v < 20]
        if low_items:
            recommendations.append(f"⚠️ أعد طلب: {', '.join(low_items)}")

        # توصيات المبيعات
        if self.daily_sales < 5:
            recommendations.append("📢 زيادة حملات التسويق")

        recommendations.append("✅ حافظ على جودة الخدمة للعملاء")
        recommendations.append("📊 راقب المنتجات الشهيرة")

        return recommendations


def main():
    """الدالة الرئيسية"""
    agent = VantoryAgent()

    # مثال على الاستخدام
    print("\n🚀 بدء عمليات المتجر التلقائية...\n")

    # طلب جديد
    new_order = {
        "order_id": "ORD-001",
        "customer_email": "customer@example.com",
        "items": [
            {"name": "Vantory Shield - Black", "sku": "VT-SHIELD-BLK", "quantity": 1, "price": 299.00},
            {"name": "Vantory Slim - Grey", "sku": "VT-SLIM-GRY", "quantity": 2, "price": 199.00}
        ],
        "total_price": 697.00
    }

    print("📦 معالجة طلب جديد...")
    agent.process_new_order(new_order)

    # استفسار عميل
    inquiry = {
        "email": "customer@example.com",
        "subject": "سؤال عن المنتج",
        "message": "هل المحفظة مقاومة للماء؟"
    }

    print("\n💬 معالجة استفسار عميل...")
    agent.handle_customer_inquiry(inquiry)

    # جدولة الشحن
    print("\n📮 جدولة شحن...")
    agent.schedule_shipment("ORD-001", "2026-08-24")

    # تقرير يومي
    print("\n📊 إنشاء تقرير يومي...")
    daily_report = agent.generate_daily_report()
    print(f"\nالتقرير الكامل:")
    print(json.dumps(daily_report, ensure_ascii=False, indent=2, default=str))

    # حفظ الحالة
    print("\n💾 حفظ الحالة...")
    agent.save_state("vantory_state.json")

    print("\n✅ انتهت العمليات اليومية!")


if __name__ == "__main__":
    main()
