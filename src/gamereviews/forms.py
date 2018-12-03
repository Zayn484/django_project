from django import forms
from .models import News, Reviews, Topgames, Slideshow


class NewsCreateForm(forms.ModelForm):
    class Meta:
        model = News
        fields = [
            'title',
            'category',
            'imgs',
            'info',
            'content'
        ]

class ReviewsCreateForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields =[
            'title',
            'imgs',
            'gameplay',
            'info',
            'content',
            'category',
            'cpu',
            'gpu',
            'ram',
            'space',
            'os'
        ]

class TopgamesCreateForm(forms.ModelForm):
    class Meta:
        model = Topgames
        fields =[
            'title',
            'imgs',
            'release_date',
            'content'
        ]



class SlideshowCreateForm(forms.ModelForm):
    class Meta:
        model = Slideshow
        fields =[
            'imgs'
        ]

