from django.contrib.auth.models import AbstractUser
from django.db import models

# add additional models to represent details about posts, likes, and followers.
# python manage.py makemigrations
# python manage.py migrate 
class User(AbstractUser):
    pass

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['follower', 'profile']

    def __str__(self):
        return f'{self.follower} follows {self.profile}'

    @staticmethod
    def get_followers_count(user_id):
        return Follow.objects.filter(following=user_id).count()

    @staticmethod
    def get_following_count(user_id):
        return Follow.objects.filter(follower=user_id).count()

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=1000)
    likes = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Posted by {self.user.username} at {self.timestamp}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_given')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes_received')

    class Meta:
        unique_together = ['user', 'post']