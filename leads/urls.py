from django.urls import path
from .views import addlead, leadlist, leaddetails, delete_lead, edit_lead, converToClient, LeadListView, \
    LeadDetailView, LeadDeleteView, LeadUpdateView, LeadCreateView, ConvertToClientView, AddCommentView, AddFileView, \
    leadsExport
app_name='leads'
urlpatterns = [
    path('add-lead/', LeadCreateView.as_view(), name='add'),
    path('<int:pk>/', LeadDetailView.as_view(), name = 'details'),
    path('<int:pk>/delete/', LeadDeleteView.as_view(), name='delete'),
    path('<int:pk>/update/', LeadUpdateView.as_view(), name='edit'),
    path('<int:pk>/convert/', ConvertToClientView.as_view(), name='convert'),
    path('lead-list/', LeadListView.as_view() , name='list'),
    path('<int:pk>/add-comments/', AddCommentView.as_view(), name='addcomment'),
    path('<int:pk>/add-files/', AddFileView.as_view(), name='addfile'),
    path('export/', leadsExport, name='leadexport')

]