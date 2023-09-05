import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender='movies.Filmwork')
def attention(sender, instance, created, **kwargs):
    if created and instance.creation_date == datetime.date.today():
        print(f"Сегодня премьера {instance.title}! \U0001F973")
