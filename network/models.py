from django.contrib.auth.models import AbstractUser
from django.db import models

# add additional models to represent details about posts, likes, and followers.
# python manage.py makemigrations
# python manage.py migrate 
class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=1000)
    likes = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def like(self):
        self.likes += 1
        self.save()

    def unlike(self):
        if self.likes > 0:
            self.likes -= 1
            self.save()
    
    def __str__(self):
        return f"Posted by {self.user.username} at {self.timestamp}"
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_given')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes_received')

    class Meta:
        unique_together = ['user', 'post']