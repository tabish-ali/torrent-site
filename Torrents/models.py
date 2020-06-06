from django.db import models
from datetime import date

class UploadTorrents(models.Model):

    torrent_name= models.CharField(max_length=50)
    torrent_description = models.CharField(max_length=250)
    torrent_image = models.ImageField(upload_to = 'static/torrent_images/',blank=False,null=True)
    torrent_file = models.FileField(upload_to='static/torrent-files/',blank=False,null=False)
    likes = models.IntegerField(default=False)
    unlikes = models.IntegerField(default=False)
    uploader_name = models.CharField(max_length=50)
    user_id = models.IntegerField(default=False)

class Likes(models.Model):
 
    user_id = models.IntegerField()
    post_id = models.IntegerField()
    liked = models.BooleanField()
    unliked = models.BooleanField()
    liked_by = models.CharField(max_length=50,blank=True)
    unliked_by = models.CharField(max_length=50,blank=True)

class Comments(models.Model):
    user_id = models.IntegerField()
    post_id = models.IntegerField()
    user_name = models.CharField(max_length=50)
    comment = models.CharField(max_length=1000)
    user_avatar = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
 
