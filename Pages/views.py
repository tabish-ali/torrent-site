from django.shortcuts import render
from django.http import HttpResponse
from Users.models import UserProfile
from Torrents.models import UploadTorrents, Likes
from django.forms.models import model_to_dict
from django.core import serializers
import json
from django.http import JsonResponse

# Create your views here.
def about_view(request):
	context = {
	"user_profile":UserProfile.objects.all(),
	"torrents": UploadTorrents.objects.filter(user_id = request.user.id),
	}
	return render(request,"about.html",context)

def contact_view(request):
	return render(request,"contact.html",{})

def home_view(request):
	context = {
	"user_profile":UserProfile.objects.all(),
	"torrents": UploadTorrents.objects.filter(user_id = request.user.id),
	}
	return render(request,"home.html",context)

	