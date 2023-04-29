from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, UserProfile

# @receiver(post_save, sender=User)
# def post_save_create_profile_receiver(sender, instance, created, **kwargs):
#     if created:  # Check if user is created or not
#         UserProfile.objects.create(user=instance) # Create user profile for that user

#     else: # If user is not created but modified 
#         try:
#             profile = UserProfile.objects.get(user=instance)
#             profile.save()
#         except:
#             # Create the userprofile if not exist
#             UserProfile.objects.create(user=instance)

