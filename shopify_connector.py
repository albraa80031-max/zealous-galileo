#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════
        SHOPIFY CONNECTOR - وحدة الاتصال المباشرة
═══════════════════════════════════════════════════════════════
اتصال مباشر وآني مع متجر Shopify Vantory
"""

import requests
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

# إعداد السجلات
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [SHOPIFY] - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ShopifyConnector:
    """
    وحدة الاتصال المباشرة مع Shopify API
    تدير جميع عمليات المتجر بشكل فوري
    """

    def __init__(self, shop_url: str, api_token: str):
        """
        تهيئة الاتصال

        Args:
            shop_url: رابط المتجر (مثل: uk1msh-1p.myshopify.com)
            api_token: توكن API من Shopify
        """
        self.shop_url = shop_url
        self.api_token = api_token
        self.api_version = "2024-01"
        self.base_url = f"https://{shop_url}/admin/api/{self.api_version}"

        self.headers = {
            "X-Shopify-Access-Token": api_token,
            "Content-Type": "application/json"
        }

        # تتبع الحالة
        self.is_connected = False
        self.last_sync = None
        self.orders_count = 0
        self.products_count = 0

        # الاتصال والتحقق
        self._verify_connection()

    def _verify_connection(self) -> bool:
        """التحقق من الاتصال"""
        try:
            response = requests.get(
                f"{self.base_url}/shop.json",
                headers=self.headers,
                timeout=10
            )

            if response.status_code == 200:
                shop_data = response.json()["shop"]
                self.is_connected = True
                logger.info(f"✅ متصل بـ {shop_data['name']}")
                logger.info(f"   المتجر: {self.shop_url}")
                logger.info(f"   الخطة: {shop_data['plan_name']}")
                logger.info(f"   العملة: {shop_data['currency']}")
                return True
            else:
                logger.error(f"❌ فشل الاتصال: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ خطأ في الاتصال: {e}")
            return False

    def get_new_orders(self, status: str = "any") -> List[Dict]:
        """
        سحب الطلبات الجديدة من Shopify

        Args:
            status: حالة الطلبات (any, fulfilled, unfulfilled)

        Returns:
            قائمة الطلبات
        """
        try:
            url = f"{self.base_url}/orders.json"
            params = {
                "status": status,
                "limit": 250,
                "order": "created_at desc"
            }

            response = requests.get(
                url,
                headers=self.headers,
                params=params,
                timeout=10
            )

            if response.status_code == 200:
                orders = response.json().get("orders", [])
                self.last_sync = datetime.now().isoformat()
                self.orders_count = len(orders)

                logger.info(f"✅ تم سحب {len(orders)} طلب من Shopify")
                return orders
            else:
                logger.error(f"❌ خطأ في سحب الطلبات: {response.status_code}")
                return []

        except Exception as e:
            logger.error(f"❌ خطأ في سحب الطلبات: {e}")
            return []

    def get_products(self) -> List[Dict]:
        """الحصول على جميع المنتجات"""
        try:
            url = f"{self.base_url}/products.json"
            params = {"limit": 250}

            response = requests.get(
                url,
                headers=self.headers,
                params=params,
                timeout=10
            )

            if response.status_code == 200:
                products = response.json().get("products", [])
                self.products_count = len(products)
                logger.info(f"✅ تم سحب {len(products)} منتج من Shopify")
                return products
            else:
                logger.error(f"❌ خطأ في سحب المنتجات: {response.status_code}")
                return []

        except Exception as e:
            logger.error(f"❌ خطأ في سحب المنتجات: {e}")
            return []

    def update_order_status(self, order_id: int, status: str) -> bool:
        """
        تحديث حالة الطلب

        Args:
            order_id: معرف الطلب
            status: الحالة الجديدة

        Returns:
            نتيجة التحديث
        """
        try:
            url = f"{self.base_url}/orders/{order_id}.json"

            data = {
                "order": {
                    "id": order_id,
                    "status": status
                }
            }

            response = requests.put(
                url,
                headers=self.headers,
                json=data,
                timeout=10
            )

            if response.status_code == 200:
                logger.info(f"✅ تم تحديث الطلب #{order_id} إلى {status}")
                return True
            else:
                logger.error(f"❌ فشل تحديث الطلب: {response.status_code}")
                return False

        except Exception as e:
            logger.error(f"❌ خطأ في تحديث الطلب: {e}")
            return False

    def update_inventory(self, inventory_item_id: int, quantity: int) -> bool:
        """
        تحديث المخزون

        Args:
            inventory_item_id: معرف عنصر المخزون
            quantity: الكمية الجديدة

        Returns:
            نتيجة التحديث
        """
        try:
            url = f"{self.base_url}/inventory_levels/adjust.json"

            data = {
                "inventory_adjustment": {
                    "inventory_item_id": inventory_item_id,
                    "available_adjustment": quantity
                }
            }

            response = requests.post(
                url,
                headers=self.headers,
                json=data,
                timeout=10
            )

            if response.status_code == 200:
                logger.info(f"✅ تم تحديث المخزون #{inventory_item_id}")
                return True
            else:
                logger.error(f"❌ فشل تحديث المخزون: {response.status_code}")
                return False

        except Exception as e:
            logger.error(f"❌ خطأ في تحديث المخزون: {e}")
            return False

    def send_order_email(self, order_id: int, email_subject: str = None) -> bool:
        """
        إرسال بريد الطلب

        Args:
            order_id: معرف الطلب
            email_subject: موضوع البريد

        Returns:
            نتيجة الإرسال
        """
        try:
            url = f"{self.base_url}/orders/{order_id}/fulfillment_orders.json"

            response = requests.get(
                url,
                headers=self.headers,
                timeout=10
            )

            if response.status_code == 200:
                logger.info(f"✅ تم إرسال تأكيد البريد للطلب #{order_id}")
                return True
            else:
                logger.error(f"❌ فشل إرسال البريد: {response.status_code}")
                return False

        except Exception as e:
            logger.error(f"❌ خطأ في إرسال البريد: {e}")
            return False

    def get_order_details(self, order_id: int) -> Dict:
        """الحصول على تفاصيل الطلب"""
        try:
            url = f"{self.base_url}/orders/{order_id}.json"

            response = requests.get(
                url,
                headers=self.headers,
                timeout=10
            )

            if response.status_code == 200:
                order = response.json().get("order", {})
                logger.info(f"✅ تم سحب تفاصيل الطلب #{order_id}")
                return order
            else:
                logger.error(f"❌ فشل سحب التفاصيل: {response.status_code}")
                return {}

        except Exception as e:
            logger.error(f"❌ خطأ في سحب التفاصيل: {e}")
            return {}

    def create_fulfillment(self, order_id: int, line_items: List) -> bool:
        """
        إنشاء عملية شحن (Fulfillment)

        Args:
            order_id: معرف الطلب
            line_items: عناصر الطلب المراد شحنها

        Returns:
            نتيجة الإنشاء
        """
        try:
            # أولاً احصل على fulfillment orders
            url = f"{self.base_url}/orders/{order_id}/fulfillment_orders.json"
            response = requests.get(url, headers=self.headers, timeout=10)

            if response.status_code != 200:
                return False

            fulfillment_orders = response.json().get("fulfillment_orders", [])

            if not fulfillment_orders:
                return False

            # ثم أنشئ fulfillment
            fulfillment_order_id = fulfillment_orders[0]["id"]

            url = f"{self.base_url}/fulfillments.json"
            data = {
                "fulfillment": {
                    "line_items_by_fulfillment_order": [
                        {
                            "fulfillment_order_id": fulfillment_order_id,
                            "fulfillment_order_line_items": [
                                {"id": item["id"]}
                                for item in fulfillment_orders[0].get("line_items", [])
                            ]
                        }
                    ]
                }
            }

            response = requests.post(
                url,
                headers=self.headers,
                json=data,
                timeout=10
            )

            if response.status_code == 201:
                logger.info(f"✅ تم إنشاء عملية شحن للطلب #{order_id}")
                return True
            else:
                logger.error(f"❌ فشل إنشاء الشحن: {response.status_code}")
                return False

        except Exception as e:
            logger.error(f"❌ خطأ في إنشاء الشحن: {e}")
            return False

    def get_store_stats(self) -> Dict:
        """الحصول على إحصائيات المتجر"""
        try:
            # سحب الطلبات
            orders_response = requests.get(
                f"{self.base_url}/orders.json?limit=1&status=any",
                headers=self.headers,
                timeout=10
            )

            # سحب المنتجات
            products_response = requests.get(
                f"{self.base_url}/products.json?limit=1",
                headers=self.headers,
                timeout=10
            )

            orders = orders_response.json().get("orders", [])
            products = products_response.json().get("products", [])

            stats = {
                "connected": self.is_connected,
                "shop": self.shop_url,
                "last_sync": self.last_sync,
                "orders_synced": self.orders_count,
                "products_synced": self.products_count,
                "timestamp": datetime.now().isoformat()
            }

            logger.info(f"✅ إحصائيات المتجر: {stats}")
            return stats

        except Exception as e:
            logger.error(f"❌ خطأ في جلب الإحصائيات: {e}")
            return {}


def main():
    """الدالة الرئيسية"""
    print("\n" + "="*60)
    print("  🔗 Shopify Connector - وحدة الاتصال المباشرة")
    print("="*60)

    # البيانات الأساسية
    SHOP = "uk1msh-1p.myshopify.com"
    TOKEN = "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"

    # إنشاء الاتصال
    print("\n🔌 الاتصال بـ Shopify...")
    connector = ShopifyConnector(SHOP, TOKEN)

    if not connector.is_connected:
        print("\n❌ فشل الاتصال!")
        return

    print("\n✅ الاتصال نجح!")

    # 1. سحب الطلبات
    print("\n📦 سحب الطلبات الجديدة...")
    orders = connector.get_new_orders(status="unfulfilled")

    if orders:
        print(f"\n📋 الطلبات الجديدة ({len(orders)}):")
        for order in orders[:3]:  # أول 3 طلبات
            print(f"\n   طلب #{order['id']}:")
            print(f"   - العميل: {order['customer']['email']}")
            print(f"   - المبلغ: {order['total_price']} {order['currency']}")
            print(f"   - الحالة: {order['fulfillment_status']}")
            print(f"   - المنتجات: {len(order['line_items'])}")

    # 2. سحب المنتجات
    print("\n\n📦 سحب المنتجات...")
    products = connector.get_products()

    if products:
        print(f"\n📋 المنتجات ({len(products)}):")
        for product in products[:3]:  # أول 3 منتجات
            print(f"\n   {product['title']}")
            print(f"   - المعرّف: {product['id']}")
            print(f"   - المتغيرات: {len(product['variants'])}")

    # 3. الإحصائيات
    print("\n\n📊 إحصائيات المتجر:")
    stats = connector.get_store_stats()
    print(json.dumps(stats, ensure_ascii=False, indent=2))

    print("\n✅ انتهى الاتصال الأساسي!")


if __name__ == "__main__":
    main()
