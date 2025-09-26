# -*- coding: utf-8 -*-
"""
Naebak Statistics Service - Flask Application

This is the main application file for the Naebak Statistics Service. It provides a RESTful API
for accessing comprehensive platform analytics, including overall statistics, regional data,
and political party metrics. The service is designed to support dashboards, reporting, and
data-driven decision making across the Naebak platform.

Key Features:
- Platform-wide statistics aggregation
- Regional analytics by governorate
- Political party performance metrics
- Reference data endpoints for frontend applications
- Real-time statistics with Redis backend
"""

from flask import Flask, jsonify, request
from config import Config
from models import StatisticsService
import constants

# Create Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Create statistics service
stats_service = StatisticsService()

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for service monitoring.
    
    This endpoint provides comprehensive health status including Redis connectivity
    and service version information. It's used by load balancers and monitoring
    systems to verify service availability.
    
    Returns:
        JSON response with service health information including:
        - Service status and version
        - Redis connectivity status
    """
    try:
        # Test Redis connection
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
    """
    Retrieve comprehensive platform-wide statistics.
    
    This endpoint provides a complete overview of platform usage including user counts,
    activity metrics, and complaint resolution data. It's the primary endpoint for
    main dashboard displays and executive reporting.
    
    Returns:
        JSON response with comprehensive platform statistics including:
        - Total users across all categories
        - Activity metrics (messages, ratings, complaints)
        - Complaint resolution statistics
        - User engagement indicators
        
    Business Metrics:
        - User growth and distribution
        - Platform engagement levels
        - Service effectiveness through complaint resolution
        - Political participation through candidate/member counts
    """
    try:
        stats = stats_service.get_overall_statistics()
        return jsonify(stats.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/statistics/governorate/<governorate_code>/', methods=['GET'])
def get_governorate_statistics(governorate_code):
    """
    Retrieve statistics for a specific governorate.
    
    This endpoint provides regional analytics for understanding platform usage
    patterns across different governorates in Egypt. It helps identify areas
    with high engagement and regions that may need additional outreach.
    
    Args:
        governorate_code (str): The unique code identifying the governorate.
    
    Returns:
        JSON response with governorate-specific statistics including:
        - User registration counts
        - Complaint submission patterns
        - Communication activity levels
        - Regional engagement metrics
        
    Regional Insights:
        - User density per governorate for resource allocation
        - Complaint patterns for identifying regional issues
        - Communication activity for engagement measurement
    """
    try:
        stats = stats_service.get_governorate_statistics(governorate_code)
        return jsonify({
            "governorate_code": stats.governorate_code,
            "governorate_name": stats.governorate_name,
            "users_count": stats.users_count,
            "complaints_count": stats.complaints_count,
            "messages_count": stats.messages_count,
            "complaints_per_user": round(stats.get_complaints_per_user(), 2),
            "activity_score": round(stats.get_activity_score(), 2)
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/statistics/party/<party_name>/', methods=['GET'])
def get_party_statistics(party_name):
    """
    Retrieve statistics for a specific political party.
    
    This endpoint provides political analytics including party membership,
    candidate participation, and public ratings. It offers insights into
    party popularity and engagement within the platform.
    
    Args:
        party_name (str): The name of the political party.
    
    Returns:
        JSON response with party-specific statistics including:
        - Candidate and member counts
        - Average public ratings
        - Total representation metrics
        - Performance categorization
        
    Political Analytics:
        - Party representation through candidate and member counts
        - Public perception through average ratings
        - Political engagement and participation metrics
    """
    try:
        stats = stats_service.get_party_statistics(party_name)
        return jsonify({
            "party_name": stats.party_name,
            "candidates_count": stats.candidates_count,
            "members_count": stats.members_count,
            "ratings_average": round(stats.ratings_average, 2),
            "total_representation": stats.get_total_representation(),
            "rating_category": stats.get_rating_category()
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/statistics/governorates/all/', methods=['GET'])
def get_all_governorates_statistics():
    """
    Retrieve statistics for all governorates.
    
    This endpoint provides a comprehensive view of regional platform usage
    across all Egyptian governorates, useful for national-level analytics
    and comparative regional analysis.
    
    Returns:
        JSON array with statistics for all governorates, sorted by activity level.
    """
    try:
        all_stats = stats_service.get_all_governorate_statistics()
        # Sort by activity score for better insights
        all_stats.sort(key=lambda x: x.get_activity_score(), reverse=True)
        
        return jsonify([{
            "governorate_code": stats.governorate_code,
            "governorate_name": stats.governorate_name,
            "users_count": stats.users_count,
            "complaints_count": stats.complaints_count,
            "messages_count": stats.messages_count,
            "activity_score": round(stats.get_activity_score(), 2)
        } for stats in all_stats]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/statistics/parties/top/', methods=['GET'])
def get_top_parties_statistics():
    """
    Retrieve statistics for top political parties by representation.
    
    This endpoint provides political analytics for the most active parties
    on the platform, useful for understanding political engagement patterns.
    
    Query Parameters:
        limit (int, optional): Maximum number of parties to return (default: 10).
    
    Returns:
        JSON array with top parties sorted by total representation.
    """
    try:
        limit = request.args.get('limit', 10, type=int)
        top_parties = stats_service.get_top_parties_by_representation(limit)
        
        return jsonify([{
            "party_name": stats.party_name,
            "candidates_count": stats.candidates_count,
            "members_count": stats.members_count,
            "total_representation": stats.get_total_representation(),
            "ratings_average": round(stats.ratings_average, 2),
            "rating_category": stats.get_rating_category()
        } for stats in top_parties]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/statistics/data/governorates/', methods=['GET'])
def get_governorates_data():
    """
    Retrieve reference data for all governorates.
    
    This endpoint provides the complete list of Egyptian governorates with
    their codes and names, used by frontend applications for dropdowns
    and reference purposes.
    
    Returns:
        JSON array with governorate reference data.
    """
    return jsonify(constants.GOVERNORATES), 200

@app.route('/api/statistics/data/parties/', methods=['GET'])
def get_parties_data():
    """
    Retrieve reference data for all political parties.
    
    This endpoint provides the complete list of political parties recognized
    by the platform, used by frontend applications for party selection and
    reference purposes.
    
    Returns:
        JSON array with political party reference data.
    """
    return jsonify(constants.POLITICAL_PARTIES), 200

@app.route('/api/statistics/data/user-types/', methods=['GET'])
def get_user_types_data():
    """
    Retrieve reference data for user types.
    
    This endpoint provides the classification of user types available on
    the platform (citizens, candidates, members, etc.), used for user
    registration and analytics categorization.
    
    Returns:
        JSON array with user type reference data.
    """
    return jsonify(constants.USER_TYPES), 200

@app.route('/api/statistics/data/councils/', methods=['GET'])
def get_councils_data():
    """
    Retrieve reference data for council types.
    
    This endpoint provides information about different types of councils
    and governmental bodies represented on the platform.
    
    Returns:
        JSON array with council type reference data.
    """
    return jsonify(constants.COUNCIL_TYPES), 200

@app.route('/api/statistics/data/complaint-categories/', methods=['GET'])
def get_complaint_categories_data():
    """
    Retrieve reference data for complaint categories.
    
    This endpoint provides the classification system for complaints,
    used by frontend applications for complaint submission and
    analytics categorization.
    
    Returns:
        JSON array with complaint category reference data.
    """
    return jsonify(constants.COMPLAINT_CATEGORIES), 200

@app.route('/api/statistics/summary/', methods=['GET'])
def get_statistics_summary():
    """
    Retrieve a summary of key platform metrics.
    
    This endpoint provides a condensed view of the most important platform
    statistics, optimized for quick dashboard displays and mobile applications.
    
    Returns:
        JSON response with key summary metrics including engagement rates
        and resolution statistics.
    """
    try:
        stats = stats_service.get_overall_statistics()
        
        return jsonify({
            "total_users": stats.total_users,
            "total_complaints": stats.total_complaints,
            "complaint_resolution_rate": round(stats.get_complaint_resolution_rate(), 1),
            "user_engagement_score": round(stats.get_user_engagement_score(), 1),
            "active_candidates": stats.total_candidates,
            "platform_activity": {
                "messages": stats.total_messages,
                "ratings": stats.total_ratings
            }
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/statistics/initialize/', methods=['POST'])
def initialize_default_data():
    """
    Initialize default statistical data for testing and demonstration.
    
    This endpoint sets up realistic sample data when the service is first
    deployed, providing immediate visual feedback for dashboards and
    testing capabilities for development environments.
    
    Returns:
        JSON response confirming successful data initialization.
        
    Security Note:
        This endpoint should be protected or disabled in production environments.
    """
    try:
        stats_service.initialize_default_data()
        return jsonify({"message": "تم تهيئة البيانات الافتراضية بنجاح"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 Not Found errors."""
    return jsonify({"error": "الصفحة غير موجودة"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 Internal Server errors."""
    return jsonify({"error": "خطأ داخلي في الخادم"}), 500

if __name__ == '__main__':
    # Initialize default data on startup for testing
    try:
        stats_service.initialize_default_data()
        print("✅ Default data initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing data: {e}")
    
    # Run the application
    app.run(
        host='0.0.0.0', 
        port=app.config['PORT'], 
        debug=app.config['FLASK_ENV'] == 'development'
    )
