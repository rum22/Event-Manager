from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile_org

#doing this becuase we want a profile to be created for each user created
@receiver(post_save, sender=User)
def create_profile_org(sender, instance, created, **kwargs):
	if created:
		Profile_org.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile_org(sender, instance, **kwargs):
	instance.profile_org.save()