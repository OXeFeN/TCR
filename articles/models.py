from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='articles'
    )

    class Meta:
        permissions = [
            ("can_publish_article", "Can publish article"),
        ]

    def __str__(self):
        return self.title

