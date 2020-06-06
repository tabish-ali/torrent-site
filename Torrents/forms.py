from django import forms 
from .models import UploadTorrents,Comments


class UserUploadForm(forms.ModelForm):
    class Meta:
        model = UploadTorrents
        fields = {
            'torrent_name',
            'torrent_description',
            'torrent_image',
            'torrent_file',
            'date_of_c',
                }
    
    torrent_name = forms.CharField(label='Name',required=True,
                            widget=forms.TextInput(
							attrs={'placeholder':'Name','class':'form-control my-input'}))   
    torrent_description = forms.CharField(label='description',required=True,
                            widget=forms.TextInput(
							attrs={'placeholder':'description','class':'form-control my-input'}))   

    date_of_c = forms.CharField(required=False)

class CommentBlock(forms.ModelForm):
    class Meta:
        model = Comments
        fields = {
            'comment',
        }
    comment = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder':'comment...','row':'5','col': '1','id':'comments'}))