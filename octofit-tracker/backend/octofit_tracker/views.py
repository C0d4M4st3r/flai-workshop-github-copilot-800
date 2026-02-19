from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Team, Activity, Leaderboard, Workout
from .serializers import (
    UserSerializer, 
    TeamSerializer, 
    ActivitySerializer, 
    LeaderboardSerializer, 
    WorkoutSerializer
)
#test

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User model
    Provides CRUD operations for users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=False, methods=['get'])
    def by_team(self, request):
        """Get users by team_id"""
        team_id = request.query_params.get('team_id')
        if team_id:
            users = User.objects.filter(team_id=team_id)
            serializer = self.get_serializer(users, many=True)
            return Response(serializer.data)
        return Response(
            {'error': 'team_id parameter is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=False, methods=['get'])
    def by_email(self, request):
        """Get user by email"""
        email = request.query_params.get('email')
        if email:
            try:
                user = User.objects.get(email=email)
                serializer = self.get_serializer(user)
                return Response(serializer.data)
            except User.DoesNotExist:
                return Response(
                    {'error': 'User not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(
            {'error': 'email parameter is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )


class TeamViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Team model
    Provides CRUD operations for teams
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """Get all members of a team"""
        team = self.get_object()
        users = User.objects.filter(team_id=str(team._id))
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get team statistics"""
        team = self.get_object()
        leaderboard_entries = Leaderboard.objects.filter(team_id=str(team._id))
        
        total_activities = sum(entry.total_activities for entry in leaderboard_entries)
        total_calories = sum(entry.total_calories for entry in leaderboard_entries)
        total_distance = sum(entry.total_distance for entry in leaderboard_entries)
        
        return Response({
            'team_id': str(team._id),
            'team_name': team.name,
            'total_activities': total_activities,
            'total_calories': total_calories,
            'total_distance': round(total_distance, 2),
            'member_count': User.objects.filter(team_id=str(team._id)).count()
        })


class ActivityViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Activity model
    Provides CRUD operations for activities
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    
    @action(detail=False, methods=['get'])
    def by_user(self, request):
        """Get activities by user_id"""
        user_id = request.query_params.get('user_id')
        if user_id:
            activities = Activity.objects.filter(user_id=user_id)
            serializer = self.get_serializer(activities, many=True)
            return Response(serializer.data)
        return Response(
            {'error': 'user_id parameter is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get activities by activity_type"""
        activity_type = request.query_params.get('activity_type')
        if activity_type:
            activities = Activity.objects.filter(activity_type=activity_type)
            serializer = self.get_serializer(activities, many=True)
            return Response(serializer.data)
        return Response(
            {'error': 'activity_type parameter is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )


class LeaderboardViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Leaderboard model
    Provides CRUD operations for leaderboard entries
    """
    queryset = Leaderboard.objects.all().order_by('rank')
    serializer_class = LeaderboardSerializer
    
    @action(detail=False, methods=['get'])
    def top(self, request):
        """Get top N entries from leaderboard"""
        limit = int(request.query_params.get('limit', 10))
        top_entries = Leaderboard.objects.all().order_by('rank')[:limit]
        serializer = self.get_serializer(top_entries, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_team(self, request):
        """Get leaderboard entries by team_id"""
        team_id = request.query_params.get('team_id')
        if team_id:
            entries = Leaderboard.objects.filter(team_id=team_id).order_by('rank')
            serializer = self.get_serializer(entries, many=True)
            return Response(serializer.data)
        return Response(
            {'error': 'team_id parameter is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )


class WorkoutViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Workout model
    Provides CRUD operations for workout suggestions
    """
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    
    @action(detail=False, methods=['get'])
    def by_difficulty(self, request):
        """Get workouts by difficulty level"""
        difficulty = request.query_params.get('difficulty')
        if difficulty:
            workouts = Workout.objects.filter(difficulty=difficulty)
            serializer = self.get_serializer(workouts, many=True)
            return Response(serializer.data)
        return Response(
            {'error': 'difficulty parameter is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=False, methods=['get'])
    def by_activity_type(self, request):
        """Get workouts by activity_type"""
        activity_type = request.query_params.get('activity_type')
        if activity_type:
            workouts = Workout.objects.filter(activity_type=activity_type)
            serializer = self.get_serializer(workouts, many=True)
            return Response(serializer.data)
        return Response(
            {'error': 'activity_type parameter is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
