# -*- coding: utf-8 -*-
"""إعدادات خدمة الإحصائيات"""

import os
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

class Config:
    """إعدادات التطبيق الأساسية"""
    
    # إعدادات Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    # إعدادات Redis
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    
    # إعدادات الخدمة
    PORT = int(os.environ.get('PORT', 8012))
    STATS_RETENTION_DAYS = int(os.environ.get('STATS_RETENTION_DAYS', 90))
    REAL_TIME_ENABLED = os.environ.get('REAL_TIME_ENABLED', 'true').lower() == 'true'
    AGGREGATION_INTERVAL = int(os.environ.get('AGGREGATION_INTERVAL', 300))
