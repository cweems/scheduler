import unittest
from datetime import datetime, timedelta
from django.utils import timezone
from main.utils import free_time_finder
from django.contrib.auth.models import User
from main.models import Meeting

class TestFreeTimeFinder(unittest.TestCase):

    def create_meetings(self):
        user1 = User.objects.create(username='1', email='user1@example.com')
        user2 = User.objects.create(username='2', email='user2@example.com')
        user3 = User.objects.create(username='3', email='user3@example.com')

        meeting1 = Meeting.objects.create(
                        user=user1,
                        start_time=timezone.now(),
                        end_time=timezone.now() + timedelta(hours=1))

        meeting2 = Meeting.objects.create(
                        user=user2,
                        start_time=timezone.now() + timedelta(hours=2),
                        end_time=timezone.now() + timedelta(hours=3))

        meeting3 = Meeting.objects.create(
                        user=user3,
                        start_time=timezone.now() + timedelta(hours=3),
                        end_time=timezone.now() + timedelta(hours=4))

        meeting4 = Meeting.objects.create(
                        user=user1,
                        start_time=timezone.now() + timedelta(hours=5),
                        end_time=timezone.now() + timedelta(hours=6))

    def test_find_free_time_before_and_after(self):
        self.create_meetings()

        result = free_time_finder()
        before_string = 'Any time before ' + timezone.now().strftime("%Y-%m-%d %H:%M")
        last_meeting_time = timezone.now() + timedelta(hours=6)
        after_string = 'Any time after ' + last_meeting_time.strftime("%Y-%m-%d %H:%M")

        self.assertIn(before_string, result)
        self.assertIn(after_string, result)

    def test_find_time_between_meetings(self):

        result = free_time_finder()

        between_1_start = timezone.now() + timedelta(hours=1)
        between_1_end = timezone.now() + timedelta(hours=2)
        between_1 = 'Between ' + between_1_start.strftime("%Y-%m-%d %H:%M") + ' and ' + between_1_end.strftime("%Y-%m-%d %H:%M")

        between_2_start = timezone.now() + timedelta(hours=4)
        between_2_end = timezone.now() + timedelta(hours=5)
        between_2 = 'Between ' + between_2_start.strftime("%Y-%m-%d %H:%M") + ' and ' + between_2_end.strftime("%Y-%m-%d %H:%M")

        self.assertIn(between_1, result)
        self.assertIn(between_2, result)
