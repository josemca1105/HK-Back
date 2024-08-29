from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model

@receiver(post_migrate)
def create_default_user(sender, **kwargs):
    User = get_user_model()
    if not User.objects.filter(email='jasseyda@gmail.com').exists():
        User.objects.create_superuser(
            email='jasseyda@gmail.com',
            password='admin123',
            f_name='Jasseyda',
            l_name='Aljorna',
            role='admin',
        )
        print("Default admin user created.")