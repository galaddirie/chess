from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.auth.models import User
from django.dispatch import receiver  
# from .models import Player

# @receiver(post_save, sender=User)
# def create_player(sender, instance, created, **kwarg):
#     if created:
#         Player.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwarg):
#     instance.profile.save()