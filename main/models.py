from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Meeting(models.Model):

    user = models.ForeignKey(User, blank=False, null=False)

    start_time = models.DateTimeField(blank=False, null=False)
    end_time = models.DateTimeField(blank=False, null=False)

    def validate_start_before_end(self):
        if self.start_time > self.end_time:
            raise ValidationError('Meeting cannot end before it starts.')

    def validate_no_existing_meeting_overlap(self):
        user_meetings = Meeting.objects.filter(user=self.user)
        all_meetings = [('start', self.start_time), ('end', self.end_time)]
        for meeting in user_meetings:
            all_meetings.append(('start', meeting.start_time))
            all_meetings.append(('end', meeting.end_time))

        sorted_meetings = sorted(all_meetings, key=lambda meeting: meeting[1])

        concurrent_meetings = 0
        for meeting in sorted_meetings:
            if meeting[0] == 'start':
                concurrent_meetings += 1
            elif meeting[0] == 'end':
                concurrent_meetings -= 1

            if concurrent_meetings > 1:
                raise ValidationError('New meeting cannot overlap with exisiting meeting.')

    def clean(self, *args, **kwargs):
        if self.start_time and self.end_time:
            self.validate_start_before_end()
            self.validate_no_existing_meeting_overlap()
        super(Meeting, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Meeting, self).save(*args, **kwargs)
