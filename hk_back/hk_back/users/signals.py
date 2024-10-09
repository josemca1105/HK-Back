from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model

# Create default admins user
@receiver(post_migrate)
def create_default_user(sender, **kwargs):
    User = get_user_model()

    # First admin user
    if not User.objects.filter(email='jasseyda@gmail.com').exists():
        User.objects.create_superuser(
            email='jasseyda@gmail.com',
            password='Admin123*',
            f_name='Jasseyda',
            l_name='Aljorna',
            role='admin',
        )
        print("Default Jasseyda user created.")
    
    # Second admin user
    if not User.objects.filter(email='hilaimar@gmail.com').exists():
        User.objects.create_superuser(
            email='hilaimar@gmail.com',
            password='Admin123*',
            f_name='Hilaimar',
            l_name='Nose',
            role='admin',
        )
        print("Default Hilaimar user created.")
    
    # Third admin user
    if not User.objects.filter(email='jm.calderon1105@gmail.com').exists():
        User.objects.create_superuser(
            email='jm.calderon1105@gmail.com',
            password='Admin123*',
            f_name='Jose',
            l_name='Calderon',
            role='admin',
        )
        print("Default Jose user created.")
