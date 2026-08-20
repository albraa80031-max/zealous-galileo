#!/usr/bin/env python3
"""
Legal Agent Web Interface
واجهة ويب تفاعلية لنظام وكيل الشؤون القانونية
"""

from flask import Flask, render_template, request, jsonify
import json
from pathlib import Path
from legal_agent import LegalAgent

app = Flask(__name__)

# تحميل Legal Agent
agent = LegalAgent()
agent.import_from_json("data/sample_legal_data.json")


@app.route('/')
def index():
    """الصفحة الرئيسية"""
    return render_template('index.html')


@app.route('/api/summary')
def api_summary():
    """API للحصول على الملخص"""
    summary = agent.get_summary()
    return jsonify(summary)


@app.route('/api/search', methods=['POST'])
def api_search():
    """API للبحث"""
    data = request.get_json()
    search_type = data.get('type')
    query = data.get('query', '').lower()

    results = []

    if search_type == 'cases':
        cases = agent.get_all_cases()
        for case in cases:
            if (query in case.get('title', '').lower() or
                query in case.get('description', '').lower()):
                results.append(case)

    elif search_type == 'contracts':
        for contract in agent.contracts:
            if (query in contract.get('title', '').lower() or
                query in contract.get('type', '').lower()):
                results.append(contract)

    elif search_type == 'documents':
        for doc in agent.documents:
            if (query in doc.get('title', '').lower() or
                query in doc.get('type', '').lower() or
                query in ' '.join(doc.get('tags', [])).lower()):
                results.append(doc)

    return jsonify({'results': results, 'count': len(results)})


@app.route('/api/case/<case_id>')
def api_case(case_id):
    """API للحصول على تفاصيل قضية"""
    case = agent.get_case(case_id)
    if not case:
        return jsonify({'error': 'Case not found'}), 404

    # الحصول على الوثائق المرتبطة
    related_docs = []
    for doc_id in case.get('documents', []):
        for doc in agent.documents:
            if doc['id'] == doc_id:
                related_docs.append(doc)

    case['related_documents'] = related_docs
    return jsonify(case)


@app.route('/api/cases')
def api_cases():
    """API للحصول على جميع القضايا"""
    cases = agent.get_all_cases()
    return jsonify({'cases': cases, 'count': len(cases)})


@app.route('/api/contracts')
def api_contracts():
    """API للحصول على جميع العقود"""
    return jsonify({'contracts': agent.contracts, 'count': len(agent.contracts)})


@app.route('/api/documents')
def api_documents():
    """API للحصول على جميع الوثائق"""
    return jsonify({'documents': agent.documents, 'count': len(agent.documents)})


@app.route('/api/export/<case_id>')
def api_export(case_id):
    """API لتصدير بيانات قضية"""
    case = agent.get_case(case_id)
    if not case:
        return jsonify({'error': 'Case not found'}), 404

    return jsonify(case)


if __name__ == '__main__':
    print("🚀 Starting Legal Agent Web Interface...")
    print("📱 Open http://localhost:5000 in your browser")
    app.run(debug=True, port=5000)
