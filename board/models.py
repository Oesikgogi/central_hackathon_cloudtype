# community/board/models.py

from django.db import models
from member.models import CustomUser

class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='board_posts')
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='board_comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

from django.db import models

class Facility(models.Model):
    name = models.CharField(max_length=200)
    region = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    sport = models.CharField(max_length=100)
    target = models.CharField(max_length=100)
    period = models.CharField(max_length=100)
    day = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    fee = models.IntegerField()
    capacity = models.IntegerField()

    def __str__(self):
        return self.name
