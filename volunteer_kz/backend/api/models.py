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
    # phone_number = models.CharField(max_length=20, null=True, blank=True)
    profile_image = models.ImageField(upload_to="profiles/", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    bio = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    
    totalHour = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    

class ActiveProjectManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status="open")
    def by_category(self, category_id):
        return self.get_queryset().filter(category_id=category_id)


class ProjectCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    icon = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    

class Project(models.Model):
    STATUS_CHOICES = [
        ("open", "Открыт"),
        ("in_progress", "В процессе"),
        ("completed", "Завершён"),
        ("cancelled", "Отменён"),
    ]

    category = models.ForeignKey(
        ProjectCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name="projects"
    )

    title = models.CharField(max_length=150)
    description = models.TextField()
    address = models.CharField(max_length=200)
    image = models.ImageField(upload_to="projects/", null=True, blank=True)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    hours_count = models.IntegerField()
    volunteers_needed = models.IntegerField()

    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="open")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active = ActiveProjectManager()

    def __str__(self):
        return f"{self.title} | {self.status}"
    

class ProjectApplication(models.Model):
    STATUS_CHOICES = [
        ("pending", "На рассмотрении"),
        ("approved", "Одобрено"),
        ("rejected", "Отклонено"),
        ("completed", "Выполнено"),
        ("cancelled", "Отменено"),
    ]

    volunteer = models.ForeignKey(
        VolunteerProfile,
        on_delete=models.CASCADE,
        related_name="project_applications"
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    cover_letter = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="pending")
    hours_logged = models.IntegerField(default=0)
    reject_reason = models.TextField(null=True, blank=True)

    applied_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("volunteer", "project")

    def __str__(self):
        return f"{self.volunteer.user.username} → {self.project.title} | {self.status}"


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    topic = models.CharField(max_length=50)
    message = models.TextField()

    def __str__(self):
        return f"from {self.name} ({self.email}); topic - {self.topic}; message: {self.message}"
