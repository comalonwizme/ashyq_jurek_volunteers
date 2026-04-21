from django.contrib import admin
from .models import VolunteerProfile, Contact, ProjectApplication, ProjectCategory, ActiveProjectManager, Project
# Register your models here.

admin.site.register(VolunteerProfile)
admin.site.register(Project)
admin.site.register(Contact)
