from django import forms
from .models import Artist, Live, Audience

class ArtistForm(forms.ModelForm):

    class Meta:
        model = Artist
        fields = ('name','url','Twitter',)


class LiveForm(forms.ModelForm):

    class Meta:
        model = Live
        fields = ('name', 'artists', 'place', 'url', 'date', 'open_time', 'start_time', 'adv', 'door', 'published_date',)


class AudienceForm(forms.ModelForm):

    class Meta:
        model = Audience
        fields = ('live', 'name', 'mail', 'ticket',)