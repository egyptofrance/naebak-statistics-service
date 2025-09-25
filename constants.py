# -*- coding: utf-8 -*-
"""ثوابت وبيانات أساسية لخدمة الإحصائيات"""

# مفاتيح Redis للإحصائيات الأساسية
REDIS_KEYS = {
    'TOTAL_USERS': 'stats:total_users',
    'TOTAL_CITIZENS': 'stats:total_citizens', 
    'TOTAL_CANDIDATES': 'stats:total_candidates',
    'TOTAL_MEMBERS': 'stats:total_members',
    'TOTAL_MESSAGES': 'stats:total_messages',
    'TOTAL_COMPLAINTS': 'stats:total_complaints',
    'TOTAL_RATINGS': 'stats:total_ratings',
    'RESOLVED_COMPLAINTS': 'stats:resolved_complaints',
    'PENDING_COMPLAINTS': 'stats:pending_complaints',
}

# المحافظات المصرية (27 محافظة)
GOVERNORATES = [
    {"name": "القاهرة", "name_en": "Cairo", "code": "CAI"},
    {"name": "الجيزة", "name_en": "Giza", "code": "GIZ"},
    {"name": "الإسكندرية", "name_en": "Alexandria", "code": "ALX"},
    {"name": "الدقهلية", "name_en": "Dakahlia", "code": "DAK"},
    {"name": "البحر الأحمر", "name_en": "Red Sea", "code": "RSS"},
    {"name": "البحيرة", "name_en": "Beheira", "code": "BEH"},
    {"name": "الفيوم", "name_en": "Fayoum", "code": "FAY"},
    {"name": "الغربية", "name_en": "Gharbia", "code": "GHR"},
    {"name": "الإسماعيلية", "name_en": "Ismailia", "code": "ISM"},
    {"name": "المنوفية", "name_en": "Monufia", "code": "MNF"},
    {"name": "المنيا", "name_en": "Minya", "code": "MNY"},
    {"name": "القليوبية", "name_en": "Qalyubia", "code": "QLY"},
    {"name": "الوادي الجديد", "name_en": "New Valley", "code": "WAD"},
    {"name": "شمال سيناء", "name_en": "North Sinai", "code": "NSI"},
    {"name": "جنوب سيناء", "name_en": "South Sinai", "code": "SSI"},
    {"name": "الشرقية", "name_en": "Sharqia", "code": "SHR"},
    {"name": "سوهاج", "name_en": "Sohag", "code": "SOH"},
    {"name": "السويس", "name_en": "Suez", "code": "SUZ"},
    {"name": "أسوان", "name_en": "Aswan", "code": "ASW"},
    {"name": "أسيوط", "name_en": "Asyut", "code": "ASY"},
    {"name": "بني سويف", "name_en": "Beni Suef", "code": "BNS"},
    {"name": "بورسعيد", "name_en": "Port Said", "code": "PTS"},
    {"name": "دمياط", "name_en": "Damietta", "code": "DAM"},
    {"name": "كفر الشيخ", "name_en": "Kafr El Sheikh", "code": "KFS"},
    {"name": "مطروح", "name_en": "Matrouh", "code": "MAT"},
    {"name": "الأقصر", "name_en": "Luxor", "code": "LUX"},
    {"name": "قنا", "name_en": "Qena", "code": "QEN"}
]

# الأحزاب السياسية المصرية
POLITICAL_PARTIES = [
    {"name": "حزب الوفد", "name_en": "Al-Wafd Party", "abbreviation": "الوفد"},
    {"name": "الحزب الوطني الديمقراطي", "name_en": "National Democratic Party", "abbreviation": "الوطني"},
    {"name": "حزب الغد", "name_en": "Al-Ghad Party", "abbreviation": "الغد"},
    {"name": "حزب التجمع الوطني التقدمي الوحدوي", "name_en": "National Progressive Unionist Party", "abbreviation": "التجمع"},
    {"name": "حزب الناصري", "name_en": "Nasserist Party", "abbreviation": "الناصري"},
    {"name": "حزب الكرامة", "name_en": "Al-Karama Party", "abbreviation": "الكرامة"},
    {"name": "حزب الوسط الجديد", "name_en": "New Wasat Party", "abbreviation": "الوسط"},
    {"name": "حزب الحرية المصري", "name_en": "Egyptian Freedom Party", "abbreviation": "الحرية"},
    {"name": "حزب المصريين الأحرار", "name_en": "Free Egyptians Party", "abbreviation": "المصريين الأحرار"},
    {"name": "حزب النور", "name_en": "Al-Nour Party", "abbreviation": "النور"},
    {"name": "حزب البناء والتنمية", "name_en": "Building and Development Party", "abbreviation": "البناء والتنمية"},
    {"name": "حزب الإصلاح والتنمية", "name_en": "Reform and Development Party", "abbreviation": "الإصلاح والتنمية"},
    {"name": "حزب مستقبل وطن", "name_en": "Future of a Nation Party", "abbreviation": "مستقبل وطن"},
    {"name": "حزب المؤتمر", "name_en": "Conference Party", "abbreviation": "المؤتمر"},
    {"name": "حزب الشعب الجمهوري", "name_en": "Republican People's Party", "abbreviation": "الشعب الجمهوري"},
    {"name": "مستقل", "name_en": "Independent", "abbreviation": "مستقل"}
]

# أنواع المستخدمين
USER_TYPES = [
    {
        "type": "citizen", 
        "name": "مواطن", 
        "name_en": "Citizen",
        "description": "مواطن له صوت انتخابي",
        "required_fields": ["phone_number", "governorate"]
    },
    {
        "type": "candidate", 
        "name": "مرشح", 
        "name_en": "Candidate",
        "description": "مرشح لعضوية مجلس الشيوخ أو النواب",
        "required_fields": ["phone_number", "governorate", "council_type", "party"]
    },
    {
        "type": "current_member", 
        "name": "عضو حالي", 
        "name_en": "Current Member",
        "description": "عضو فعلي في مجلس الشيوخ أو النواب",
        "required_fields": ["phone_number", "governorate", "council_type", "party"]
    },
    {
        "type": "admin", 
        "name": "إدارة", 
        "name_en": "Admin",
        "description": "إدارة النظام",
        "required_fields": ["phone_number"]
    }
]

# أنواع المجالس
COUNCIL_TYPES = [
    {
        "type": "parliament", 
        "name": "مجلس النواب", 
        "name_en": "Parliament",
        "description": "المجلس الأساسي للتشريع",
        "term_duration": 5,
        "total_seats": 596
    },
    {
        "type": "senate", 
        "name": "مجلس الشيوخ", 
        "name_en": "Senate",
        "description": "المجلس الاستشاري العلوي", 
        "term_duration": 5,
        "total_seats": 300
    }
]

# حالات الشكاوى
COMPLAINT_STATUSES = [
    {"status": "pending", "name": "في الانتظار", "name_en": "Pending", "color": "#FFC107"},
    {"status": "under_review", "name": "قيد المراجعة", "name_en": "Under Review", "color": "#17A2B8"},
    {"status": "assigned", "name": "تم التعيين", "name_en": "Assigned", "color": "#007BFF"},
    {"status": "resolved", "name": "تم الحل", "name_en": "Resolved", "color": "#28A745"},
    {"status": "rejected", "name": "مرفوضة", "name_en": "Rejected", "color": "#DC3545"}
]

# فئات الشكاوى
COMPLAINT_CATEGORIES = [
    {"name": "البنية التحتية", "name_en": "Infrastructure", "icon": "🏗️"},
    {"name": "الصحة", "name_en": "Health", "icon": "🏥"},
    {"name": "التعليم", "name_en": "Education", "icon": "🎓"},
    {"name": "الأمن", "name_en": "Security", "icon": "🛡️"},
    {"name": "الخدمات العامة", "name_en": "Public Services", "icon": "🏛️"},
    {"name": "النقل والمواصلات", "name_en": "Transportation", "icon": "🚌"},
    {"name": "البيئة", "name_en": "Environment", "icon": "🌱"},
    {"name": "الإسكان", "name_en": "Housing", "icon": "🏠"},
    {"name": "العمل والتوظيف", "name_en": "Employment", "icon": "💼"},
    {"name": "الشؤون الاجتماعية", "name_en": "Social Affairs", "icon": "👥"},
    {"name": "أخرى", "name_en": "Other", "icon": "📝"}
]

# أنواع الإشعارات
NOTIFICATION_TYPES = [
    {"type": "message", "name": "رسالة جديدة", "name_en": "New Message", "icon": "💬"},
    {"type": "complaint", "name": "شكوى", "name_en": "Complaint", "icon": "📋"},
    {"type": "rating", "name": "تقييم", "name_en": "Rating", "icon": "⭐"},
    {"type": "system", "name": "إشعار النظام", "name_en": "System Notification", "icon": "🔔"},
    {"type": "achievement", "name": "إنجاز", "name_en": "Achievement", "icon": "🏆"},
    {"type": "event", "name": "فعالية", "name_en": "Event", "icon": "📅"}
]
