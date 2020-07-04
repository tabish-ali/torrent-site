from django import forms 
from .models import UploadTorrents,Comments


class UserUploadForm(forms.ModelForm):
    class Meta:
        model = UploadTorrents
        fields = {
            'torrent_description',
            'torrent_image',
            'torrent_file',
                }
    torrent_description = forms.CharField(label='description',required=True,
                            widget=forms.Textarea(
							attrs={'placeholder':'description','class':'form-control my-input',
                            'rows': 1,
                                  'cols': 40}))   


class CommentBlock(forms.ModelForm):
    class Meta:
        model = Comments
        fields = {
            'comment',
        }
    comment = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder':'comment...','row':'5','col': '1','id':'comments'}))