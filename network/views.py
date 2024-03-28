from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import User, Post, Like, Follow

import datetime

def index(request):
    posts = Post.objects.all().order_by("-timestamp")
    return render(request, "network/index.html", {
        "posts": posts,
    })

@login_required
def following(request):
    return render(request, "network/following.html", {

    })

def user_profile (request, user_id):
    try: 
        user_profile = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))
    
    profile_followers = user_profile.followers.all()
    profile_following = user_profile.following.all()
    followers_count = profile_followers.count()
    following_count = profile_following.count()
    user_posts = Post.objects.filter(user=user_id).all().order_by("-timestamp")

    try:
        current_user = User.objects.get(username=request.user)
        is_following = current_user in [follower.follower for follower in profile_followers]
    except User.DoesNotExist:
        is_following = False

    return render(request, "network/user.html", {
        "user_profile": user_profile,
        "followers_count": followers_count,
        "following_count": following_count,
        "user_posts": user_posts,
        "is_following": is_following,
    })

@login_required
def follow(request, user_id):
    if request.method == 'POST':
        current_user = User.objects.get(username=request.user)
        user_profile = User.objects.get(id=user_id)

        follow = Follow(follower=current_user, profile=user_profile)
        follow.save()
        messages.success(request, f"You now follow {user_profile}")
        return redirect(reverse("user_profile", args=[user_id]))
    else:
        return HttpResponseRedirect(reverse("index"))

@login_required
def unfollow(request, user_id):
    if request.method == 'POST':
        current_user = User.objects.get(username=request.user)
        user_profile = User.objects.get(id=user_id)

        follow = Follow.objects.filter(follower=current_user, profile=user_profile).all()
        follow.delete()
        messages.success(request, f"You unfollowed {user_profile}")
        return redirect(reverse("user_profile", args=[user_id]))
    else:
            return HttpResponseRedirect(reverse("index"))

@login_required
def create_post(request):
    if request.method == "POST":
        user = request.user
        content = request.POST["post"]
        post = Post(content=content, user=user)
        post.save()
        messages.success(request, "Your post was published!")
        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
