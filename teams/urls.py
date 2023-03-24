from django.urls import path
from .views import editteam, team_details
app_name = 'teams'
urlpatterns = [
    path('<int:pk>/edit-team/', editteam, name='edit'),
    path('<int:pk>/details/',team_details , name='details'),
]