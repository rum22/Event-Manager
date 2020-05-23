from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from django.urls import reverse

class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	organization= models.ForeignKey(User, on_delete=models.CASCADE, related_name='name_of_organizer')
	date_of_event = models.DateTimeField(blank=False, null=False)#datetime.datetime(yyyy,mm,dd,look on net for timeformat)
	venue = models.CharField(max_length=100)
	MY_TAGS=(('educational','educational'),('fun','fun'),('sports','sports'),('party','party'),('other','other'))
	tags=MultiSelectField(choices=MY_TAGS, max_length=100)
	#tags={'educational' : 0,'fun' : 0,'sports' : 0,'party' : 0,'other' : 0}

	#returns the title when queries
	def __str__(self):
		return self.title

	#tells django the url to a particular post 
	def get_absolute_url(self):
		return reverse('post-detail' ,kwargs={'pk': self.pk})