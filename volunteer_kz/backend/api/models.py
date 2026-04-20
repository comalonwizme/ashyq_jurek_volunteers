from django.db import models
from django.contrib.auth.models import User
class VolunteerProfile(models.Model):
    ROLE_CHOICES = [
        ("volunteer", "Volunteer"),
        ("coordinator", "Coordinator")
    ]

    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name="volunteer_profile"
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="volunteer")
    phone_number = models.CharField(max_length=20)
    profile_image = models.ImageField(upload_to="profiles/", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    bio = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    
    totalHour = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
