from django.db import models
from django.conf import settings

class VolunteerProfile(models.Model):
    ROLE_CHOICES = [
        ("volunteer", "Volunteer"),
        ("coordinator", "Coordinator")
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    iin = models.CharField(max_length=12)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default="volunteer")
    profile_image = models.ImageField(upload_to="profile/", null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_hours = models.IntegerChoices()

    def __str__(self):
        return f"{self.user.username} - {self.role}"