from django.db import models
from datetime import date
from django.contrib.auth.models import User

class UploadTorrents(models.Model):

    user = models.ForeignKey(User, on_delete = models.CASCADE)
    torrent_description = models.CharField(max_length=500)
    torrent_image = models.ImageField(upload_to = 'static/torrent_images/',blank=True, null=True)
    torrent_file = models.FileField(upload_to='static/torrent-files/',blank=False, null=False)
    total_likes = models.IntegerField(default=0, blank = True)
    total_unlikes = models.IntegerField(default=0, blank = True)
    uploader_name = models.CharField(max_length=50, blank = True, default='tabish')
    created_at = models.DateTimeField(auto_now_add=True)

class Likes(models.Model):
 
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    post = models.ForeignKey(UploadTorrents, on_delete = models.CASCADE)
    liked = models.BooleanField()
    unliked = models.BooleanField()
    liked_by = models.CharField(max_length=50,blank=True)
    unliked_by = models.CharField(max_length=50,blank=True)


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    post = models.ForeignKey(UploadTorrents, on_delete = models.CASCADE)
    user_name = models.CharField(max_length=50)
    comment = models.CharField(max_length=1000)
    user_avatar = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
 
