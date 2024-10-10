from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model

import os, environ

# Load environment variables
env = environ.Env()
environ.Env.read_env(env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

# Create default admins user
@receiver(post_migrate)
def create_default_user(sender, **kwargs):
    User = get_user_model()

    # First admin user
    if not User.objects.filter(email=env('ADMIN1_EMAIL')).exists():
        User.objects.create_superuser(
            email=env('ADMIN1_EMAIL'),
            password=env('ADMIN1_PASSWORD'),
            f_name=env('ADMIN1_FIRST_NAME'),
            l_name=env('ADMIN1_LAST_NAME'),
            role='admin',
        )
        print(f"Default {env('ADMIN1_FIRST_NAME')} user created.")
    
    # Second admin user
    if not User.objects.filter(email=env('ADMIN2_EMAIL')).exists():
        User.objects.create_superuser(
            email=env('ADMIN2_EMAIL'),
            password=env('ADMIN2_PASSWORD'),
            f_name=env('ADMIN2_FIRST_NAME'),
            l_name=env('ADMIN2_LAST_NAME'),
            role='admin',
        )
        print(f"Default {env('ADMIN2_FIRST_NAME')} user created.")
    
    # Third admin user
    if not User.objects.filter(email=env('ADMIN3_EMAIL')).exists():
        User.objects.create_superuser(
            email=env('ADMIN3_EMAIL'),
            password=env('ADMIN3_PASSWORD'),
            f_name=env('ADMIN3_FIRST_NAME'),
            l_name=env('ADMIN3_LAST_NAME'),
            role='admin',
        )
        print(f"Default {env('ADMIN3_FIRST_NAME')} user created.")
