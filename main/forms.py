from django import forms
from main.models import Meeting
from django.contrib.auth.models import User

from django.contrib.admin import widgets
from datetimewidget.widgets import DateTimeWidget


class NewMeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = [
            'user',
            'start_time',
            'end_time'
        ]

    def __init__(self, *args, **kwargs):
        super(NewMeetingForm, self).__init__(*args, **kwargs)
        self.fields['user'] = forms.ModelChoiceField(
                                                queryset=User.objects.all(),
                                                to_field_name="id")
        self.fields['start_time'].widget = DateTimeWidget(
                                                usel10n=True,
                                                bootstrap_version=3)
        self.fields['end_time'].widget = DateTimeWidget(
                                                usel10n=True,
                                                bootstrap_version=3)
