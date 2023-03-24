from django.contrib.auth.forms import authenticate
from django.shortcuts import render, redirect
from .models import Userprofile
from django.contrib.auth.decorators import login_required
from teams.models import Team
from .forms import SignUpForm
# Create your views here.
def signup(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Userprofile.objects.create(user = user)
            team =Team.objects.create(name= user.username + "'s Team", created_by=user)
            team.members.add(user)
            team.save()
            return redirect('../login/')
    else:
        form = SignUpForm()

    return render(request, 'userprofile/signup.html', {'form': form})

@login_required
def myaccount(request):
    team=Team.objects.filter(created_by=request.user)[0]
    return render(request, 'userprofile/myaccount.html', {'team': team})


