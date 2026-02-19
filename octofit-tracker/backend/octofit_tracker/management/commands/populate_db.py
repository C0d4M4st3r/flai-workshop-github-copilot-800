from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting database population...'))
        
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Existing data cleared'))
        
        # Create Teams
        self.stdout.write('Creating teams...')
        team_marvel = Team.objects.create(
            name='Team Marvel',
            description='Avengers assemble! The mightiest heroes of the Marvel Universe'
        )
        team_dc = Team.objects.create(
            name='Team DC',
            description='Justice League united! DC\'s finest superheroes'
        )
        self.stdout.write(self.style.SUCCESS(f'Created teams: {team_marvel.name}, {team_dc.name}'))
        
        # Create Marvel Users
        self.stdout.write('Creating Marvel heroes...')
        marvel_users = [
            User.objects.create(
                name='Tony Stark',
                email='ironman@marvel.com',
                password='arc_reactor_3000',
                team_id=str(team_marvel._id)
            ),
            User.objects.create(
                name='Steve Rogers',
                email='captainamerica@marvel.com',
                password='shield_forever',
                team_id=str(team_marvel._id)
            ),
            User.objects.create(
                name='Thor Odinson',
                email='thor@marvel.com',
                password='mjolnir_worthy',
                team_id=str(team_marvel._id)
            ),
            User.objects.create(
                name='Bruce Banner',
                email='hulk@marvel.com',
                password='gamma_smash',
                team_id=str(team_marvel._id)
            ),
            User.objects.create(
                name='Natasha Romanoff',
                email='blackwidow@marvel.com',
                password='red_room_grad',
                team_id=str(team_marvel._id)
            ),
            User.objects.create(
                name='Peter Parker',
                email='spiderman@marvel.com',
                password='with_great_power',
                team_id=str(team_marvel._id)
            ),
        ]
        
        # Create DC Users
        self.stdout.write('Creating DC heroes...')
        dc_users = [
            User.objects.create(
                name='Clark Kent',
                email='superman@dc.com',
                password='krypton_pride',
                team_id=str(team_dc._id)
            ),
            User.objects.create(
                name='Bruce Wayne',
                email='batman@dc.com',
                password='im_batman',
                team_id=str(team_dc._id)
            ),
            User.objects.create(
                name='Diana Prince',
                email='wonderwoman@dc.com',
                password='themyscira_warrior',
                team_id=str(team_dc._id)
            ),
            User.objects.create(
                name='Barry Allen',
                email='flash@dc.com',
                password='fastest_alive',
                team_id=str(team_dc._id)
            ),
            User.objects.create(
                name='Arthur Curry',
                email='aquaman@dc.com',
                password='atlantis_king',
                team_id=str(team_dc._id)
            ),
            User.objects.create(
                name='Hal Jordan',
                email='greenlantern@dc.com',
                password='willpower_ring',
                team_id=str(team_dc._id)
            ),
        ]
        
        all_users = marvel_users + dc_users
        self.stdout.write(self.style.SUCCESS(f'Created {len(all_users)} superhero users'))
        
        # Create Activities
        self.stdout.write('Creating activities...')
        activity_types = ['Running', 'Cycling', 'Swimming', 'Weightlifting', 'Yoga', 'Boxing']
        activities = []
        
        for user in all_users:
            # Create 10-15 activities per user
            num_activities = random.randint(10, 15)
            for i in range(num_activities):
                activity_type = random.choice(activity_types)
                duration = random.randint(20, 120)  # 20 to 120 minutes
                calories = duration * random.randint(5, 10)  # 5-10 calories per minute
                distance = round(duration * random.uniform(0.05, 0.15), 2) if activity_type in ['Running', 'Cycling', 'Swimming'] else None
                activity_date = date.today() - timedelta(days=random.randint(0, 30))
                
                activities.append(Activity.objects.create(
                    user_id=str(user._id),
                    activity_type=activity_type,
                    duration=duration,
                    calories_burned=calories,
                    distance=distance,
                    date=activity_date
                ))
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(activities)} activities'))
        
        # Create Leaderboard entries
        self.stdout.write('Creating leaderboard entries...')
        leaderboard_entries = []
        
        for user in all_users:
            user_activities = Activity.objects.filter(user_id=str(user._id))
            total_activities = user_activities.count()
            total_duration = sum(a.duration for a in user_activities)
            total_calories = sum(a.calories_burned for a in user_activities)
            total_distance = sum(a.distance for a in user_activities if a.distance)
            
            leaderboard_entries.append(Leaderboard.objects.create(
                user_id=str(user._id),
                team_id=user.team_id,
                total_activities=total_activities,
                total_duration=total_duration,
                total_calories=total_calories,
                total_distance=round(total_distance, 2)
            ))
        
        # Calculate and assign ranks based on total calories
        leaderboard_entries.sort(key=lambda x: x.total_calories, reverse=True)
        for rank, entry in enumerate(leaderboard_entries, start=1):
            entry.rank = rank
            entry.save()
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(leaderboard_entries)} leaderboard entries'))
        
        # Create Workout suggestions
        self.stdout.write('Creating workout suggestions...')
        workouts = [
            Workout.objects.create(
                name='Super Soldier Sprint',
                description='High-intensity interval training inspired by Captain America',
                activity_type='Running',
                difficulty='Hard',
                duration=45,
                calories_estimate=500
            ),
            Workout.objects.create(
                name='Asgardian Strength Training',
                description='Build godlike strength with Thor\'s hammer workout',
                activity_type='Weightlifting',
                difficulty='Hard',
                duration=60,
                calories_estimate=600
            ),
            Workout.objects.create(
                name='Stark Tech Cardio',
                description='Efficient cardio workout designed by Tony Stark',
                activity_type='Cycling',
                difficulty='Medium',
                duration=40,
                calories_estimate=450
            ),
            Workout.objects.create(
                name='Widow\'s Flexibility Flow',
                description='Enhance flexibility and balance like Black Widow',
                activity_type='Yoga',
                difficulty='Medium',
                duration=50,
                calories_estimate=250
            ),
            Workout.objects.create(
                name='Web-Slinger Agility',
                description='Spider-Man inspired agility and endurance training',
                activity_type='Boxing',
                difficulty='Medium',
                duration=45,
                calories_estimate=500
            ),
            Workout.objects.create(
                name='Kryptonian Power Cycle',
                description='Superman\'s morning cardio routine',
                activity_type='Cycling',
                difficulty='Hard',
                duration=60,
                calories_estimate=700
            ),
            Workout.objects.create(
                name='Dark Knight Combat Training',
                description='Batman\'s martial arts and combat conditioning',
                activity_type='Boxing',
                difficulty='Hard',
                duration=90,
                calories_estimate=800
            ),
            Workout.objects.create(
                name='Amazonian Warrior Workout',
                description='Wonder Woman\'s complete body conditioning',
                activity_type='Weightlifting',
                difficulty='Hard',
                duration=75,
                calories_estimate=650
            ),
            Workout.objects.create(
                name='Speed Force Intervals',
                description='The Flash\'s lightning-fast interval training',
                activity_type='Running',
                difficulty='Hard',
                duration=30,
                calories_estimate=550
            ),
            Workout.objects.create(
                name='Atlantean Aqua Workout',
                description='Aquaman\'s underwater-inspired swimming routine',
                activity_type='Swimming',
                difficulty='Medium',
                duration=50,
                calories_estimate=500
            ),
            Workout.objects.create(
                name='Green Lantern Willpower Session',
                description='Mental and physical endurance training',
                activity_type='Yoga',
                difficulty='Easy',
                duration=40,
                calories_estimate=200
            ),
            Workout.objects.create(
                name='Beginner Hero Training',
                description='Perfect for starting your superhero fitness journey',
                activity_type='Running',
                difficulty='Easy',
                duration=30,
                calories_estimate=300
            ),
        ]
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(workouts)} workout suggestions'))
        
        # Summary
        self.stdout.write(self.style.SUCCESS('\n=== Database Population Complete ==='))
        self.stdout.write(self.style.SUCCESS(f'Teams: {Team.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Users: {User.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Activities: {Activity.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Leaderboard Entries: {Leaderboard.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Workouts: {Workout.objects.count()}'))
        self.stdout.write(self.style.SUCCESS('\n✨ OctoFit Tracker is ready for superhero action! ✨'))
