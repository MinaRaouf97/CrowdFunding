from django import forms
from taggit.forms import *

class AddCommentForm(forms.Form):
    comment = forms.CharField(
        min_length=10,
        max_length = 200,
        label='',
        widget=forms.Textarea(
                    attrs={
            "class":"materialize-textarea"
        }
        )
    )
    CHOICES = (('5', 'Amazing'), ('4', 'Very Good'),('3', 'Good'),('2', 'Not bad'),('1', 'Bad'))
    rate = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)



