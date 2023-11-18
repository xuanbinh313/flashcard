from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Deck, Progress


@receiver(post_save, sender=Deck)
def create_progress(sender, instance, created, **kwargs):
    if created:
        Progress.objects.create(
            deck=instance,
        )
