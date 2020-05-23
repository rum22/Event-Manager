import datefinder
from django.shortcuts import get_object_or_404
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
from datetime import datetime, timedelta
from .models import Post
from django.views.generic import DetailView


def create_event(start_time_str, summary, duration=2, description=None, location=None):
	credentials=pickle.load(open("token.pkl", "rb"))
	service=build("calendar", "v3", credentials=credentials)
	matches = list(datefinder.find_dates(start_time_str))
	if len(matches):
		start_time = matches[0]
		end_time = start_time+timedelta(hours=duration)
	event = {
		'summary': summary,
		'location': location,
		'description': description,
		'start':{
			'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
			'timeZone': 'Asia/Kolkata',
		},
		'end':{
			'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
			'timeZone': 'Asia/Kolkata',
		},
		'reminders': {
			'useDefault': False,
			'overrides': [
				{'method': 'email', 'minutes': 3*60},
				{'method': 'popup', 'minutes': 30},
			],
		},
	}
	service.events().insert(calendarId='primary',body=event).execute()

class Set_Reminder(DetailView):
	model = Post
	template_name = 'event/after_bookmark.html'
	def get_queryset(self):
		post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
		start_time_string = post.date_of_event.strftime("%Y-%m-%dT%H:%M:%S")
		event_summary = post.title
		event_venue=post.venue
		create_event(start_time_str=start_time_string,summary=event_summary,location=event_venue)
		return super().get_queryset()
	
