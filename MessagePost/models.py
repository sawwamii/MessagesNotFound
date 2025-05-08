from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class postData(models.Model):
    data = models.JSONField()
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)

    def __str__(self):
        return f"this truly is data {self.id}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.user.username

class Comment(models.Model):
    post = models.ForeignKey('postData', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}: {self.content[:20]}"