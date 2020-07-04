from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from .forms import UserRegisterForm, UserloginForm, UserProfileForm, UserEditForm, UserPasswordEditForm
from django.contrib.auth.forms import PasswordChangeForm
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import os
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from Torrents.models import Comments,Likes, UploadTorrents



def signin_view(request):
    try:
        my_form = UserloginForm()
        context = {
            "form": my_form,
            "error": "",
            "avatar": "",
        }

        if request.method == "POST":
            my_form = UserloginForm(request.POST or None)
            if my_form.is_valid():
                username = my_form.cleaned_data['Usr_Name']
                password = my_form.cleaned_data['Usr_Pwd']
                user = authenticate(username=username, password=password)
                login(request, user)

                return redirect("homepage")

            else:
                print(my_form.errors.as_text)

    except AttributeError:
        context["error"] = "Invalid Username/password"

    return render(request, "registration/login.html", context)


def signup_view(request):
    my_form = UserRegisterForm()
    profile_form = UserProfileForm()

    if request.method == "POST":
        my_form = UserRegisterForm(request.POST or None)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if my_form.is_valid() and profile_form.is_valid():
            user = my_form.save()
            print(user.id)
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            username = my_form.cleaned_data['username']
            password = my_form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect("homepage")

        else:
            print(my_form.is_valid())
            print(my_form.errors.as_text())

    return render(request, "registration/register.html", context={"form": my_form, "profile_form": profile_form})


def logout_view(request):

    logout(request)
    return redirect('/')


def account_view(request):

    context = {
        "user_profile": UserProfile.objects.all(),
    }
    return render(request, "user-account/account-info.html", context)


def user_edit_view(request):
    user_form = UserPasswordEditForm()  # User Model
    editForm = UserEditForm()  # Custom Model

    context = {
        "user_profile": UserProfile.objects.all(),
        "form": editForm,
        "user_form": user_form,
        "username_error": "",
        "email_error": ""
    }
    if request.method == "POST":
        image_file_name = ""
        user_form = UserPasswordEditForm(request.POST, instance=request.user)
        editForm = UserEditForm(
            request.POST, request.FILES, instance=request.user)

        if bool(request.FILES.get('image_field', False)) == True:
            image_file_name = request.FILES['image_field']

        if editForm.is_valid() and user_form.is_valid():
            user_form.save()
            user = request.user
            email = editForm.cleaned_data['email']
            first_name = editForm.cleaned_data['first_name']
            profile_status = editForm.cleaned_data['profile_status']

            UserProfile.objects.filter(user_id=user.id).update(
                email=email, first_name=first_name,profile_status=profile_status)
        
            Comments.objects.filter(user_id=user.id).update(user_name=user.username)
            Likes.objects.filter(user_id=user.id).update(liked_by = user.username)

            if image_file_name != "":
                m = UserProfile.objects.get(user_id=user.id)
                try:
                    os.remove(str(m.image_field))
                except FileNotFoundError:
                    print("old file not found")
                m.image_field = request.FILES['image_field']
                m.save()
                Comments.objects.filter(user_id=request.user.id).update(user_avatar=UserProfile.objects.get(user_id=user.id).image_field )
                return redirect('account-info')
            else:
                return redirect('account-info')

        else:
            if "username" in user_form.errors:
                context["username_error"] = user_form.errors['username']
            if "email" in editForm.errors:
                context["email_error"] = editForm.errors["email"]

    return render(request, "user-account/account-edit.html", context)


def user_change_password(request):
    form = PasswordChangeForm(request.user)

    context = {
        'form': form,
        "user_profile": UserProfile.objects.all(),
        "message_success":"",
        "errors":"",
    }
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            context['message_success'] = "Password updated successfully"
            return render(request, 'user-account/change-password.html',context)
        else:
            messages.error(request, 'Please correct the error below.')
            if "new_password2" in form.errors:
                context["errors"] = form.errors["new_password2"]
               
            if "old_password" in form.errors:
                context["errors"] += form.errors["old_password"]
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'user-account/change-password.html',context)


def uploaded_torrents(request):

    context = {
	"user_profile":UserProfile.objects.all(),
	"torrents": UploadTorrents.objects.filter(user_id = request.user.id),
	}

    return render(request, 'user-account/uploaded_torrents.html', context);

