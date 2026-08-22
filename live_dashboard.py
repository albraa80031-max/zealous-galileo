#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════
    LIVE DASHBOARD - لوحة مراقبة فانتوري الحية
═══════════════════════════════════════════════════════════════
عرض حي وفوري لجميع عمليات المتجر وإحصائياته

المعلومات المعروضة:
  📊 إحصائيات المبيعات الحية
  📦 حالة المخزون الفورية
  💰 الإيرادات اليومية
  🚚 حالة الشحنات
  👥 آخر الطلبات
  ⚠️  التنبيهات والتحذيرات
  🔌 حالة الاتصال بـ Shopify
═══════════════════════════════════════════════════════════════
"""

import json
import logging
import time
import os
from datetime import datetime
from typing import Dict, List
from advanced_vantory_agent import AdvancedVantoryAgent

# إعداد السجلات
logging.basicConfig(level=logging.WARNING)  # تقليل ضوضاء السجلات للداشبورد


class LiveDashboard:
    """لوحة مراقبة متجر Vantory الحية"""

    def __init__(self, shop_url: str = "uk1msh-1p.myshopify.com",
                 api_token: str = "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",
                 config_path: str = "vantory_config.json"):
        """
        تهيئة لوحة المراقبة

        Args:
            shop_url: رابط المتجر
            api_token: توكن API
            config_path: مسار الإعدادات
        """
        self.agent = AdvancedVantoryAgent(shop_url, api_token, config_path)
        self.refresh_interval = 30  # ثانية
        self.is_running = False

    def clear_screen(self):
        """مسح الشاشة"""
        os.system('clear' if os.name == 'posix' else 'cls')

    def draw_box(self, title: str, content: str, width: int = 60) -> str:
        """رسم صندوق حول المحتوى"""
        lines = []
        lines.append("┌" + "─" * (width - 2) + "┐")
        lines.append(f"│ {title:<{width-4}} │")
        lines.append("├" + "─" * (width - 2) + "┤")

        for line in content.split("\n"):
            if line:
                padding = width - len(line) - 3
                lines.append(f"│ {line:<{padding}} │")

        lines.append("└" + "─" * (width - 2) + "┘")
        return "\n".join(lines)

    def get_sales_stats(self) -> str:
        """إحصائيات المبيعات"""
        report = self.agent.generate_daily_report()
        summary = report['summary']

        stats = f"""
📦 عدد الطلبات: {summary['total_orders']}
💰 الإيرادات: {summary['total_revenue']:.0f} ريال
📈 متوسط الطلب: {summary['average_order_value']:.0f} ريال
💵 الربح المتوقع: {report['profit_estimate']:.0f} ريال
"""
        return self.draw_box("📊 إحصائيات المبيعات", stats.strip())

    def get_inventory_status(self) -> str:
        """حالة المخزون"""
        inventory = self.agent.inventory
        total = sum(inventory.values())
        low_stock = {sku: qty for sku, qty in inventory.items() if qty < 20}
        critical = {sku: qty for sku, qty in inventory.items() if qty < 10}

        status_text = f"""
📦 إجمالي المخزون: {total} وحدة
⚠️  المنخفض (<20): {len(low_stock)} منتج
🔴 الحرج (<10): {len(critical)} منتج
"""

        if low_stock:
            status_text += "\n📋 المنتجات قليلة المخزون:\n"
            for sku, qty in list(low_stock.items())[:5]:
                product_name = self.agent._get_product_name(sku)
                status_text += f"  • {product_name}: {qty} وحدة\n"

        return self.draw_box("📦 حالة المخزون", status_text.strip())

    def get_recent_orders(self) -> str:
        """آخر الطلبات"""
        orders = list(self.agent.orders.values())[-5:]

        if not orders:
            return self.draw_box("🛒 آخر الطلبات", "لا توجد طلبات بعد")

        orders_text = ""
        for order in orders:
            orders_text += f"""
📌 #{order['id']}
   العميل: {order['customer_email']}
   المبلغ: {order['total_price']:.0f} ريال
   الحالة: {order['status']}
   ───────────────────
"""

        return self.draw_box("🛒 آخر الطلبات", orders_text.strip())

    def get_alerts(self) -> str:
        """التنبيهات والتحذيرات"""
        alerts = []

        # تنبيهات المخزون
        low_stock = {sku: qty for sku, qty in self.agent.inventory.items() if qty < 10}
        if low_stock:
            count = len(low_stock)
            alerts.append(f"🔴 {count} منتج/منتجات بمستوى حرج من المخزون!")

        # تنبيهات الطلبات
        if len(self.agent.orders) < 5 and len(self.agent.orders) > 0:
            alerts.append(f"⚠️  عدد الطلبات قليل: {len(self.agent.orders)} طلب فقط")

        # تنبيهات الاتصال
        if not self.agent.shopify.is_connected:
            alerts.append("❌ فقدان الاتصال بـ Shopify!")

        # الإيرادات
        if self.agent.daily_revenue == 0:
            alerts.append("📉 لا توجد إيرادات حتى الآن")

        if not alerts:
            alerts = ["✅ كل شيء يعمل بشكل طبيعي"]

        alerts_text = "\n".join(alerts)
        return self.draw_box("⚠️  التنبيهات", alerts_text)

    def get_connection_status(self) -> str:
        """حالة الاتصال"""
        shopify_status = "✅ متصل" if self.agent.shopify.is_connected else "❌ غير متصل"

        status_text = f"""
Shopify: {shopify_status}
الإصدار: {self.agent.shopify.api_version}
آخر مزامنة: {self.agent.sync_stats['last_sync'] or 'لم تتم'}
المتجر: {self.agent.shopify.shop_url}
"""
        return self.draw_box("🔌 حالة الاتصال", status_text.strip())

    def get_performance_metrics(self) -> str:
        """مقاييس الأداء"""
        uptime = "غير متوفر"
        if self.agent.sync_stats['last_sync']:
            # يمكن حساب وقت التشغيل من آخر مزامنة
            pass

        metrics_text = f"""
🔄 الطلبات المعالجة: {len(self.agent.processed_order_ids)}
📦 إجمالي المنتجات المراقبة: {len(self.agent.inventory)}
✅ المهام المكتملة: {len([t for t in self.agent.tasks.values() if t.get('status') == 'COMPLETED'])}
⏳ المهام المعلقة: {len([t for t in self.agent.tasks.values() if t.get('status') == 'PENDING'])}
"""
        return self.draw_box("⚡ مقاييس الأداء", metrics_text.strip())

    def render_dashboard(self):
        """عرض لوحة المراقبة الكاملة"""
        self.clear_screen()

        # الرأس
        print("\n" + "="*70)
        print("  🏪 لوحة مراقبة متجر Vantory الحية")
        print(f"  ⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70 + "\n")

        # الصناديق الرئيسية
        print(self.get_sales_stats())
        print()
        print(self.get_inventory_status())
        print()
        print(self.get_connection_status())
        print()
        print(self.get_performance_metrics())
        print()
        print(self.get_alerts())
        print()
        print(self.get_recent_orders())

        # التذييل
        print("\n" + "="*70)
        print(f"  🔄 التحديث التالي في {self.refresh_interval} ثانية")
        print("  اضغط Ctrl+C للخروج")
        print("="*70 + "\n")

    def start_live_monitoring(self, interval: int = 30):
        """
        بدء المراقبة الحية

        Args:
            interval: فترة التحديث بالثواني
        """
        self.refresh_interval = interval
        self.is_running = True

        try:
            while self.is_running:
                self.render_dashboard()
                time.sleep(interval)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """إيقاف المراقبة"""
        self.is_running = False
        self.clear_screen()
        print("\n✅ تم إيقاف لوحة المراقبة\n")

    def get_full_report(self) -> Dict:
        """الحصول على تقرير شامل"""
        return {
            "timestamp": datetime.now().isoformat(),
            "sales": self.agent.generate_daily_report(),
            "system_status": self.agent.get_full_status(),
            "sync_stats": self.agent.sync_stats
        }

    def export_report(self, filename: str = None) -> str:
        """تصدير التقرير إلى ملف"""
        if not filename:
            filename = f"dashboard_report_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"

        report = self.get_full_report()

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2, default=str)

        return filename


def main():
    """الدالة الرئيسية"""
    dashboard = LiveDashboard()

    print("\n" + "="*70)
    print("  🏪 لوحة مراقبة متجر Vantory الحية")
    print("="*70 + "\n")

    # عرض القائمة
    while True:
        print("📋 الخيارات:")
        print("  [1] عرض لوحة المراقبة الحية")
        print("  [2] تصدير تقرير فوري")
        print("  [3] عرض تقرير شامل")
        print("  [4] قائمة الطلبات الكاملة")
        print("  [0] خروج")
        print()

        choice = input("🎯 اختر خياراً: ").strip()

        if choice == "1":
            print("\n🔄 جاري بدء المراقبة الحية...")
            print("(اضغط Ctrl+C للعودة إلى القائمة)\n")
            dashboard.start_live_monitoring(interval=30)

        elif choice == "2":
            print("\n📊 جاري تصدير التقرير...")
            filename = dashboard.export_report()
            print(f"✅ تم حفظ التقرير في: {filename}")

        elif choice == "3":
            print("\n📈 التقرير الشامل:")
            report = dashboard.get_full_report()
            print(json.dumps(report, ensure_ascii=False, indent=2, default=str))

        elif choice == "4":
            print("\n📋 قائمة جميع الطلبات:")
            if not dashboard.agent.orders:
                print("  لا توجد طلبات")
            else:
                for order_id, order in dashboard.agent.orders.items():
                    print(f"\n  #{order_id}")
                    print(f"    العميل: {order['customer_email']}")
                    print(f"    المبلغ: {order['total_price']:.0f} ريال")
                    print(f"    الحالة: {order['status']}")
                    print(f"    عدد المنتجات: {len(order.get('items', []))}")

        elif choice == "0":
            print("\n👋 شكراً لاستخدام لوحة المراقبة!")
            break

        else:
            print("\n❌ اختيار غير صحيح\n")

        input("\nاضغط Enter للمتابعة...")


if __name__ == "__main__":
    main()
