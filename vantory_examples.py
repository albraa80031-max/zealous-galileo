#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أمثلة عملية لاستخدام Vantory Agent
Vantory Agent Practical Examples
"""

from vantory_agent import VantoryAgent
import json
import time


def example_1_process_real_orders():
    """مثال 1: معالجة طلبات حقيقية"""
    print("\n" + "="*60)
    print("  📦 مثال 1: معالجة الطلبات الحقيقية")
    print("="*60)

    agent = VantoryAgent()

    # طلبات حقيقية
    orders = [
        {
            "order_id": "ORD-2026-001",
            "customer_email": "ahmed@email.com",
            "items": [
                {"name": "Vantory Shield - Black", "sku": "VT-SHIELD-BLK", "quantity": 1, "price": 299.00}
            ],
            "total_price": 299.00
        },
        {
            "order_id": "ORD-2026-002",
            "customer_email": "fatima@email.com",
            "items": [
                {"name": "Vantory Slim - Grey", "sku": "VT-SLIM-GRY", "quantity": 2, "price": 199.00},
                {"name": "Vantory Shield - Silver", "sku": "VT-SHIELD-SLV", "quantity": 1, "price": 299.00}
            ],
            "total_price": 697.00
        },
        {
            "order_id": "ORD-2026-003",
            "customer_email": "mohammed@email.com",
            "items": [
                {"name": "Vantory Slim - Black", "sku": "VT-SLIM-BLK", "quantity": 3, "price": 199.00}
            ],
            "total_price": 597.00
        }
    ]

    print("\n✏️  معالجة 3 طلبات...")
    for order in orders:
        print(f"\n📦 الطلب: {order['order_id']}")
        print(f"   العميل: {order['customer_email']}")
        print(f"   المبلغ: {order['total_price']} ريال")

        agent.process_new_order(order)
        time.sleep(0.5)

    print("\n✅ تمت معالجة جميع الطلبات!")


def example_2_customer_inquiries():
    """مثال 2: معالجة استفسارات العملاء"""
    print("\n" + "="*60)
    print("  💬 مثال 2: معالجة استفسارات العملاء")
    print("="*60)

    agent = VantoryAgent()

    inquiries = [
        {
            "email": "client1@email.com",
            "subject": "سؤال عن المنتج",
            "message": "هل المحفظة مقاومة للماء والأتربة؟"
        },
        {
            "email": "client2@email.com",
            "subject": "مشكلة في الطلب",
            "message": "الطلب وصلني مكسور!"
        },
        {
            "email": "client3@email.com",
            "subject": "استفسار عن الشحن",
            "message": "كم المدة المتوقعة للشحن إلى الإمارات؟"
        }
    ]

    print("\n✏️  معالجة 3 استفسارات...")
    for inquiry in inquiries:
        print(f"\n💬 استفسار من: {inquiry['email']}")
        print(f"   الموضوع: {inquiry['subject']}")

        agent.handle_customer_inquiry(inquiry)
        time.sleep(0.5)

    print("\n✅ تمت معالجة جميع الاستفسارات!")


def example_3_daily_operations():
    """مثال 3: العمليات اليومية الكاملة"""
    print("\n" + "="*60)
    print("  ⚙️  مثال 3: العمليات اليومية الكاملة")
    print("="*60)

    agent = VantoryAgent()

    # 1. معالجة 5 طلبات
    print("\n1️⃣  معالجة الطلبات اليومية...")
    orders = [
        {"order_id": f"ORD-{i:04d}", "customer_email": f"customer{i}@email.com",
         "items": [{"name": f"Product {i}", "sku": f"SKU-{i}", "quantity": 1, "price": 299.00}],
         "total_price": 299.00}
        for i in range(1, 6)
    ]

    for order in orders:
        agent.process_new_order(order)

    print(f"   ✅ تمت معالجة {len(orders)} طلبات")

    # 2. جدولة الشحن
    print("\n2️⃣  جدولة الشحن...")
    for i in range(1, 6):
        agent.schedule_shipment(f"ORD-{i:04d}", "2026-08-24")

    print(f"   ✅ تمت جدولة {len(orders)} طلب للشحن")

    # 3. إنشاء التقرير اليومي
    print("\n3️⃣  إنشاء التقرير اليومي...")
    report = agent.generate_daily_report()

    print(f"\n   📊 ملخص التقرير:")
    print(f"   - عدد الطلبات: {report['summary']['total_orders']}")
    print(f"   - الإيرادات: {report['summary']['total_revenue']} ريال")
    print(f"   - متوسط الطلب: {report['summary']['average_order_value']:.2f} ريال")
    print(f"   - الربح المتوقع: {report['profit_estimate']:.2f} ريال")

    # 4. حفظ الحالة
    print("\n4️⃣  حفظ الحالة...")
    agent.save_state("vantory_daily_state.json")
    print("   ✅ تم حفظ جميع البيانات")

    print("\n✅ انتهت العمليات اليومية بنجاح!")


def example_4_inventory_management():
    """مثال 4: إدارة المخزون"""
    print("\n" + "="*60)
    print("  📦 مثال 4: إدارة المخزون")
    print("="*60)

    agent = VantoryAgent()

    print("\n📊 حالة المخزون الحالية:")
    print(json.dumps(agent.inventory, indent=2, ensure_ascii=False))

    # معالجة عدة طلبات لتقليل المخزون
    print("\n⚙️  معالجة طلبات متعددة...")
    orders = [
        {"order_id": "ORD-INV-001", "customer_email": "user@email.com",
         "items": [{"name": "Shield", "sku": "VT-SHIELD-BLK", "quantity": 25, "price": 299}],
         "total_price": 7475}
    ]

    for order in orders:
        agent.process_new_order(order)

    print("\n📊 حالة المخزون بعد المعالجة:")
    print(json.dumps(agent.inventory, indent=2, ensure_ascii=False))

    print("\n⚠️  المنتجات قليلة المخزون:")
    low_stock = {sku: qty for sku, qty in agent.inventory.items() if qty < 20}
    if low_stock:
        for sku, qty in low_stock.items():
            print(f"   - {sku}: {qty} وحدة")
    else:
        print("   ✅ جميع المنتجات بكميات كافية")


def example_5_analytics_and_reports():
    """مثال 5: التحليلات والتقارير"""
    print("\n" + "="*60)
    print("  📈 مثال 5: التحليلات والتقارير الشاملة")
    print("="*60)

    agent = VantoryAgent()

    # إضافة عدة طلبات
    print("\n📊 إنشاء بيانات للتحليل...")
    orders_data = [
        {"order_id": "ORD-A001", "customer_email": "user1@email.com",
         "items": [{"name": "Shield", "sku": "VT-SHIELD-BLK", "quantity": 2, "price": 299}],
         "total_price": 598},
        {"order_id": "ORD-A002", "customer_email": "user2@email.com",
         "items": [{"name": "Slim", "sku": "VT-SLIM-GRY", "quantity": 1, "price": 199}],
         "total_price": 199},
        {"order_id": "ORD-A003", "customer_email": "user3@email.com",
         "items": [{"name": "Shield", "sku": "VT-SHIELD-SLV", "quantity": 1, "price": 299},
                  {"name": "Slim", "sku": "VT-SLIM-BLK", "quantity": 1, "price": 199}],
         "total_price": 498},
    ]

    for order in orders_data:
        agent.process_new_order(order)

    # 1. التقرير اليومي
    print("\n1️⃣  التقرير اليومي:")
    daily_report = agent.generate_daily_report()
    print(f"   📦 عدد الطلبات: {daily_report['summary']['total_orders']}")
    print(f"   💰 الإيرادات: {daily_report['summary']['total_revenue']} ريال")
    print(f"   🏆 المنتج الأكثر مبيعاً: {daily_report['top_product']}")
    print(f"   📈 الربح المتوقع: {daily_report['profit_estimate']:.2f} ريال")

    # 2. التحليلات الشهرية
    print("\n2️⃣  التحليلات الشهرية:")
    monthly_analytics = agent.generate_monthly_analytics()
    print(f"   📅 الشهر: {monthly_analytics['month']}")
    print(f"   📊 إجمالي الطلبات: {monthly_analytics['total_orders']}")
    print(f"   💰 الإيرادات: {monthly_analytics['total_revenue']} ريال")
    print(f"   📈 الربح المتوقع: {monthly_analytics['projected_profit']:.2f} ريال")

    # 3. التوصيات
    print("\n3️⃣  التوصيات:")
    for rec in monthly_analytics['recommendations']:
        print(f"   {rec}")

    # 4. المهام المتبقية
    print("\n4️⃣  قائمة المهام:")
    pending_tasks = agent.list_tasks()
    for task in pending_tasks[:5]:  # أول 5 مهام
        print(f"   - {task['name']} [{task['status']}]")


def example_6_advanced_automation():
    """مثال 6: الأتمتة المتقدمة"""
    print("\n" + "="*60)
    print("  🤖 مثال 6: الأتمتة المتقدمة")
    print("="*60)

    agent = VantoryAgent()

    print("\n⚙️  تفعيل الأتمتة المتقدمة...")

    # 1. معالجة طلبات متعددة
    print("\n1️⃣  معالجة دفعة طلبات (Batch Processing)...")
    batch_orders = [
        {"order_id": f"BATCH-{i}", "customer_email": f"batch_user{i}@email.com",
         "items": [{"name": "Auto Product", "sku": f"AUTO-{i}", "quantity": 1, "price": 299}],
         "total_price": 299}
        for i in range(1, 4)
    ]

    for order in batch_orders:
        agent.process_new_order(order)

    print(f"   ✅ تمت معالجة {len(batch_orders)} طلب تلقائياً")

    # 2. التنبيهات الذكية
    print("\n2️⃣  التنبيهات الذكية...")
    agent._check_low_inventory()

    # 3. جدولة العمليات
    print("\n3️⃣  جدولة العمليات الدورية...")
    for i in range(1, 4):
        agent.schedule_shipment(f"BATCH-{i}", "2026-08-25")

    print(f"   ✅ تمت جدولة {len(batch_orders)} عملية")

    # 4. إنشاء التقارير
    print("\n4️⃣  إنشاء التقارير التلقائية...")
    report = agent.generate_daily_report()
    print(f"   ✅ تم إنشاء تقرير شامل")

    # 5. حفظ تلقائي
    print("\n5️⃣  الحفظ التلقائي...")
    agent.save_state("vantory_automation_state.json")
    print(f"   ✅ تم حفظ الحالة بنجاح")

    print("\n✅ انتهت الأتمتة المتقدمة!")


def main():
    """الدالة الرئيسية"""
    print("\n" + "="*60)
    print("  🏪 أمثلة عملية لـ Vantory Agent")
    print("="*60)

    examples = [
        ("معالجة الطلبات الحقيقية", example_1_process_real_orders),
        ("معالجة استفسارات العملاء", example_2_customer_inquiries),
        ("العمليات اليومية الكاملة", example_3_daily_operations),
        ("إدارة المخزون", example_4_inventory_management),
        ("التحليلات والتقارير", example_5_analytics_and_reports),
        ("الأتمتة المتقدمة", example_6_advanced_automation),
    ]

    print("\n📋 الأمثلة المتاحة:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  [{i}] {name}")
    print(f"  [{len(examples)+1}] تشغيل جميع الأمثلة")
    print(f"  [0] خروج")

    choice = input("\n🎯 اختر مثالاً: ").strip()

    try:
        choice = int(choice)
        if choice == 0:
            print("\n👋 شكراً لاستخدامك Vantory Agent!\n")
            return
        elif choice == len(examples) + 1:
            for _, example_func in examples:
                example_func()
                print("\n" + "="*60)
                time.sleep(1)
        elif 1 <= choice <= len(examples):
            examples[choice - 1][1]()
        else:
            print("  ❌ اختيار غير صحيح")
    except ValueError:
        print("  ❌ الرجاء إدخال رقم صحيح")

    print("\n✅ انتهت الأمثلة!")


if __name__ == "__main__":
    main()
