from django.db import models
from djongo import models as djongo_models


class User(models.Model):
    """User model for OctoFit Tracker"""
    _id = djongo_models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True, db_index=True)
    password = models.CharField(max_length=200)
    team_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['email'], name='user_email_idx'),
        ]
    
    def __str__(self):
        return self.name


class Team(models.Model):
    """Team model for OctoFit Tracker"""
    _id = djongo_models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'teams'
    
    def __str__(self):
        return self.name


class Activity(models.Model):
    """Activity model for OctoFit Tracker"""
    _id = djongo_models.ObjectIdField(primary_key=True)
    user_id = models.CharField(max_length=100)
    activity_type = models.CharField(max_length=100)
    duration = models.IntegerField(help_text="Duration in minutes")
    calories_burned = models.IntegerField()
    distance = models.FloatField(null=True, blank=True, help_text="Distance in miles")
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'activities'
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.activity_type} - {self.duration} mins"


class Leaderboard(models.Model):
    """Leaderboard model for OctoFit Tracker"""
    _id = djongo_models.ObjectIdField(primary_key=True)
    user_id = models.CharField(max_length=100)
    team_id = models.CharField(max_length=100)
    total_activities = models.IntegerField(default=0)
    total_duration = models.IntegerField(default=0, help_text="Total duration in minutes")
    total_calories = models.IntegerField(default=0)
    total_distance = models.FloatField(default=0.0, help_text="Total distance in miles")
    rank = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'leaderboard'
        ordering = ['rank']
    
    def __str__(self):
        return f"Rank {self.rank} - User {self.user_id}"


class Workout(models.Model):
    """Workout suggestion model for OctoFit Tracker"""
    _id = djongo_models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    activity_type = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=50)
    duration = models.IntegerField(help_text="Suggested duration in minutes")
    calories_estimate = models.IntegerField(help_text="Estimated calories burned")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'workouts'
    
    def __str__(self):
        return self.name
