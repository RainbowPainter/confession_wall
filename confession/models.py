from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import os


def validate_image_size(value):
    filesize = value.size
    if filesize > 5 * 1024 * 1024:  # 5MB
        raise ValidationError("图片大小不能超过5MB")


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_banned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Confession(models.Model):
    STATUS_CHOICES = (
        ('pending', '待审核'),
        ('approved', '已通过'),
        ('rejected', '已拒绝'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="表白内容")
    image = models.ImageField(
        upload_to='confessions/',
        blank=True,
        null=True,
        verbose_name="图片",
        validators=[validate_image_size]
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    likes_count = models.IntegerField(default=0)
    is_pinned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    confession = models.ForeignKey(Confession, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'confession']

    def __str__(self):
        return f"{self.user.username} liked {self.confession.id}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    confession = models.ForeignKey(Confession, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="评论内容")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}"