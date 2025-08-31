from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class StreamPlatform(models.Model):
    name = models.CharField(max_length=30)
    about = models.CharField(max_length=150)
    website = models.URLField(max_length=100)
    
    def __str__(self):
        return f"{self.name}"


class WatchList(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    active = models.BooleanField(default=True)
    created = models.DateField(auto_now=True)
    platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name='watchlist')
    avg_rating = models.FloatField(default=0)
    number_rating = models.IntegerField(default=0)
    
    
    def __str__(self):
        return f"{self.title}"
    

class Reviews(models.Model):
    review_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_user')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(null=True)
    created = models.DateField(auto_now_add=True)
    update = models.DateField(auto_now=True)
    active = models.BooleanField(default=True)
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE, related_name='reviews')
    
    
    def __str__(self):
        return f'({self.rating}), {self.watchlist.title}'