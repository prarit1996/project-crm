from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Team
from .forms import TeamForm

# Create your views here.

@login_required
def team_details(request, pk):
    team = Team.objects.filter(created_by=request.user, pk=pk)[0]
    return render(request, 'teams/team_details.html', {'team': team})


@login_required
def editteam(request, pk):
    team = get_object_or_404(Team, created_by=request.user, pk=pk)
    teameditform = TeamForm(instance=team)
    if request.method == 'POST':
        teameditform = TeamForm(request.POST, instance=team)
        teameditform.save()
        messages.success(request, message='The team name changed successfully.')
        return redirect('userprofile:myaccount')

    return render(request, 'teams/edit_team.html', {'team': team, 'form': teameditform})
