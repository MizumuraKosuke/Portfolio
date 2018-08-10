from django.shortcuts import render
from .forms import ArtistForm, LiveForm, AudienceForm

def reserve(request):
    return render(request, 'reserve/reserve.html', {})

def audience_form(request):
    if request.method == "POST":
        form = AudienceForm(request.POST)
        if form.is_valid():
            post = form.save()
            return render(request, 'reserve/reserve.html', {})
    else:
        form = AudienceForm()
    return render(request, 'reserve/audience_form.html', {'form': form})

def artist_form(request):
    if request.method == "POST":
        form = LiveForm(request.POST)
        if form.is_valid():
            post = form.save()
            return render(request, 'reserve/reserve.html', {})
    else:
        form = LiveForm()
    return render(request, 'reserve/artist_form.html', {'form': form})

