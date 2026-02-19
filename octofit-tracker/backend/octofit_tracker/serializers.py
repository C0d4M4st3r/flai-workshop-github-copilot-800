from rest_framework import serializers
from .models import User, Team, Activity, Leaderboard, Workout


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['_id', 'name', 'email', 'password', 'team_id', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        """Create and return a new user"""
        return User.objects.create(**validated_data)


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for Team model"""
    class Meta:
        model = Team
        fields = ['_id', 'name', 'description', 'created_at']
        read_only_fields = ['_id', 'created_at']


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for Activity model"""
    class Meta:
        model = Activity
        fields = ['_id', 'user_id', 'activity_type', 'duration', 'calories_burned', 
                  'distance', 'date', 'created_at']
        read_only_fields = ['_id', 'created_at']


class LeaderboardSerializer(serializers.ModelSerializer):
    """Serializer for Leaderboard model"""
    class Meta:
        model = Leaderboard
        fields = ['_id', 'user_id', 'team_id', 'total_activities', 'total_duration', 
                  'total_calories', 'total_distance', 'rank', 'updated_at']
        read_only_fields = ['_id', 'updated_at']


class WorkoutSerializer(serializers.ModelSerializer):
    """Serializer for Workout model"""
    class Meta:
        model = Workout
        fields = ['_id', 'name', 'description', 'activity_type', 'difficulty', 
                  'duration', 'calories_estimate', 'created_at']
        read_only_fields = ['_id', 'created_at']
