from django.urls import path
from .views import clientslist, clientdetails, clientadd, deleteclient, clientedit, AddFileView, clientExport
app_name= 'clients'
urlpatterns = [
    path('client-list/', clientslist, name = 'list'),
    path('<int:pk>', clientdetails, name = 'details'),
    path('<int:pk>/delete', deleteclient, name = 'delete'),
    path('add-client/', clientadd,name='add'),
    path('<int:pk>/edit-client/', clientedit, name='edit'),
    path('<int:pk>/add_comment', clientdetails, name = 'addcomment'),
    path('<int:pk>/add_file', AddFileView , name = 'addfile'),
    path('export/', clientExport, name='clientexport'),
]