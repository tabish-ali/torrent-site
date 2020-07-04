from django.shortcuts import render
from django.http import HttpResponse
from Users.models import UserProfile
from Torrents.models import UploadTorrents, Likes
from django.forms.models import model_to_dict
from django.core import serializers
import json
from django.http import JsonResponse
from Torrents.views import get_torrent_info

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

	latest_five = {}

	torrents = UploadTorrents.objects.all().order_by('id')[:5]

	for torrent in torrents:
		meta_data = get_torrent_info(torrent.id)
		latest_five[meta_data['info']['name']] = torrent

	top_liked = {}

	torrents = UploadTorrents.objects.all().order_by('-total_likes')[:5]

	for torrent in torrents:
		meta_data = get_torrent_info(torrent.id)
		top_liked[meta_data['info']['name']] = torrent


	context = {
	"user_profile":UserProfile.objects.filter(user_id = request.user.id),
	"latest_five": latest_five,
	"top_liked" : top_liked,
	}

	return render(request,"home.html",context)

	