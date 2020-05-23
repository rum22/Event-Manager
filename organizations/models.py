from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from event.models import Post

class Profile_org(models.Model):
	#simply means that each User will have a profile
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='default_org.jpg', upload_to='profile_org_pics')
	is_org = models.BooleanField(default=False)
	roll_number = models.CharField(max_length=100,default='Please fill this.')
	department = models.CharField(max_length=100,default='Please fill this.')
	bookmarks = models.ManyToManyField(Post)

	def __str__(self):
			return f'{self.user.username} Profile'

	#to resize the image to a smaller image. overriding the save function of the model
	def save(self, *args, **kwargs):
		super(Profile_org, self).save(*args, **kwargs)

		img = Image.open(self.image.path)
		if img.height>300 or img.width>300:
			output_size = (300,300)
			img.thumbnail(output_size)
			img.save(self.image.path)