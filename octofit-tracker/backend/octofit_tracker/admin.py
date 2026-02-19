from django.contrib import admin
from .models import User, Team, Activity, Leaderboard, Workout


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin interface for User model"""
    list_display = ('name', 'email', 'team_id', 'created_at')
    list_filter = ('team_id', 'created_at')
    search_fields = ('name', 'email')
    ordering = ('-created_at',)
    readonly_fields = ('_id', 'created_at')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Admin interface for Team model"""
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('_id', 'created_at')


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """Admin interface for Activity model"""
    list_display = ('user_id', 'activity_type', 'duration', 'calories_burned', 'distance', 'date', 'created_at')
    list_filter = ('activity_type', 'date', 'created_at')
    search_fields = ('user_id', 'activity_type')
    ordering = ('-date', '-created_at')
    readonly_fields = ('_id', 'created_at')


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    """Admin interface for Leaderboard model"""
    list_display = ('user_id', 'team_id', 'rank', 'total_activities', 'total_duration', 'total_calories', 'total_distance', 'updated_at')
    list_filter = ('team_id', 'rank')
    search_fields = ('user_id', 'team_id')
    ordering = ('rank',)
    readonly_fields = ('_id', 'updated_at')


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    """Admin interface for Workout model"""
    list_display = ('name', 'activity_type', 'difficulty', 'duration', 'calories_estimate', 'created_at')
    list_filter = ('activity_type', 'difficulty', 'created_at')
    search_fields = ('name', 'description', 'activity_type')
    ordering = ('-created_at',)
    readonly_fields = ('_id', 'created_at')
