from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, Team, Activity, Leaderboard, Workout
from datetime import date


class UserModelTestCase(TestCase):
    """Test cases for User model"""
    
    def setUp(self):
        """Set up test data"""
        self.team = Team.objects.create(
            name='Test Team',
            description='A test team'
        )
        self.user = User.objects.create(
            name='Test User',
            email='test@example.com',
            password='testpass123',
            team_id=str(self.team._id)
        )
    
    def test_user_creation(self):
        """Test user can be created"""
        self.assertEqual(self.user.name, 'Test User')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.team_id, str(self.team._id))
    
    def test_user_string_representation(self):
        """Test user string representation"""
        self.assertEqual(str(self.user), 'Test User')


class TeamModelTestCase(TestCase):
    """Test cases for Team model"""
    
    def setUp(self):
        """Set up test data"""
        self.team = Team.objects.create(
            name='Test Team',
            description='A test team description'
        )
    
    def test_team_creation(self):
        """Test team can be created"""
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(self.team.description, 'A test team description')
    
    def test_team_string_representation(self):
        """Test team string representation"""
        self.assertEqual(str(self.team), 'Test Team')


class ActivityModelTestCase(TestCase):
    """Test cases for Activity model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create(
            name='Test User',
            email='activity@example.com',
            password='testpass123'
        )
        self.activity = Activity.objects.create(
            user_id=str(self.user._id),
            activity_type='Running',
            duration=30,
            calories_burned=300,
            distance=3.5,
            date=date.today()
        )
    
    def test_activity_creation(self):
        """Test activity can be created"""
        self.assertEqual(self.activity.activity_type, 'Running')
        self.assertEqual(self.activity.duration, 30)
        self.assertEqual(self.activity.calories_burned, 300)
    
    def test_activity_string_representation(self):
        """Test activity string representation"""
        self.assertEqual(str(self.activity), 'Running - 30 mins')


class LeaderboardModelTestCase(TestCase):
    """Test cases for Leaderboard model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create(
            name='Test User',
            email='leaderboard@example.com',
            password='testpass123'
        )
        self.team = Team.objects.create(
            name='Test Team',
            description='Test team'
        )
        self.leaderboard = Leaderboard.objects.create(
            user_id=str(self.user._id),
            team_id=str(self.team._id),
            total_activities=10,
            total_duration=500,
            total_calories=5000,
            total_distance=50.5,
            rank=1
        )
    
    def test_leaderboard_creation(self):
        """Test leaderboard entry can be created"""
        self.assertEqual(self.leaderboard.total_activities, 10)
        self.assertEqual(self.leaderboard.rank, 1)
    
    def test_leaderboard_string_representation(self):
        """Test leaderboard string representation"""
        self.assertIn('Rank 1', str(self.leaderboard))


class WorkoutModelTestCase(TestCase):
    """Test cases for Workout model"""
    
    def setUp(self):
        """Set up test data"""
        self.workout = Workout.objects.create(
            name='Test Workout',
            description='A test workout description',
            activity_type='Running',
            difficulty='Medium',
            duration=45,
            calories_estimate=450
        )
    
    def test_workout_creation(self):
        """Test workout can be created"""
        self.assertEqual(self.workout.name, 'Test Workout')
        self.assertEqual(self.workout.difficulty, 'Medium')
    
    def test_workout_string_representation(self):
        """Test workout string representation"""
        self.assertEqual(str(self.workout), 'Test Workout')


class UserAPITestCase(APITestCase):
    """API test cases for User endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.team = Team.objects.create(
            name='API Test Team',
            description='Team for API testing'
        )
        self.user = User.objects.create(
            name='API User',
            email='api@example.com',
            password='apipass123',
            team_id=str(self.team._id)
        )
    
    def test_get_users_list(self):
        """Test retrieving users list"""
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_user(self):
        """Test creating a new user"""
        data = {
            'name': 'New User',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'team_id': str(self.team._id)
        }
        response = self.client.post('/api/users/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TeamAPITestCase(APITestCase):
    """API test cases for Team endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.team = Team.objects.create(
            name='API Team',
            description='Team for API testing'
        )
    
    def test_get_teams_list(self):
        """Test retrieving teams list"""
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_team(self):
        """Test creating a new team"""
        data = {
            'name': 'New Team',
            'description': 'A brand new team'
        }
        response = self.client.post('/api/teams/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ActivityAPITestCase(APITestCase):
    """API test cases for Activity endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create(
            name='Activity API User',
            email='activityapi@example.com',
            password='testpass123'
        )
    
    def test_get_activities_list(self):
        """Test retrieving activities list"""
        response = self.client.get('/api/activities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_activity(self):
        """Test creating a new activity"""
        data = {
            'user_id': str(self.user._id),
            'activity_type': 'Cycling',
            'duration': 60,
            'calories_burned': 600,
            'distance': 15.5,
            'date': date.today().isoformat()
        }
        response = self.client.post('/api/activities/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LeaderboardAPITestCase(APITestCase):
    """API test cases for Leaderboard endpoints"""
    
    def test_get_leaderboard_list(self):
        """Test retrieving leaderboard list"""
        response = self.client.get('/api/leaderboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WorkoutAPITestCase(APITestCase):
    """API test cases for Workout endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.workout = Workout.objects.create(
            name='Test API Workout',
            description='Workout for API testing',
            activity_type='Yoga',
            difficulty='Easy',
            duration=30,
            calories_estimate=200
        )
    
    def test_get_workouts_list(self):
        """Test retrieving workouts list"""
        response = self.client.get('/api/workouts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_workout(self):
        """Test creating a new workout"""
        data = {
            'name': 'New API Workout',
            'description': 'A new workout for testing',
            'activity_type': 'Swimming',
            'difficulty': 'Hard',
            'duration': 45,
            'calories_estimate': 500
        }
        response = self.client.post('/api/workouts/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
