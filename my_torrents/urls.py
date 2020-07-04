from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from Pages.views import home_view, contact_view,about_view
from Users.views import signin_view,signup_view,logout_view,account_view, uploaded_torrents, user_edit_view, user_change_password
from Torrents import views as torrent_views
from django.conf.urls import include
from django.conf.urls import url


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view,name="homepage"),
    path('contact/', contact_view),
    path('about/', about_view,name='about'),
    path('register/',signup_view,name='register'),
    path('login/',signin_view,name='login'),
    # path('upload_torrent/',torrent_views.torrents_upload_view),
    path('torrents/', torrent_views.torrents_list, name="torrents"),
    path('accounts/logout/',logout_view),
    path('account-info/',account_view,name="account-info"),
    path('account-edit/',user_edit_view),
    path('torrents_list/',torrent_views.torrents_list_view,name='torrents_list_view'),
    path('torrent/<int:pk>/',torrent_views.torrents_view, name='torrents_view'),
    path('home/<int:pk>/',torrent_views.delete_torrent, name='delete_torrent'),
    path('change-password/',user_change_password,name="change-password"),

    path('uploaded_torrents/', uploaded_torrents, name="uploaded_torrents"),
    
    path('<int:pk>',torrent_views.file_download_view,name='file_download_view'),
    url(r'^ajax/validate_like/$', torrent_views.validate_like, name='validate_like'),
    url(r'^ajax/get_like_list/$', torrent_views.get_like_list, name='get_like_list'),
    url(r'^ajax/validate_unlike/$', torrent_views.validate_unlike, name='validate_unlike'),
    url(r'^ajax/submit_comment/$', torrent_views.submit_comment, name='submit_comment'),
    path('accounts/', include('django.contrib.auth.urls')),

]
urlpatterns += staticfiles_urlpatterns()