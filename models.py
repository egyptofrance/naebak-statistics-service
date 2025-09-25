# -*- coding: utf-8 -*-
"""نماذج البيانات الأساسية لخدمة الإحصائيات"""

from dataclasses import dataclass
from typing import List, Dict, Any
import redis
from config import Config

# إعداد اتصال Redis
redis_client = redis.from_url(Config.REDIS_URL, decode_responses=True)

@dataclass
class StatisticsData:
    """نموذج بيانات الإحصائيات الأساسية"""
    total_users: int = 0
    total_citizens: int = 0
    total_candidates: int = 0
    total_members: int = 0
    total_messages: int = 0
    total_complaints: int = 0
    total_ratings: int = 0
    resolved_complaints: int = 0
    pending_complaints: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل البيانات إلى قاموس"""
        return {
            'total_users': self.total_users,
            'total_citizens': self.total_citizens,
            'total_candidates': self.total_candidates,
            'total_members': self.total_members,
            'total_messages': self.total_messages,
            'total_complaints': self.total_complaints,
            'total_ratings': self.total_ratings,
            'resolved_complaints': self.resolved_complaints,
            'pending_complaints': self.pending_complaints
        }

@dataclass
class GovernorateStats:
    """إحصائيات المحافظات"""
    governorate_code: str
    governorate_name: str
    users_count: int = 0
    complaints_count: int = 0
    messages_count: int = 0

@dataclass
class PartyStats:
    """إحصائيات الأحزاب"""
    party_name: str
    candidates_count: int = 0
    members_count: int = 0
    ratings_average: float = 0.0

class StatisticsService:
    """خدمة الحصول على الإحصائيات"""
    
    def __init__(self):
        self.redis_client = redis_client
    
    def get_overall_statistics(self) -> StatisticsData:
        """الحصول على الإحصائيات الإجمالية"""
        stats = StatisticsData()
        
        # الحصول على البيانات من Redis
        stats.total_users = int(self.redis_client.get('stats:total_users') or 0)
        stats.total_citizens = int(self.redis_client.get('stats:total_citizens') or 0)
        stats.total_candidates = int(self.redis_client.get('stats:total_candidates') or 0)
        stats.total_members = int(self.redis_client.get('stats:total_members') or 0)
        stats.total_messages = int(self.redis_client.get('stats:total_messages') or 0)
        stats.total_complaints = int(self.redis_client.get('stats:total_complaints') or 0)
        stats.total_ratings = int(self.redis_client.get('stats:total_ratings') or 0)
        stats.resolved_complaints = int(self.redis_client.get('stats:resolved_complaints') or 0)
        stats.pending_complaints = int(self.redis_client.get('stats:pending_complaints') or 0)
        
        return stats
    
    def get_governorate_statistics(self, governorate_code: str) -> GovernorateStats:
        """الحصول على إحصائيات محافظة معينة"""
        from constants import GOVERNORATES
        
        # البحث عن المحافظة
        governorate = next((g for g in GOVERNORATES if g['code'] == governorate_code), None)
        if not governorate:
            raise ValueError(f"محافظة غير موجودة: {governorate_code}")
        
        stats = GovernorateStats(
            governorate_code=governorate_code,
            governorate_name=governorate['name']
        )
        
        # الحصول على الإحصائيات من Redis
        stats.users_count = int(self.redis_client.get(f'stats:gov:{governorate_code}:users') or 0)
        stats.complaints_count = int(self.redis_client.get(f'stats:gov:{governorate_code}:complaints') or 0)
        stats.messages_count = int(self.redis_client.get(f'stats:gov:{governorate_code}:messages') or 0)
        
        return stats
    
    def get_party_statistics(self, party_name: str) -> PartyStats:
        """الحصول على إحصائيات حزب معين"""
        stats = PartyStats(party_name=party_name)
        
        # الحصول على الإحصائيات من Redis
        stats.candidates_count = int(self.redis_client.get(f'stats:party:{party_name}:candidates') or 0)
        stats.members_count = int(self.redis_client.get(f'stats:party:{party_name}:members') or 0)
        
        # حساب متوسط التقييمات
        ratings_sum = float(self.redis_client.get(f'stats:party:{party_name}:ratings_sum') or 0)
        ratings_count = int(self.redis_client.get(f'stats:party:{party_name}:ratings_count') or 0)
        stats.ratings_average = ratings_sum / ratings_count if ratings_count > 0 else 0.0
        
        return stats
    
    def increment_counter(self, key: str, amount: int = 1):
        """زيادة عداد معين"""
        self.redis_client.incr(key, amount)
    
    def set_counter(self, key: str, value: int):
        """تعيين قيمة عداد معين"""
        self.redis_client.set(key, value)
    
    def initialize_default_data(self):
        """تهيئة البيانات الافتراضية للاختبار"""
        # تعيين قيم افتراضية للاختبار
        default_values = {
            'stats:total_users': 1500,
            'stats:total_citizens': 1200,
            'stats:total_candidates': 200,
            'stats:total_members': 100,
            'stats:total_messages': 5000,
            'stats:total_complaints': 800,
            'stats:total_ratings': 2500,
            'stats:resolved_complaints': 600,
            'stats:pending_complaints': 200
        }
        
        for key, value in default_values.items():
            if not self.redis_client.exists(key):
                self.redis_client.set(key, value)
