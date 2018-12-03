from django import forms
from .models import Comment



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content_type','object_id','comment_content']
        widgets = {'content_type': forms.HiddenInput(),'object_id': forms.HiddenInput(),}
        labels = {'comment_content': ''}