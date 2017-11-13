from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect

from datetime import datetime
from django.utils.timezone import get_current_timezone

from main.models import Meeting
from main.forms import NewMeetingForm
from main.utils import free_time_finder

def index(request):
    new_meeting_form = NewMeetingForm(request.POST or None)
    free_meeting_times = free_time_finder()

    if request.method == 'POST':
        if new_meeting_form.is_valid():
            tz = get_current_timezone()
            start_time = tz.localize(datetime.strptime(new_meeting_form['start_time'].data, "%Y-%m-%d %H:%M:%S"))
            end_time = tz.localize(datetime.strptime(new_meeting_form['end_time'].data, "%Y-%m-%d %H:%M:%S"))

            meeting = Meeting(
                user = User.objects.get(pk=new_meeting_form['user'].data),
                start_time = start_time,
                end_time = end_time
            )

            meeting.save()
            return redirect('/')

    meetings = Meeting.objects.order_by('start_time')
    return render(request, 'index.html', {'meetings': meetings, 'new_meeting_form': new_meeting_form, 'free_meeting_times': free_meeting_times})
