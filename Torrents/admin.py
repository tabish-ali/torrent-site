from django.contrib import admin
from .models import UploadTorrents, Likes, Comments

# Register your models here.
admin.site.register(UploadTorrents)
admin.site.register(Likes)
admin.site.register(Comments)
