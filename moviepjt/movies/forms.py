from django import forms
from .models import *

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ('title', 'overview', 'release_date', 'genres')

class ReviewForm(forms.ModelForm):
    rank = forms.IntegerField(max_value=10, min_value=0)
    class Meta:
        model = Review
        fields = ('title', 'rank', 'content',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)