# -*- coding: utf-8 -*-
"""
Statistics Service Data Models - Naebak Project

This module defines the core data models and business logic for the Naebak Statistics Service.
It includes models for platform-wide statistics, governorate-specific analytics, and political
party metrics. The service provides comprehensive insights into platform usage and engagement.
"""

from dataclasses import dataclass
from typing import List, Dict, Any
import redis
from config import Config

# Setup Redis connection
redis_client = redis.from_url(Config.REDIS_URL, decode_responses=True)

@dataclass
class StatisticsData:
    """
    Represents comprehensive platform-wide statistics.
    
    This dataclass aggregates key metrics across all aspects of the Naebak platform,
    providing a high-level overview of platform usage, user engagement, and system
    activity. These statistics are used for dashboards, reporting, and strategic
    decision-making.
    
    Attributes:
        total_users (int): Total number of registered users across all user types.
        total_citizens (int): Number of registered citizens (voters).
        total_candidates (int): Number of registered political candidates.
        total_members (int): Number of registered party/council members.
        total_messages (int): Total number of messages sent through the platform.
        total_complaints (int): Total number of complaints submitted.
        total_ratings (int): Total number of ratings/reviews given.
        resolved_complaints (int): Number of complaints that have been resolved.
        pending_complaints (int): Number of complaints still pending resolution.
    
    Business Metrics:
        - User engagement can be measured by messages and ratings per user
        - Platform effectiveness by complaint resolution rate
        - Political participation by candidate and member registration
    """
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
        """
        Convert statistics data to dictionary format for JSON serialization.
        
        Returns:
            Dict[str, Any]: A dictionary representation of the platform statistics.
        """
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
    
    def get_complaint_resolution_rate(self) -> float:
        """
        Calculate the complaint resolution rate as a percentage.
        
        Returns:
            float: Percentage of complaints that have been resolved (0-100).
        """
        if self.total_complaints == 0:
            return 0.0
        return (self.resolved_complaints / self.total_complaints) * 100
    
    def get_user_engagement_score(self) -> float:
        """
        Calculate a user engagement score based on messages and ratings per user.
        
        Returns:
            float: Average engagement actions per user.
        """
        if self.total_users == 0:
            return 0.0
        return (self.total_messages + self.total_ratings) / self.total_users

@dataclass
class GovernorateStats:
    """
    Represents statistics for a specific governorate.
    
    This dataclass provides regional analytics to understand platform usage
    patterns across different governorates in Egypt. It helps identify areas
    with high engagement and regions that may need additional outreach.
    
    Attributes:
        governorate_code (str): Unique identifier for the governorate.
        governorate_name (str): Human-readable name of the governorate.
        users_count (int): Number of registered users from this governorate.
        complaints_count (int): Number of complaints submitted from this governorate.
        messages_count (int): Number of messages sent by users from this governorate.
    
    Regional Insights:
        - User density per governorate for resource allocation
        - Complaint patterns for identifying regional issues
        - Communication activity for engagement measurement
    """
    governorate_code: str
    governorate_name: str
    users_count: int = 0
    complaints_count: int = 0
    messages_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert governorate statistics to dictionary format for JSON serialization.
        
        Returns:
            Dict[str, Any]: A dictionary representation of the governorate statistics.
        """
        return {
            'governorate_code': self.governorate_code,
            'governorate_name': self.governorate_name,
            'users_count': self.users_count,
            'complaints_count': self.complaints_count,
            'messages_count': self.messages_count
        }
    
    def get_complaints_per_user(self) -> float:
        """
        Calculate the average number of complaints per user in this governorate.
        
        Returns:
            float: Average complaints per user, indicating regional engagement levels.
        """
        if self.users_count == 0:
            return 0.0
        return self.complaints_count / self.users_count
    
    def get_activity_score(self) -> float:
        """
        Calculate an activity score based on messages and complaints per user.
        
        Returns:
            float: Combined activity score for the governorate.
        """
        if self.users_count == 0:
            return 0.0
        return (self.messages_count + self.complaints_count) / self.users_count

@dataclass
class PartyStats:
    """
    Represents statistics for a specific political party.
    
    This dataclass tracks political party metrics including membership,
    candidate participation, and public ratings. It provides insights into
    party popularity and engagement within the platform.
    
    Attributes:
        party_name (str): Name of the political party.
        candidates_count (int): Number of candidates affiliated with this party.
        members_count (int): Number of registered party members.
        ratings_average (float): Average rating received by party candidates/members.
    
    Political Analytics:
        - Party representation through candidate and member counts
        - Public perception through average ratings
        - Political engagement and participation metrics
    """
    party_name: str
    candidates_count: int = 0
    members_count: int = 0
    ratings_average: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert party statistics to dictionary format for JSON serialization.
        
        Returns:
            Dict[str, Any]: A dictionary representation of the party statistics.
        """
        return {
            'party_name': self.party_name,
            'candidates_count': self.candidates_count,
            'members_count': self.members_count,
            'ratings_average': round(self.ratings_average, 2)
        }
    
    def get_total_representation(self) -> int:
        """
        Calculate total party representation (candidates + members).
        
        Returns:
            int: Combined count of candidates and members.
        """
        return self.candidates_count + self.members_count
    
    def get_rating_category(self) -> str:
        """
        Categorize the party based on its average rating.
        
        Returns:
            str: Rating category (excellent, good, average, poor).
        """
        if self.ratings_average >= 4.5:
            return "excellent"
        elif self.ratings_average >= 3.5:
            return "good"
        elif self.ratings_average >= 2.5:
            return "average"
        else:
            return "poor"

class StatisticsService:
    """
    Main service class for statistics aggregation and analytics operations.
    
    This class implements the core business logic for collecting, aggregating,
    and serving statistical data across the Naebak platform. It uses Redis for
    high-performance counter operations and provides comprehensive analytics
    for dashboards and reporting.
    
    Key Features:
        - Real-time statistics aggregation using Redis
        - Platform-wide metrics and regional analytics
        - Political party performance tracking
        - Configurable counter operations for data updates
        - Default data initialization for testing and demos
    
    Attributes:
        redis_client: Redis client for data storage and retrieval.
    
    Performance Considerations:
        - All counters are stored in Redis for fast access
        - Atomic operations ensure data consistency
        - Efficient key naming for organized data structure
    """
    
    def __init__(self):
        """
        Initialize the statistics service with Redis connection.
        """
        self.redis_client = redis_client
    
    def get_overall_statistics(self) -> StatisticsData:
        """
        Retrieve comprehensive platform-wide statistics.
        
        This method aggregates all major platform metrics from Redis counters
        and returns a complete statistics overview for dashboards and reporting.
        
        Returns:
            StatisticsData: Complete platform statistics including user counts,
            activity metrics, and complaint resolution data.
        """
        stats = StatisticsData()
        
        # Retrieve all statistics from Redis
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
        """
        Retrieve statistics for a specific governorate.
        
        This method provides regional analytics for understanding platform usage
        patterns across different governorates in Egypt.
        
        Args:
            governorate_code (str): The unique code identifying the governorate.
            
        Returns:
            GovernorateStats: Statistics specific to the requested governorate.
            
        Raises:
            ValueError: If the governorate code is not found in the system.
        """
        from constants import GOVERNORATES
        
        # Find the governorate in the constants
        governorate = next((g for g in GOVERNORATES if g['code'] == governorate_code), None)
        if not governorate:
            raise ValueError(f"Governorate not found: {governorate_code}")
        
        stats = GovernorateStats(
            governorate_code=governorate_code,
            governorate_name=governorate['name']
        )
        
        # Retrieve governorate-specific statistics from Redis
        stats.users_count = int(self.redis_client.get(f'stats:gov:{governorate_code}:users') or 0)
        stats.complaints_count = int(self.redis_client.get(f'stats:gov:{governorate_code}:complaints') or 0)
        stats.messages_count = int(self.redis_client.get(f'stats:gov:{governorate_code}:messages') or 0)
        
        return stats
    
    def get_party_statistics(self, party_name: str) -> PartyStats:
        """
        Retrieve statistics for a specific political party.
        
        This method provides political analytics including party membership,
        candidate participation, and public ratings.
        
        Args:
            party_name (str): The name of the political party.
            
        Returns:
            PartyStats: Statistics specific to the requested political party.
        """
        stats = PartyStats(party_name=party_name)
        
        # Retrieve party-specific statistics from Redis
        stats.candidates_count = int(self.redis_client.get(f'stats:party:{party_name}:candidates') or 0)
        stats.members_count = int(self.redis_client.get(f'stats:party:{party_name}:members') or 0)
        
        # Calculate average ratings
        ratings_sum = float(self.redis_client.get(f'stats:party:{party_name}:ratings_sum') or 0)
        ratings_count = int(self.redis_client.get(f'stats:party:{party_name}:ratings_count') or 0)
        stats.ratings_average = ratings_sum / ratings_count if ratings_count > 0 else 0.0
        
        return stats
    
    def increment_counter(self, key: str, amount: int = 1):
        """
        Increment a specific counter in Redis.
        
        This method provides a convenient way to update statistics counters
        when events occur throughout the platform.
        
        Args:
            key (str): The Redis key for the counter to increment.
            amount (int): The amount to increment by (default: 1).
        """
        self.redis_client.incr(key, amount)
    
    def set_counter(self, key: str, value: int):
        """
        Set a specific counter value in Redis.
        
        This method allows direct setting of counter values, useful for
        initialization or bulk updates.
        
        Args:
            key (str): The Redis key for the counter to set.
            value (int): The value to set for the counter.
        """
        self.redis_client.set(key, value)
    
    def get_all_governorate_statistics(self) -> List[GovernorateStats]:
        """
        Retrieve statistics for all governorates.
        
        This method provides a comprehensive view of regional platform usage
        across all Egyptian governorates.
        
        Returns:
            List[GovernorateStats]: Statistics for all governorates.
        """
        from constants import GOVERNORATES
        
        all_stats = []
        for governorate in GOVERNORATES:
            try:
                stats = self.get_governorate_statistics(governorate['code'])
                all_stats.append(stats)
            except ValueError:
                # Skip governorates with no data
                continue
        
        return all_stats
    
    def get_top_parties_by_representation(self, limit: int = 10) -> List[PartyStats]:
        """
        Get the top political parties by total representation.
        
        Args:
            limit (int): Maximum number of parties to return.
            
        Returns:
            List[PartyStats]: Top parties sorted by total representation.
        """
        from constants import POLITICAL_PARTIES
        
        party_stats = []
        for party in POLITICAL_PARTIES:
            try:
                stats = self.get_party_statistics(party['name'])
                party_stats.append(stats)
            except Exception:
                # Skip parties with no data
                continue
        
        # Sort by total representation and return top parties
        party_stats.sort(key=lambda x: x.get_total_representation(), reverse=True)
        return party_stats[:limit]
    
    def initialize_default_data(self):
        """
        Initialize default statistical data for testing and demonstration.
        
        This method sets up realistic sample data when the service is first
        deployed, providing immediate visual feedback for dashboards and
        testing capabilities for development.
        
        Default Values:
            - 1,500 total users with realistic distribution
            - 5,000 messages indicating active communication
            - 800 complaints with 75% resolution rate
            - 2,500 ratings showing user engagement
        """
        # Set default values for testing
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
    
    def reset_all_statistics(self):
        """
        Reset all statistics counters to zero.
        
        This method is useful for testing or when starting fresh data collection.
        Use with caution as this operation cannot be undone.
        """
        keys_to_reset = [
            'stats:total_users', 'stats:total_citizens', 'stats:total_candidates',
            'stats:total_members', 'stats:total_messages', 'stats:total_complaints',
            'stats:total_ratings', 'stats:resolved_complaints', 'stats:pending_complaints'
        ]
        
        for key in keys_to_reset:
            self.redis_client.set(key, 0)
