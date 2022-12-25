from platform import mac_ver
from tkinter import CASCADE
from unicodedata import category
from django.contrib.auth.models import AbstractUser
from django.db import models
# Importing it to use it in the date field.
from django.utils import timezone
class User(AbstractUser):
    pass
    def __str__(self):
        return f"{self.username}"
class Listing(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(
            blank=True,
            max_length= 200
    )
    category = models.CharField(default="other",
        blank=True,
       max_length=50)
    price = models.FloatField(blank=False)
    date = models.DateTimeField(default=timezone.now)
    image = models.CharField(blank = True, max_length=2000)
    active = models.BooleanField(default=True)
    creator = models.ForeignKey(
        User, 
        on_delete= models.CASCADE,
        related_name="creator"
    )
class Bid(models.Model):
    user = models.ForeignKey(
        User,
        on_delete= models.CASCADE,
        related_name="bider"
    )
    item = models.ForeignKey(
        Listing, 
        on_delete= models.CASCADE,
        related_name="list"
    )
    bid = models.IntegerField(default=0)
    numberofbids = models.IntegerField(default=0)
    # The purpose of this class is to define to the objects.latest function
    # That it work on the bid column
    class Meta:
        get_latest_by = 'bid'
class Comment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete= models.CASCADE,
        related_name="commenter"
    )
    item = models.ForeignKey(
        Listing, 
        on_delete= models.CASCADE,
        related_name="commented_item"
    )
    comment = models.CharField(max_length=1000)
class watchlist(models.Model):
    user = models.ForeignKey(
        User,
        on_delete= models.CASCADE,
        related_name="watcher"
    )
    item = models.ForeignKey(
        Listing, 
        on_delete= models.CASCADE,
        related_name="watche_item"
    )
    watched = models.BooleanField(default=False)
    number_watch = models.IntegerField(default=0)
