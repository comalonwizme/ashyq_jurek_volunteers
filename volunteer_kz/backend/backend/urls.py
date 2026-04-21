from django.contrib import admin
from django.urls import path
from api import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", views.register_view),
    path("login/", views.login_view),
    path("logout/", views.logout_view),
    path("projects/", views.ProjectListCreateView.as_view()),
    path("projects/<int:pk>/", views.ProjectDetailView.as_view()),
    path("projects/<int:pk>/apply/", views.apply_to_project),
    path("ratings/", views.ratings_view),
    path("contact/", views.ContactAPIView.as_view()),
    path("contact/<int:pk>/", views.ContactAPIView.as_view()),
]
