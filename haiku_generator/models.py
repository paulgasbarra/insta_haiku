# haiku_generator/models.py

from django.db import models

class Haiku(models.Model):
    text = models.TextField()
    image = models.ImageField(upload_to='haiku_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)
    seed_words = models.CharField(max_length=255, blank=True, null=True)
    alt_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.text[:50]
