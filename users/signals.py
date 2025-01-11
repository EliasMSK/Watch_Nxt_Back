# users/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

@receiver(post_save, sender=get_user_model())
def assign_default_role(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='Usuario')
        instance.groups.add(group)
