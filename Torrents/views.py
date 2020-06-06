from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import UserUploadForm, CommentBlock
from .models import UploadTorrents,Likes,Comments
from Users.models import UserProfile
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.forms.models import model_to_dict
from django.core import serializers
import json
import os
import bencode
import hashlib


def torrents_view(request, pk):
    liked_status = False
    unliked_status = False   
    obj = UploadTorrents.objects.get(pk=pk)
    likes = Likes.objects.all()
    commments = Comments.objects.filter(post_id = pk)
    files =[]
    tracker_list =[]

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    torrent = UploadTorrents.objects.get(id=pk)
    field_path = torrent.torrent_file
    file_path = os.path.join(BASE_DIR, str(field_path))
    torrent_file = open(str(field_path),'rb').read()


    data = bencode.decode(torrent_file)


    info_hash = hashlib.sha1(bencode.bencode(data['info'])).hexdigest()


    announce = data['announce']
    announce_list =data['announce-list']
    comment = data['comment']
    created_by = data['created by']
    name = data['info']['name'] 
    date = data['creation date']
    total_size = 0 
    filename_size = {}
    try:
        files = data['info']['files']
        file_flag = 1
    except KeyError:
        files = data['info']['name']
        total_size = data['info']['length']
        total_size = total_size_estimate(total_size)
        file_flag = 0

    if file_flag == 1:
        for t_f in files:
            if t_f['length'] >= 1e3 and t_f['length']<1e6:
                size = round(t_f['length']/1e3,2)
                filename_size[' / '.join(t_f['path'])] = str(size) + ' KB'

            elif t_f['length'] >= 1e6 and t_f['length']<1e9:
                size = round(t_f['length']/1e6,2)
                filename_size[' / '.join(t_f['path'])]= str(size) + ' MB' 

            elif t_f['length'] >= 1e9 and t_f['length']<1e12:
                size = round(t_f['length']/1e9,2)
                filename_size[' / '.join(t_f['path'])]= str(size) + ' GB'

            total_size += t_f['length']

        total_size = total_size_estimate(total_size)
    
    try:
        likes_obj = Likes.objects.get(post_id=pk,user_id=request.user.id)
        liked_status = likes_obj.liked
        unliked_status = likes_obj.unliked
      

    except ObjectDoesNotExist:
        liked_status = False
        unliked_status = False

    context ={"selected_torrent" :obj,
    "user_profile":UserProfile.objects.all(),
    "liked_status":liked_status,
    "unliked_status":unliked_status,
    "likes":likes,
    "torrent_comments": commments,
    "comment_area" : CommentBlock(), 
    "announce":announce,
    "announce_list":announce_list,
    "created_by":created_by,
    "filename_size":filename_size,
    "info_hash":info_hash, 
    "total_size":total_size,
    "name":name,
    }

    return render(request,"torrents/torrent.html",context)

def total_size_estimate(total_size):
    if total_size >= 1e3 and total_size < 1e6:
        total_size = round(total_size/1e3,2)
        total_size = str(total_size) +' KB'

    elif total_size >= 1e6 and total_size < 1e9:
        total_size = round(total_size/1e6,2)
        total_size = str(total_size) +' MB'

    elif total_size >= 1e9 and total_size < 1e12 :
        total_size = round(total_size/1e9,2)
        total_size = str(total_size) +' GB'
    
    return total_size 

def file_download_view(request, pk):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    torrent = UploadTorrents.objects.get(id=pk)
    
    field_path = torrent.torrent_file
    file_path = os.path.join(BASE_DIR, str(field_path))
    
    torrent_file = open(str(field_path),'rb')

    response = HttpResponse(torrent_file.read(),content_type='application/force-download')
    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
    return response

def torrents_upload_view(request):
    
    uploadForm = UserUploadForm()
    upload = False
    context ={
	"uform": uploadForm,    
    "user_profile": UserProfile.objects.all(),
	}

    if request.method == "POST":

        uploadForm = UserUploadForm(request.POST, request.FILES)
       
        if uploadForm.is_valid():
            image = request.FILES['torrent_image']
            name = uploadForm.cleaned_data['torrent_name']
            
            torrent_file = request.FILES['torrent_file']
            description = uploadForm.cleaned_data['torrent_description']

            UploadTorrents.objects.create(torrent_name=name,
            torrent_description=description,
            torrent_file=torrent_file,
            torrent_image=image, user_id=request.user.id,
            uploader_name = request.user)

            upload = True
        else:
            print(uploadForm.errors.as_text)
    if not upload:
        return render(request,"torrents/upload_torrent.html",context)
    else:
        return redirect("torrents_list_view")


def torrents_list_view(request):
    obj = UploadTorrents.objects.all()
    user_profile = UserProfile.objects.all()
    context = {
        "torrents" : obj,
        "user_profile":user_profile,
        }

    return render(request,"torrents/torrents_list.html",context)

def validate_like(request):
    updated_like = ""
    updated_unlikes =""
    is_liked = False
    user_id = request.GET.get("user_id")
    post_id = request.GET.get("post_id")
    
    post = UploadTorrents.objects.get(id=post_id)
    liked_obj = Likes.objects.filter(user_id=user_id,post_id=post_id)
    if liked_obj.count() == 0:
        Likes.objects.create(user_id=user_id,post_id=post_id,
        liked_by=str(request.user),liked=True,unliked=False)
        post.likes += 1
        post.save()
        is_liked =True
    else:  
        try:
            obj = Likes.objects.get(user_id=user_id,post_id=post_id)
            if liked_obj.count()== 1:
                if(obj.unliked):
                    obj.unliked = False
                    obj.liked = True
                    obj.liked_by = str(request.user)
                    obj.unliked_by = ""
                    obj.save()
                    post.unlikes -= 1
                    post.likes += 1
                    post.save()
                    is_liked = True

                elif obj.liked:
                    liked_obj.delete()
                    post.likes -= 1
                    post.save()
                    
        except ObjectDoesNotExist:
                                print("object does not exist")

    update = UploadTorrents.objects.get(id=post_id)
    updated_like = update.likes
    updated_unlikes = update.unlikes

    data = {
        'updated_like': updated_like,
        'updated_unlikes': updated_unlikes,
        'is_liked': is_liked,
    }
    return JsonResponse(data)



def get_like_list(request):
    post_id = request.GET.get("post_id")
    likes_list = Likes.objects.filter(post_id=post_id)
    liked_by_list=[]
    disliked_by_list=[]

    for obj in likes_list:
        liked_by_list.append(obj.liked_by)
        disliked_by_list.append(obj.unliked_by)

    data = {
    'like_list': liked_by_list,
    'dislike_list':disliked_by_list,
    }
    return JsonResponse(data,safe=False)


def validate_unlike(request):
    updated_like = ""
    updated_unlikes =""
    is_unliked = False

    user_id = request.GET.get("user_id")
    post_id = request.GET.get("post_id")
    post = UploadTorrents.objects.get(id=post_id)
    liked_obj = Likes.objects.filter(user_id=user_id,post_id=post_id)
        
    if liked_obj.count() == 0:
        Likes.objects.create(user_id=user_id,post_id=post_id,
        unliked_by=str(request.user),liked=False,unliked=True)
        post.unlikes += 1
        post.save()
        is_unliked =True
    else:
        try:
            obj = Likes.objects.get(user_id=user_id,post_id=post_id)
            if liked_obj.count() == 1:
                if(obj.liked):
                    obj.liked = False
                    obj.unliked = True
                    obj.unliked_by = str(request.user)
                    obj.liked_by = ""
                    obj.save()
                    post.likes -= 1
                    post.unlikes += 1
                    post.save()
                    is_unliked = True

                elif obj.unliked:
                    liked_obj.delete()
                    post.unlikes -= 1
                    post.save()

        except ObjectDoesNotExist:
                                print("object does not exist")

      
    update = UploadTorrents.objects.get(id=post_id)
    updated_like = update.likes
    updated_unlikes = update.unlikes

    data = {
        'updated_like':updated_like,
        'updated_unlikes': updated_unlikes,
        'is_unliked': is_unliked,
    }
    return JsonResponse(data)

def submit_comment(request):

    latest_comment = ""

    user_id = request.GET.get("user_id")
    post_id = request.GET.get("post_id")
    comment = request.GET.get("comment")
    user_pic = UserProfile.objects.get(user_id=request.user.id).image_field

    comment_obj = Comments()
    comment_obj.user_id = user_id
    comment_obj.post_id = post_id
    comment_obj.comment = comment
    comment_obj.user_name = request.user
    comment_obj.user_avatar = user_pic
    comment_obj.save()

    latest_comment_obj = Comments.objects.get(pk=comment_obj.pk)
    latest_comment = latest_comment_obj.comment
    user_name = latest_comment_obj.user_name

    data = {
        'latest_comment':latest_comment,
        'user_name' : user_name,
    }
    return JsonResponse(data, safe=False)

def delete_torrent(request,pk):
    UploadTorrents.objects.filter(id=pk).delete()
    Comments.objects.filter(post_id=pk).delete()

    context = {
	    "user_profile":UserProfile.objects.all(),
	    "torrents": UploadTorrents.objects.filter(user_id = request.user.id),
	}
    return render(request,"home.html",context)