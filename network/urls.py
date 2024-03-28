
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_post", views.create_post, name="create_post"),
    path("user/<int:user_id>", views.user_profile, name="user_profile"),
    path("user/<int:user_id>/follow", views.follow, name="follow"),
    path("user/<int:user_id>/unfollow", views.unfollow, name="unfollow"),
    path("following", views.following, name="following"),
]
