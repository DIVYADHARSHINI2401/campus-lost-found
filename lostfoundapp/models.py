from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Item(models.Model):
    ITEM_TYPES = [
        ('lost', 'Lost'),
        ('found', 'Found'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    description = models.TextField()
    location = models.CharField(max_length=100)
    date = models.DateField()
    image = models.ImageField(upload_to='items/', blank=True, null=True)
    item_type = models.CharField(max_length=10, choices=ITEM_TYPES)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=15, blank=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item_type.title()} - {self.name}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150, blank=True)
    college_name = models.CharField(max_length=150, blank=True)
    department = models.CharField(max_length=100, blank=True)
    year_of_study = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
