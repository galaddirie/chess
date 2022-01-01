from django import forms
from django.forms.widgets import TimeInput


from .models import Game

class GameCreationForm(forms.ModelForm):
    SIDE_CHOICES = (
        ('white', 'white'),
        ('black', 'black')
    )
    
    #move_by = forms.TimeField(widget=TimeInput)
    side = forms.ChoiceField(choices=SIDE_CHOICES)
    class Meta:
        model = Game
        fields =  []