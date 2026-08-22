#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════
        كتالوج متجر Vantory - عرض المنتجات
═══════════════════════════════════════════════════════════════
عرض شامل لجميع منتجات المتجر مع التفاصيل الكاملة
"""

import json
from datetime import datetime

def load_catalog():
    """تحميل الكتالوج"""
    with open("products_catalog.json", "r", encoding="utf-8") as f:
        return json.load(f)

def print_header():
    """طباعة رأس الكتالوج"""
    print("\n" + "="*80)
    print("  🏪 كتالوج متجر Vantory الشامل")
    print("  📦 جميع المنتجات المتاحة")
    print(f"  ⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80 + "\n")

def print_category(category_name, products):
    """طباعة فئة من المنتجات"""
    print(f"\n{'─'*80}")
    print(f"  📂 {category_name}")
    print(f"{'─'*80}\n")

    for idx, product in enumerate(products, 1):
        print_product(idx, product)

def print_product(idx, product):
    """طباعة تفاصيل منتج واحد"""
    print(f"  {idx}. {product['name']}")
    print(f"     {'─'*70}")
    print(f"     📌 الكود: {product['id']}")
    print(f"     💰 السعر: {product['base_price']:.2f} درهم")
    print(f"     💳 السعر الأصلي: {product['compare_price']:.2f} درهم")

    # حساب الخصم
    discount = ((product['compare_price'] - product['base_price']) / product['compare_price']) * 100
    print(f"     🎯 الخصم: {discount:.0f}%")

    print(f"     💵 الربح: {product['profit_margin']*100:.0f}%")
    print(f"     📝 الوصف: {product['description']}")

    if 'rating' in product:
        print(f"     ⭐ التقييم: {product['rating']}/5 ({product['reviews']} تقييم)")

    if product['variants']:
        variants_str = " | ".join(product['variants'])
        print(f"     🎨 الألوان/الأنواع: {variants_str}")

    if 'features' in product:
        features_str = " • ".join(product['features'])
        print(f"     ✨ المميزات: {features_str}")

    print()

def print_statistics(catalog):
    """طباعة الإحصائيات"""
    stats = catalog['statistics']

    print("\n" + "="*80)
    print("  📊 إحصائيات المتجر")
    print("="*80 + "\n")

    print(f"  📦 إجمالي المنتجات: {stats['total_products']} منتج")
    print(f"  📂 إجمالي الفئات: {stats['total_categories']} فئة")
    print(f"  💰 متوسط السعر: {stats['average_price']:.2f} درهم")
    print(f"  ⭐ متوسط التقييم: {stats['average_rating']:.2f}/5")
    print(f"  📦 إجمالي المخزون: {stats['total_stock']:,} وحدة")
    print(f"  💵 قيمة المخزون الكلية: {stats['total_value_aed']:,.2f} درهم")

    print("\n" + "="*80 + "\n")

def print_categories_summary(catalog):
    """طباعة ملخص الفئات"""
    print(f"\n{'─'*80}")
    print("  📂 ملخص الفئات")
    print(f"{'─'*80}\n")

    for category in catalog['categories']:
        print(f"  {category['icon']} {category['name']:<20} ({category['count']} منتج)")

    print()

def show_by_category():
    """عرض المنتجات حسب الفئة"""
    catalog = load_catalog()
    print_header()

    # تنظيم المنتجات حسب الفئة
    by_category = {}
    for product in catalog['products']:
        category = product.get('category', 'غير مصنف')
        if category not in by_category:
            by_category[category] = []
        by_category[category].append(product)

    # طباعة كل فئة
    for category in ['محافظ', 'حقائب', 'إكسسوارات', 'مجموعات هدايا']:
        if category in by_category:
            print_category(category, by_category[category])

    print_statistics(catalog)

def show_all_products():
    """عرض جميع المنتجات"""
    catalog = load_catalog()
    print_header()

    products = catalog['products']
    for idx, product in enumerate(products, 1):
        print_product(idx, product)

    print_statistics(catalog)

def show_top_products():
    """عرض المنتجات الأعلى تقييماً"""
    catalog = load_catalog()
    print_header()

    # ترتيب المنتجات حسب التقييم
    products = sorted(
        [p for p in catalog['products'] if 'rating' in p],
        key=lambda x: x['rating'],
        reverse=True
    )

    print(f"\n{'─'*80}")
    print("  ⭐ أفضل المنتجات تقييماً")
    print(f"{'─'*80}\n")

    for idx, product in enumerate(products[:10], 1):
        print_product(idx, product)

def show_price_range():
    """عرض المنتجات حسب نطاق السعر"""
    catalog = load_catalog()
    print_header()

    products = sorted(catalog['products'], key=lambda x: x['base_price'])

    print(f"\n{'─'*80}")
    print("  💰 المنتجات مرتبة حسب السعر (من الأقل للأعلى)")
    print(f"{'─'*80}\n")

    for idx, product in enumerate(products, 1):
        print_product(idx, product)

def main():
    """الدالة الرئيسية"""
    print("\n" + "="*80)
    print("  🏪 كتالوج متجر Vantory")
    print("="*80)

    while True:
        print("\n📋 خيارات العرض:")
        print("  [1] عرض المنتجات حسب الفئة")
        print("  [2] عرض جميع المنتجات")
        print("  [3] أفضل المنتجات تقييماً")
        print("  [4] المنتجات مرتبة حسب السعر")
        print("  [0] خروج")
        print()

        choice = input("🎯 اختر خياراً: ").strip()

        if choice == "1":
            show_by_category()
        elif choice == "2":
            show_all_products()
        elif choice == "3":
            show_top_products()
        elif choice == "4":
            show_price_range()
        elif choice == "0":
            print("\n👋 شكراً لاستخدامك كتالوج Vantory!\n")
            break
        else:
            print("\n❌ اختيار غير صحيح\n")

if __name__ == "__main__":
    main()
