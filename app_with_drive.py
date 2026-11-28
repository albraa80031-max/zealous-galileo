#!/usr/bin/env python3
"""
Enhanced Legal Agent Web Application with Google Drive Integration
تطبيق ويب متقدم لـ Legal Agent مع مزامنة Google Drive
"""

import json
import logging
import os
from datetime import datetime

from flask import Flask, jsonify, render_template, request

from legal_agent import LegalAgent
from legal_agent.drive_sync import DriveIntegrationManager, GoogleDriveSync

# تكوين الـ logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

# تحميل Legal Agent
agent = LegalAgent()
agent.import_from_json("data/sample_legal_data.json")

# تهيئة Google Drive Sync
drive_sync = GoogleDriveSync(folder_name="Legal Agent - نظام الشؤون القانونية")
drive_manager = DriveIntegrationManager(agent, drive_sync)

# محاولة تهيئة Google Drive
try:
    drive_manager.initialize_drive()
    logger.info("✅ Google Drive integration initialized")
except Exception as e:
    logger.warning(f"⚠️  Google Drive integration not fully available: {e}")


# ============ الصفحات الرئيسية ============


@app.route("/")
def index():
    """الصفحة الرئيسية"""
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    """لوحة التحكم"""
    return render_template("dashboard.html")


@app.route("/sync")
def sync_page():
    """صفحة المزامنة"""
    return render_template("sync.html")


# ============ APIs للبيانات ============


@app.route("/api/summary")
def api_summary():
    """API للملخص"""
    summary = agent.get_summary()
    summary["sync_status"] = drive_manager.get_status()
    return jsonify(summary)


@app.route("/api/search", methods=["POST"])
def api_search():
    """API للبحث"""
    data = request.get_json()
    search_type = data.get("type")
    query = data.get("query", "").lower()

    results = []

    if search_type == "cases":
        cases = agent.get_all_cases()
        for case in cases:
            if (
                query in case.get("title", "").lower()
                or query in case.get("description", "").lower()
            ):
                results.append(case)

    elif search_type == "contracts":
        for contract in agent.contracts:
            if (
                query in contract.get("title", "").lower()
                or query in contract.get("type", "").lower()
            ):
                results.append(contract)

    elif search_type == "documents":
        for doc in agent.documents:
            if (
                query in doc.get("title", "").lower()
                or query in doc.get("type", "").lower()
                or query in " ".join(doc.get("tags", [])).lower()
            ):
                results.append(doc)

    return jsonify({"results": results, "count": len(results)})


@app.route("/api/case/<case_id>")
def api_case(case_id):
    """API لتفاصيل القضية"""
    case = agent.get_case(case_id)
    if not case:
        return jsonify({"error": "Case not found"}), 404

    related_docs = []
    for doc_id in case.get("documents", []):
        for doc in agent.documents:
            if doc["id"] == doc_id:
                related_docs.append(doc)

    case["related_documents"] = related_docs
    return jsonify(case)


@app.route("/api/cases")
def api_cases():
    """API لجميع القضايا"""
    cases = agent.get_all_cases()
    return jsonify({"cases": cases, "count": len(cases)})


@app.route("/api/contracts")
def api_contracts():
    """API لجميع العقود"""
    return jsonify({"contracts": agent.contracts, "count": len(agent.contracts)})


@app.route("/api/documents")
def api_documents():
    """API لجميع الوثائق"""
    return jsonify({"documents": agent.documents, "count": len(agent.documents)})


# ============ APIs للمزامنة مع Google Drive ============


@app.route("/api/sync/status")
def api_sync_status():
    """الحصول على حالة المزامنة"""
    status = drive_manager.get_status()
    return jsonify(status)


@app.route("/api/sync/now", methods=["POST"])
def api_sync_now():
    """تنفيذ مزامنة فورية"""
    logger.info("📤 Starting immediate sync to Google Drive")

    try:
        success = drive_manager.auto_sync()
        return jsonify(
            {
                "success": success,
                "message": "✅ تمت المزامنة بنجاح" if success else "❌ فشلت المزامنة",
                "timestamp": datetime.now().isoformat(),
                "status": drive_manager.get_status(),
            }
        )
    except Exception as e:
        logger.error(f"Sync error: {e}")
        return (
            jsonify(
                {
                    "success": False,
                    "message": f"❌ خطأ: {str(e)}",
                    "timestamp": datetime.now().isoformat(),
                }
            ),
            500,
        )


@app.route("/api/sync/backup", methods=["POST"])
def api_sync_backup():
    """إنشاء نسخة احتياطية"""
    logger.info("💾 Creating backup on Google Drive")

    try:
        backup = drive_sync.create_backup(agent)
        if backup:
            return jsonify(
                {
                    "success": True,
                    "message": "✅ تم إنشاء النسخة الاحتياطية بنجاح",
                    "backup_size": len(json.dumps(backup)),
                    "timestamp": datetime.now().isoformat(),
                }
            )
        else:
            return jsonify({"success": False, "message": "❌ فشل إنشاء النسخة الاحتياطية"}), 500
    except Exception as e:
        logger.error(f"Backup error: {e}")
        return jsonify({"success": False, "message": f"❌ خطأ: {str(e)}"}), 500


@app.route("/api/sync/log")
def api_sync_log():
    """الحصول على سجل المزامنة"""
    log_entries = drive_sync.sync_log[-20:]  # آخر 20 عملية
    return jsonify(
        {
            "total_operations": len(drive_sync.sync_log),
            "recent_operations": log_entries,
            "status": drive_manager.get_status(),
        }
    )


@app.route("/api/sync/schedule", methods=["POST"])
def api_sync_schedule():
    """جدولة مزامنة دورية"""
    data = request.get_json()
    interval = data.get("interval", 3600)

    drive_manager.sync_interval = interval
    logger.info(f"⏱️  Sync scheduled every {interval} seconds")

    return jsonify(
        {
            "success": True,
            "message": f"✅ تم جدولة المزامنة كل {interval} ثانية",
            "interval": interval,
            "next_sync": datetime.now().isoformat(),
        }
    )


# ============ APIs للقضايا (CRUD) ============


@app.route("/api/case/add", methods=["POST"])
def api_add_case():
    """إضافة قضية جديدة"""
    data = request.get_json()
    case_id = data.get("id")
    title = data.get("title")
    description = data.get("description", "")

    try:
        agent.add_case(
            case_id=case_id,
            title=title,
            description=description,
            status=data.get("status", "active"),
            priority=data.get("priority", "medium"),
            parties=data.get("parties", []),
        )

        # مزامنة تلقائية
        drive_manager.auto_sync()

        return jsonify(
            {"success": True, "message": "✅ تمت إضافة القضية بنجاح", "case_id": case_id}
        )
    except Exception as e:
        logger.error(f"Error adding case: {e}")
        return jsonify({"success": False, "message": f"❌ خطأ: {str(e)}"}), 500


@app.route("/api/case/<case_id>/update", methods=["POST"])
def api_update_case(case_id):
    """تحديث قضية"""
    data = request.get_json()

    try:
        success = agent.update_case(case_id, **data)

        if success:
            # مزامنة تلقائية
            drive_manager.auto_sync()

            return jsonify({"success": True, "message": "✅ تم تحديث القضية بنجاح"})
        else:
            return jsonify({"success": False, "message": "❌ فشل تحديث القضية"}), 404
    except Exception as e:
        logger.error(f"Error updating case: {e}")
        return jsonify({"success": False, "message": f"❌ خطأ: {str(e)}"}), 500


# ============ APIs للإحصائيات ============


@app.route("/api/stats/detailed")
def api_stats_detailed():
    """إحصائيات مفصلة"""
    cases = agent.get_all_cases()
    contracts = agent.contracts
    documents = agent.documents

    stats = {
        "cases": {
            "total": len(cases),
            "active": len([c for c in cases if c.get("status") == "active"]),
            "pending": len([c for c in cases if c.get("status") == "pending"]),
            "closed": len([c for c in cases if c.get("status") == "closed"]),
            "by_priority": {
                "high": len([c for c in cases if c.get("priority") == "high"]),
                "medium": len([c for c in cases if c.get("priority") == "medium"]),
                "low": len([c for c in cases if c.get("priority") == "low"]),
            },
        },
        "contracts": {
            "total": len(contracts),
            "active": len([c for c in contracts if c.get("status") == "active"]),
            "draft": len([c for c in contracts if c.get("status") == "draft"]),
            "expired": len([c for c in contracts if c.get("status") == "expired"]),
        },
        "documents": {
            "total": len(documents),
            "filed": len([d for d in documents if d.get("status") == "filed"]),
            "draft": len([d for d in documents if d.get("status") == "draft"]),
            "archived": len([d for d in documents if d.get("status") == "archived"]),
        },
        "sync": drive_manager.get_status(),
    }

    return jsonify(stats)


# ============ Page Not Found ============


@app.errorhandler(404)
def not_found(error):
    """معالج الصفحة غير الموجودة"""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """معالج خطأ الخادم"""
    logger.error(f"Internal error: {error}")
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    logger.info("🚀 Starting Legal Agent Web Application with Google Drive Sync")

    # قراءة المنفذ من متغير البيئة (للبيئة السحابية) أو استخدام 5000 كقيمة افتراضية
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_ENV", "development") == "development"

    logger.info(f"📱 Open http://localhost:{port} in your browser")
    logger.info("☁️  Google Drive integration is active")
    logger.info(f"🔧 Running in {'development' if debug_mode else 'production'} mode")

    # في الإنتاج، debug يجب أن يكون False
    app.run(debug=debug_mode, host="0.0.0.0", port=port)
