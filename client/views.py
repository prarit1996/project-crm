import csv
from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import client, ClientFiles
from django.contrib.auth.decorators import login_required
from .forms import AddClientForm, AddCommentForm, AddFileForm
from django.contrib import messages
from teams.models import Team
from django.http import HttpResponse
# Create your views here.
@login_required
def clientslist(request):
    clients = client.objects.filter(created_by =request.user)
    return render(request, "client/clients_list.html", {'clients': clients})

@login_required
def clientdetails(request, pk):
    clientdetail = client.objects.get(created_by= request.user, pk = pk)
    comment={}
    form = AddCommentForm()
    fileform = AddFileForm()
    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            team = Team.objects.filter(created_by=request.user)[0]
            comment = form.save(commit=False)
            comment.created_by = request.user
            comment.client_id=pk
            comment.team =team
            comment.save()
            return redirect("clients:details", pk=pk)
    return render(request, "client/client_details.html", {"client": clientdetail, 'form': form, 'fileform': fileform})

@login_required
def AddFileView(request, *args, **kwargs):
    pk = kwargs.get('pk')
    form = AddFileForm(request.POST, request.FILES)
    commentform = AddCommentForm()
    if form.is_valid():
        team = Team.objects.filter(created_by=request.user)[0]
        file = form.save(commit=False)
        file.created_by = request.user
        file.Client_id = pk
        file.team= team
        file.save()
    return redirect("clients:details",pk=pk)

@login_required
def clientedit(request,pk):
    clientdata = client.objects.get(created_by = request.user, pk= pk)
    form = AddClientForm(instance=clientdata)
    if request.method == 'POST':
        form = AddClientForm(request.POST, instance=clientdata)
        if form.is_valid():
            clientdata.save()
            messages.success(request, "Client details updated successfully")
            return redirect(reverse('clients:list'))
    return render(request, 'client/client_edit.html', {'form': form})

@login_required
def clientadd(request):
    form = AddClientForm()
    team = Team.objects.filter(created_by=request.user)[0]
    if request.method == 'POST':
        form = AddClientForm(request.POST)
        if form.is_valid():
            clientdetail = form.save(commit=False)
            clientdetail.created_by = request.user
            clientdetail.team=team
            clientdetail.save()
            messages.success(request, "Client created successfully")
            return redirect(reverse('clients:list'))
    return render(request, 'client/client_add.html', {'form': form, 'team': team})

@login_required
def deleteclient(request, pk):
    clientdata = client.objects.get(created_by= request.user, pk=pk)
    clientdata.delete()
    messages.success(request, "Client Deleted successfully")
    return redirect('clients:list')

@login_required
def clientExport(request):
    clients= client.objects.filter(created_by=request.user)
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="clients.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow(['Client Name', 'Description', 'Created By', 'Created At'])
    for clientdata in clients:
        writer.writerow([clientdata.name, clientdata.description, clientdata.created_by, clientdata.created_at])
    return response