from main.models import Meeting
from datetime import timedelta


def free_time_finder():
    all_meetings = []
    results = []

    for meeting in Meeting.objects.all():
        all_meetings.append(('start', meeting.start_time))
        all_meetings.append(('end', meeting.end_time))

    sorted_meetings = sorted(all_meetings, key=lambda meeting: meeting[1])

    results.append(
                    'Any time before ' + sorted_meetings[0][1]
                    .strftime("%Y-%m-%d %H:%M"))

    concurrent_meetings = 0
    for idx, current_meeting in enumerate(sorted_meetings):
        if current_meeting[0] == 'start':
            concurrent_meetings += 1
        elif current_meeting[0] == 'end':
            concurrent_meetings -= 1

        if idx < len(sorted_meetings) - 1:
            next_meeting = sorted_meetings[idx + 1]
            next_meeting_start = next_meeting[1].strftime("%Y-%m-%d %H:%M")
            current_meeting_end = current_meeting[1].strftime("%Y-%m-%d %H:%M")
            if(current_meeting[0] == 'end' and
                next_meeting[0] == 'start' and
                concurrent_meetings == 0 and
                next_meeting_start > current_meeting_end):
                    results.append(
                        "Between " + current_meeting[1]
                        .strftime("%Y-%m-%d %H:%M") +
                        " and " + next_meeting[1].strftime("%Y-%m-%d %H:%M"))

    results.append(
                    'Any time after ' + sorted_meetings[-1][1]
                    .strftime("%Y-%m-%d %H:%M"))

    return results
