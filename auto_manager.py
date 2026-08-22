#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════
    AUTO MANAGER - مدير المتجر التلقائي 24/7
═══════════════════════════════════════════════════════════════
نظام إدارة متجر Vantory بالكامل بدون تدخل يدوي

المهام الآلية:
  ✅ معالجة الطلبات الجديدة (كل ساعة)
  ✅ تحديث المخزون (كل 6 ساعات)
  ✅ فحص المخزون المنخفض (كل 6 ساعات)
  ✅ إنشاء الفواتير (كل 30 دقيقة)
  ✅ جدولة الشحن (كل ساعة)
  ✅ إرسال التقارير اليومية (الساعة 23:00)
  ✅ حفظ الحالة (كل ساعة)
═══════════════════════════════════════════════════════════════
"""

import json
import logging
import time
import schedule
from datetime import datetime, timedelta
from typing import Dict, Any
from advanced_vantory_agent import AdvancedVantoryAgent

# إعداد السجلات
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [AUTO-MANAGER] - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("auto_manager.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AutoManager:
    """
    مدير متجر Vantory التلقائي
    يدير جميع العمليات بشكل مستقل 24/7
    """

    def __init__(self, shop_url: str = "uk1msh-1p.myshopify.com",
                 api_token: str = "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",
                 config_path: str = "vantory_config.json"):
        """
        تهيئة مدير المتجر التلقائي

        Args:
            shop_url: رابط المتجر
            api_token: توكن API
            config_path: مسار الإعدادات
        """
        self.agent = AdvancedVantoryAgent(shop_url, api_token, config_path)
        self.is_running = False
        self.start_time = None
        self.job_history = []

        logger.info("✅ تم تهيئة Auto Manager")
        self._setup_schedule()

    def _setup_schedule(self):
        """إعداد جدول المهام الآلية"""
        logger.info("📋 إعداد جدول المهام...")

        # معالجة الطلبات كل ساعة
        schedule.every().hour.do(self._job_process_orders)

        # فحص المخزون كل 6 ساعات
        schedule.every(6).hours.do(self._job_check_inventory)

        # تحديث المخزون كل 6 ساعات
        schedule.every(6).hours.do(self._job_sync_inventory)

        # إنشاء الفواتير كل 30 دقيقة
        schedule.every(30).minutes.do(self._job_create_invoices)

        # جدولة الشحن كل ساعة
        schedule.every().hour.do(self._job_schedule_shipments)

        # التقرير اليومي الساعة 23:00
        schedule.every().day.at("23:00").do(self._job_daily_report)

        # حفظ الحالة كل ساعة
        schedule.every().hour.do(self._job_save_state)

        # فحص الاتصال كل 30 دقيقة
        schedule.every(30).minutes.do(self._job_verify_connection)

        logger.info("✅ تم إعداد جدول المهام بنجاح")

    def _log_job(self, job_name: str, status: str, details: str = ""):
        """تسجيل تنفيذ المهمة"""
        job_record = {
            "timestamp": datetime.now().isoformat(),
            "job": job_name,
            "status": status,
            "details": details
        }
        self.job_history.append(job_record)
        logger.info(f"📋 [{job_name}] {status}: {details}")

    # ═════════════════════════════════════════════════════════════
    # المهام الآلية
    # ═════════════════════════════════════════════════════════════

    def _job_process_orders(self):
        """معالجة الطلبات الجديدة"""
        try:
            logger.info("🔄 [معالجة الطلبات] بدء العملية...")
            result = self.agent.sync_with_shopify()

            if result["success"]:
                self._log_job(
                    "معالجة الطلبات",
                    "✅ نجحت",
                    f"تمت معالجة {result['orders']['processed']} طلب"
                )
            else:
                self._log_job(
                    "معالجة الطلبات",
                    "❌ فشلت",
                    f"أخطاء: {result['orders']['errors']}"
                )
        except Exception as e:
            self._log_job("معالجة الطلبات", "❌ خطأ", str(e))

    def _job_check_inventory(self):
        """فحص المخزون المنخفض"""
        try:
            logger.info("🔄 [فحص المخزون] بدء العملية...")
            self.agent._check_low_inventory()

            low_items = {sku: qty for sku, qty in self.agent.inventory.items() if qty < 20}

            self._log_job(
                "فحص المخزون",
                "✅ انتهى",
                f"عدد المنتجات قليلة المخزون: {len(low_items)}"
            )
        except Exception as e:
            self._log_job("فحص المخزون", "❌ خطأ", str(e))

    def _job_sync_inventory(self):
        """مزامنة المخزون مع Shopify"""
        try:
            logger.info("🔄 [مزامنة المخزون] بدء العملية...")

            # سحب المنتجات من Shopify
            products = self.agent.shopify.get_products()

            self._log_job(
                "مزامنة المخزون",
                "✅ انتهت",
                f"تمت مزامنة {len(products)} منتج"
            )
        except Exception as e:
            self._log_job("مزامنة المخزون", "❌ خطأ", str(e))

    def _job_create_invoices(self):
        """إنشاء الفواتير للطلبات الجديدة"""
        try:
            logger.info("🔄 [إنشاء الفواتير] بدء العملية...")

            # إنشاء مهام للفواتير
            new_orders = [o for o in self.agent.orders.values() if o.get("status") == "جديد"]

            for order in new_orders:
                task_id = self.agent.create_task(
                    f"فاتورة الطلب #{order['id']}",
                    f"إنشاء فاتورة للعميل {order['customer_email']}",
                    priority=2  # HIGH
                )

            self._log_job(
                "إنشاء الفواتير",
                "✅ انتهت",
                f"تم إنشاء {len(new_orders)} فاتورة"
            )
        except Exception as e:
            self._log_job("إنشاء الفواتير", "❌ خطأ", str(e))

    def _job_schedule_shipments(self):
        """جدولة الشحن للطلبات المعالجة"""
        try:
            logger.info("🔄 [جدولة الشحن] بدء العملية...")

            # البحث عن الطلبات التي لم يتم جدولة شحنها
            scheduled_count = 0

            for order_id, order in self.agent.orders.items():
                if order.get("status") == "جديد" and "shipping_date" not in order:
                    # جدولة الشحن للغد
                    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
                    if self.agent.schedule_shipment(order_id, tomorrow):
                        scheduled_count += 1

            self._log_job(
                "جدولة الشحن",
                "✅ انتهت",
                f"تمت جدولة {scheduled_count} طلب"
            )
        except Exception as e:
            self._log_job("جدولة الشحن", "❌ خطأ", str(e))

    def _job_daily_report(self):
        """إنشاء التقرير اليومي"""
        try:
            logger.info("🔄 [التقرير اليومي] بدء العملية...")

            # إنشاء التقرير المتقدم
            report = self.agent.generate_advanced_report()

            # حفظ التقرير
            report_filename = f"report_{datetime.now().strftime('%Y-%m-%d')}.json"
            with open(report_filename, "w", encoding="utf-8") as f:
                json.dump(report, f, ensure_ascii=False, indent=2, default=str)

            # طباعة ملخص التقرير
            logger.info("📊 ملخص التقرير اليومي:")
            logger.info(f"   📦 عدد الطلبات: {report['summary']['total_orders']}")
            logger.info(f"   💰 الإيرادات: {report['summary']['total_revenue']} ريال")
            logger.info(f"   📈 متوسط الطلب: {report['summary']['average_order_value']:.2f} ريال")
            logger.info(f"   💵 الربح المتوقع: {report['profit_estimate']:.2f} ريال")

            self._log_job(
                "التقرير اليومي",
                "✅ انتهى",
                f"تم حفظ التقرير في {report_filename}"
            )
        except Exception as e:
            self._log_job("التقرير اليومي", "❌ خطأ", str(e))

    def _job_save_state(self):
        """حفظ حالة النظام"""
        try:
            logger.info("🔄 [حفظ الحالة] بدء العملية...")
            self.agent.save_state()
            self._log_job("حفظ الحالة", "✅ انتهى", "تم حفظ جميع البيانات")
        except Exception as e:
            self._log_job("حفظ الحالة", "❌ خطأ", str(e))

    def _job_verify_connection(self):
        """التحقق من الاتصال بـ Shopify"""
        try:
            if self.agent.shopify.is_connected:
                self._log_job("التحقق من الاتصال", "✅ متصل", "الاتصال بـ Shopify سليم")
            else:
                logger.warning("⚠️ الاتصال بـ Shopify مقطوع!")
                self._log_job("التحقق من الاتصال", "❌ غير متصل", "فشل الاتصال")
        except Exception as e:
            self._log_job("التحقق من الاتصال", "❌ خطأ", str(e))

    # ═════════════════════════════════════════════════════════════
    # التحكم في المدير
    # ═════════════════════════════════════════════════════════════

    def start(self):
        """بدء المدير التلقائي"""
        if self.is_running:
            logger.warning("⚠️ المدير يعمل بالفعل")
            return

        self.is_running = True
        self.start_time = datetime.now()

        logger.info("="*60)
        logger.info("🚀 بدء مدير Vantory التلقائي 24/7")
        logger.info(f"⏰ وقت البدء: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("="*60)

        # تنفيذ المهام المجدولة
        try:
            while self.is_running:
                schedule.run_pending()
                time.sleep(60)  # فحص المهام كل دقيقة
        except KeyboardInterrupt:
            logger.info("\n🛑 تم الإيقاف من قبل المستخدم")
            self.stop()

    def stop(self):
        """إيقاف المدير التلقائي"""
        if not self.is_running:
            logger.warning("⚠️ المدير غير مشغل")
            return

        self.is_running = False
        logger.info("🛑 جاري إيقاف المدير...")

        # حفظ الحالة النهائية
        self.agent.save_state()

        # طباعة الإحصائيات
        self._print_statistics()

        logger.info("✅ تم إيقاف المدير بنجاح")

    def _print_statistics(self):
        """طباعة إحصائيات التشغيل"""
        if not self.start_time:
            return

        uptime = datetime.now() - self.start_time
        hours = uptime.total_seconds() / 3600

        logger.info("\n" + "="*60)
        logger.info("📊 إحصائيات التشغيل:")
        logger.info("="*60)
        logger.info(f"⏱️  وقت التشغيل: {uptime}")
        logger.info(f"📦 عدد الطلبات المعالجة: {len(self.agent.orders)}")
        logger.info(f"💰 إجمالي الإيرادات: {self.agent.daily_revenue} ريال")
        logger.info(f"📈 متوسط الإيرادات بالساعة: {self.agent.daily_revenue / max(hours, 1):.2f} ريال")
        logger.info(f"✅ إجمالي المهام: {len(self.agent.tasks)}")
        logger.info(f"🔄 عدد مهام المزامنة: {len([j for j in self.job_history if 'مزامنة' in j.get('job', '')])}")
        logger.info("="*60 + "\n")

    def get_status(self) -> Dict:
        """الحصول على حالة المدير"""
        uptime = None
        if self.start_time:
            uptime = str(datetime.now() - self.start_time)

        return {
            "running": self.is_running,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "uptime": uptime,
            "agent_status": self.agent.get_full_status(),
            "recent_jobs": self.job_history[-10:] if self.job_history else []
        }

    def print_menu(self):
        """طباعة القائمة التفاعلية"""
        print("\n" + "="*60)
        print("  🤖 مدير Vantory التلقائي 24/7")
        print("="*60)
        print("  [1] بدء المدير (التشغيل)")
        print("  [2] عرض الحالة الحالية")
        print("  [3] تنفيذ مزامنة يدوية")
        print("  [4] إنشاء تقرير")
        print("  [5] عرض سجل المهام")
        print("  [6] إيقاف المدير والخروج")
        print("  [0] خروج فوري")
        print("="*60)


def main():
    """الدالة الرئيسية"""
    print("\n" + "="*70)
    print("  🤖 مدير متجر Vantory التلقائي 24/7")
    print("  إدارة كاملة للمتجر بدون تدخل يدوي")
    print("="*70 + "\n")

    # إنشاء المدير
    manager = AutoManager()

    # القائمة التفاعلية (في الخلفية)
    # بدء المدير بشكل افتراضي
    import threading

    # خيط للمدير الرئيسي
    manager_thread = threading.Thread(target=manager.start, daemon=False)

    # خيط للقائمة التفاعلية
    def interactive_menu():
        """القائمة التفاعلية"""
        while manager.is_running:
            try:
                manager.print_menu()
                choice = input("\n🎯 اختر خياراً: ").strip()

                if choice == "1":
                    if not manager.is_running:
                        print("✅ المدير مشغل بالفعل")
                    else:
                        print("✅ المدير مشغل الآن")

                elif choice == "2":
                    status = manager.get_status()
                    print("\n📊 حالة النظام:")
                    print(json.dumps(status, ensure_ascii=False, indent=2, default=str))

                elif choice == "3":
                    print("\n🔄 جاري تنفيذ مزامنة يدوية...")
                    result = manager.agent.sync_with_shopify()
                    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))

                elif choice == "4":
                    print("\n📈 إنشاء تقرير...")
                    report = manager.agent.generate_advanced_report()
                    report_file = f"manual_report_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
                    with open(report_file, "w", encoding="utf-8") as f:
                        json.dump(report, f, ensure_ascii=False, indent=2, default=str)
                    print(f"✅ تم حفظ التقرير في {report_file}")

                elif choice == "5":
                    print("\n📋 سجل آخر 10 مهام:")
                    for job in manager.job_history[-10:]:
                        print(f"  [{job['timestamp']}] {job['job']}: {job['status']} - {job['details']}")

                elif choice == "6":
                    print("\n🛑 إيقاف المدير والخروج...")
                    manager.stop()
                    break

                elif choice == "0":
                    print("\n🛑 خروج فوري...")
                    manager.is_running = False
                    break

                else:
                    print("\n❌ اختيار غير صحيح")

                time.sleep(0.5)

            except KeyboardInterrupt:
                print("\n\n🛑 إيقاف...")
                break
            except Exception as e:
                logger.error(f"❌ خطأ: {e}")

    # بدء الخيوط
    manager_thread.start()
    time.sleep(1)  # انتظر قليلاً ليبدأ المدير

    try:
        interactive_menu()
    except KeyboardInterrupt:
        logger.info("\n🛑 تم الإيقاف")
        manager.stop()

    # انتظار انتهاء الخيط
    manager_thread.join(timeout=10)

    logger.info("✅ انتهى المدير بنجاح")


if __name__ == "__main__":
    main()
