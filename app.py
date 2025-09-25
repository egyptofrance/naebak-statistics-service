# -*- coding: utf-8 -*-
"""التطبيق الرئيسي لخدمة الإحصائيات"""

from flask import Flask, jsonify, request
from config import Config
from models import StatisticsService
import constants

# إنشاء تطبيق Flask
app = Flask(__name__)
app.config.from_object(Config)

# إنشاء خدمة الإحصائيات
stats_service = StatisticsService()

@app.route('/health', methods=['GET'])
def health_check():
    """فحص صحة الخدمة"""
    try:
        # اختبار الاتصال بـ Redis
        stats_service.redis_client.ping()
        redis_status = "connected"
    except Exception as e:
        redis_status = f"disconnected: {str(e)}"
    
    return jsonify({
        "status": "ok",
        "service": "naebak-statistics-service",
        "version": "1.0.0",
        "redis_status": redis_status
    }), 200

@app.route('/api/statistics/overall/', methods=['GET'])
def get_overall_statistics():
    """الحصول على الإحصائيات الإجمالية"""
    try:
        stats = stats_service.get_overall_statistics()
        return jsonify(stats.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/statistics/governorate/<governorate_code>/', methods=['GET'])
def get_governorate_statistics(governorate_code):
    """الحصول على إحصائيات محافظة معينة"""
    try:
        stats = stats_service.get_governorate_statistics(governorate_code)
        return jsonify({
            "governorate_code": stats.governorate_code,
            "governorate_name": stats.governorate_name,
            "users_count": stats.users_count,
            "complaints_count": stats.complaints_count,
            "messages_count": stats.messages_count
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/statistics/party/<party_name>/', methods=['GET'])
def get_party_statistics(party_name):
    """الحصول على إحصائيات حزب معين"""
    try:
        stats = stats_service.get_party_statistics(party_name)
        return jsonify({
            "party_name": stats.party_name,
            "candidates_count": stats.candidates_count,
            "members_count": stats.members_count,
            "ratings_average": round(stats.ratings_average, 2)
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/statistics/data/governorates/', methods=['GET'])
def get_governorates_data():
    """الحصول على قائمة المحافظات"""
    return jsonify(constants.GOVERNORATES), 200

@app.route('/api/statistics/data/parties/', methods=['GET'])
def get_parties_data():
    """الحصول على قائمة الأحزاب"""
    return jsonify(constants.POLITICAL_PARTIES), 200

@app.route('/api/statistics/data/user-types/', methods=['GET'])
def get_user_types_data():
    """الحصول على أنواع المستخدمين"""
    return jsonify(constants.USER_TYPES), 200

@app.route('/api/statistics/data/councils/', methods=['GET'])
def get_councils_data():
    """الحصول على أنواع المجالس"""
    return jsonify(constants.COUNCIL_TYPES), 200

@app.route('/api/statistics/data/complaint-categories/', methods=['GET'])
def get_complaint_categories_data():
    """الحصول على فئات الشكاوى"""
    return jsonify(constants.COMPLAINT_CATEGORIES), 200

@app.route('/api/statistics/initialize/', methods=['POST'])
def initialize_default_data():
    """تهيئة البيانات الافتراضية (للاختبار فقط)"""
    try:
        stats_service.initialize_default_data()
        return jsonify({"message": "تم تهيئة البيانات الافتراضية بنجاح"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    """معالج الخطأ 404"""
    return jsonify({"error": "الصفحة غير موجودة"}), 404

@app.errorhandler(500)
def internal_error(error):
    """معالج الخطأ 500"""
    return jsonify({"error": "خطأ داخلي في الخادم"}), 500

if __name__ == '__main__':
    # تهيئة البيانات الافتراضية عند بدء التشغيل
    try:
        stats_service.initialize_default_data()
        print("✅ تم تهيئة البيانات الافتراضية")
    except Exception as e:
        print(f"❌ خطأ في تهيئة البيانات: {e}")
    
    # تشغيل التطبيق
    app.run(
        host='0.0.0.0', 
        port=app.config['PORT'], 
        debug=app.config['FLASK_ENV'] == 'development'
    )
