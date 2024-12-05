

from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_resized import ResizedImageField


class Member(models.Model):
    CATEGORY = (
        ('BCT', 'BCT'),
        ('BME', 'BME'),
        ('BCE', 'BCE'),
        ('BAG', 'BAG'),
        ('BARCH', 'BARCH'),

    )
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    batch = models.IntegerField(default=2078)
    faculty = models.CharField(
        max_length=200, choices=CATEGORY, default='BME')
    profile_pic = ResizedImageField(size=[1080, 1080], quality=95, crop=['middle', 'center'],
                                    upload_to="customer_images/", default='default.webp')

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_member(sender, instance, created, **kwargs):
    if created and instance.is_active:
        Member.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_member(sender, instance, **kwargs):
    instance.member.save()


class Posts(models.Model):
    member = models.ForeignKey(Member , on_delete=models.CASCADE  )
    description = models.TextField(max_length=200)
    post_picture = models.ImageField(
        upload_to="post_images/", null=True, blank=True , default='')
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.description
    
class Chat(models.Model):
    member = models.ForeignKey(Member , on_delete=models.CASCADE  )
    message = models.TextField(max_length=200)
    post_picture = models.ImageField(
        upload_to="chat_images/", null=True, blank=True , default='')
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.message
    