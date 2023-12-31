from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()


class Profile(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  id_user = models.IntegerField()
  bio = models.TextField(blank=True)
  profile_img = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
  location = models.CharField(max_length=100, blank=True)

  def __str__(self):
    return self.user.username

class Post(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4)
  user = models.ForeignKey(Profile, on_delete=models.CASCADE)
  image = models.ImageField(upload_to='post_images')
  caption = models.TextField()
  created_at = models.DateTimeField(default=datetime.now)
  no_of_likes = models.IntegerField(default=0)

  def __str__(self):
    return self.user.user.username + " - " + str(self.id)

class LikePost(models.Model):
  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  user = models.ForeignKey(Profile, on_delete=models.CASCADE)

  def __str__(self):
    return self.user.user.username

class Follow(models.Model):
  follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='following')
  followee = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followee')

  def __str__(self):
    return self.follower.user.username + self.followee.user.username