from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image_field = models.ImageField(upload_to = 'static/user_images',null=True, blank = True)
    email = models.EmailField(max_length=30,blank=False, null= False, unique= True)
    first_name = models.CharField(max_length=20)
    profile_status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
