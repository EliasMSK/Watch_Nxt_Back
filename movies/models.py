from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    genre = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    poster = models.URLField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.title