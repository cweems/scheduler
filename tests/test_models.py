from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth.models import User
from main.models import Meeting


class MeetingCreateTest(TestCase):

    # Meeting creation helper
    def create_meeting(self, user=None, start_time=timezone.now(), end_time=timezone.now() + timedelta(hours = 1)):
        meeting_user = user or User.objects.create(email='test@example.com')
        meeting = Meeting.objects.create(
                        user=meeting_user,
                        start_time=start_time,
                        end_time=end_time)

        return meeting

    # Meeting cannot be created with an end time before its start
    def create_meeting_with_end_before_start(self):
        user = User.objects.create(email='test@example.com')
        meeting = Meeting.objects.create(
                        user=user,
                        start_time=timezone.now(),
                        end_time=timezone.now() - timedelta(hours=1))

        return meeting

    # Two users can schedule two meetings at the same time
    # (Make sure that validating existing overlapping meetings only applies to
    # current user.)
    def two_users_create_two_meetings(self):
        user1 = User.objects.create(username='1', email='user1@example.com')
        user2 = User.objects.create(username='2', email='user2@example.com')

        meeting1 = Meeting.objects.create(
                        user=user1,
                        start_time=timezone.now(),
                        end_time=timezone.now() + timedelta(hours=3))

        meeting2 = Meeting.objects.create(
                        user=user2,
                        start_time=timezone.now(),
                        end_time=timezone.now() + timedelta(hours=3))

    def overlapping_meeting_case_1(self, user):
        meeting2 = self.create_meeting(
                        user=user,
                        start_time=timezone.now() - timedelta(hours=1),
                        end_time=timezone.now() + timedelta(hours=4))

    def overlapping_meeting_case_2(self, user):
        meeting2 = self.create_meeting(
                        user=user,
                        start_time=timezone.now() - timedelta(hours=1),
                        end_time=timezone.now() + timedelta(hours=1))

    def overlapping_meeting_case_3(self, user):
        meeting2 = self.create_meeting(
                        user=user,
                        start_time=timezone.now() + timedelta(hours=1),
                        end_time=timezone.now() + timedelta(hours=2))

    def overlapping_meeting_case_4(self, user):
        meeting2 = self.create_meeting(
                        user=user,
                        start_time=timezone.now() + timedelta(hours=2),
                        end_time=timezone.now() + timedelta(hours=4))

    def test_meeting_creation(self):
        m = self.create_meeting()
        self.assertTrue(isinstance(m, Meeting))

    def test_valid_meeting_times(self):
        with self.assertRaises(ValidationError):
            self.create_meeting_with_end_before_start()

    def test_users_create_meetings_at_same_time(self):
        self.two_users_create_two_meetings()

        meeting1 = Meeting.objects.all()[0]
        meeting2 = Meeting.objects.all()[1]

        self.assertTrue(isinstance(meeting1, Meeting))
        self.assertTrue(isinstance(meeting2, Meeting))

    def test_overlapping_meeting(self):
        user = User.objects.create(username='1', email='user1@example.com')
        meeting1 = self.create_meeting(user=user, end_time=timezone.now() + timedelta(hours=3))

        with self.assertRaises(ValidationError):
            self.overlapping_meeting_case_1(user)

        with self.assertRaises(ValidationError):
            self.overlapping_meeting_case_2(user)

        with self.assertRaises(ValidationError):
            self.overlapping_meeting_case_3(user)

        with self.assertRaises(ValidationError):
            self.overlapping_meeting_case_4(user)
