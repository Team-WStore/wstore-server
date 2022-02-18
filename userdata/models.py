from django.db import models
from django.contrib.auth.models import User
# Paquetes de DJango necesarios para incorporar las señales
from django.dispatch import receiver
from django.db.models.signals import post_save

# Reset password packages
from django_rest_passwordreset.signals import reset_password_token_created
# Send email Multialternative
from django.shortcuts import render
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default='')
    lastname = models.CharField(max_length=50, default='')
    phone = models.CharField(max_length=15, default='')
    identity = models.CharField(max_length=15, default='')
    address = models.CharField(max_length=50, null=True, blank=True)
    avatar = models.URLField(max_length=500)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['user__username']

@receiver(post_save, sender=User)
def ensure_profile_exists(sender, instance, **kwargs):
    if kwargs.get('created', False):
        Profile.objects.get_or_create(user=instance)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    destination_email = reset_password_token.user.email
    ctx = {
        'email':destination_email,
        'token':reset_password_token.key
    }
    template = get_template('userdata/reset_password_email.html')
    content = template.render(ctx)
    send_email = EmailMultiAlternatives(
        'Reseteo de contraseña para WStore',
        'WStore',
        settings.EMAIL_HOST_USER,
        [destination_email]
    )

    send_email.attach_alternative(content, 'text/html')
    send_email.send()