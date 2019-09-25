from django.urls import path

from django.contrib.auth import views as auth_views
from accountapp import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", views.signup, name="signup"),
    path("add_member_profile/", views.newTeamMember),
    path("team_profile/<int:id>/", views.team_profile),
]
