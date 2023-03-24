from .models import Team

def team(request):
    team= None
    if request.user.is_authenticated:
        team= Team.objects.filter(created_by=request.user)[0]
    return {'team':team}