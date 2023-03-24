from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import AddLeadForm, AddCommentForm
from .models import Lead
from django.contrib import messages
from client.models import client
from teams.models import Team


@login_required
def leadlist(request):
    leads = Lead.objects.filter(created_by = request.user, converted_to_client=False)
    return render(request, 'leads/leadlist.html', {'leads': leads})


@login_required
def leaddetails(request, pk):
    #lead = Lead.objects.filter(created_by = request.user).get(pk = pk)
    #one more method
    lead = get_object_or_404(Lead, created_by = request.user, pk=pk)
    return render(request, 'leads/leaddetails.html', {'lead': lead})

@login_required
def delete_lead(request, pk):
    lead = get_object_or_404(Lead, created_by = request.user, pk=pk)
    lead.delete()
    return redirect(reverse('leads:list'))


@login_required
def edit_lead(request,pk):
    lead = get_object_or_404(Lead, created_by = request.user, pk=pk)
    form = AddLeadForm(instance=lead)
    if request.method == 'POST':
        form = AddLeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            messages.success(request, "Lead details updated successfully")
            return redirect(reverse('leads:list'))
    return render(request, 'leads/editLead.html', {'form': form})


@login_required
def addlead(request):
    form = AddLeadForm()
    team = Team.objects.filter(created_by=request.user)[0]
    if request.method == 'POST':
        form = AddLeadForm(request.POST)
        if form.is_valid():
            leaddetail = form.save(commit=False)
            """Lead.objects.create(name= leaddetails.name, email = leaddetails.email, description = leaddetails.description,
                                priority = leaddetails.priority, status = leaddetails.status, created_by = request.user)"""
            leaddetail.created_by = request.user
            leaddetail.team =team
            leaddetail.save()
            messages.success(request, "Lead created successfully")
            return redirect(reverse('leads:list'))
    return render(request, 'leads/add_lead.html', {'form': form, 'team': team})

@login_required
def converToClient(request, pk):
    lead = get_object_or_404(Lead,created_by = request.user, pk=pk)
    team = Team.objects.filter(created_by=request.user)[0]
    Client = client.objects.create(
        name = lead.name,
        email = lead.email,
        description = lead.description,
        created_by = request.user,
        team=team
    )
    lead.converted_to_client = True
    lead.save()
    messages.success(request, "Lead converted to client successfully")
    return redirect(reverse('leadlist'))

@login_required
def leadsExport(request):
    leads= Lead.objects.filter(created_by=request.user)
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="leads.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow(['Lead Name', 'Description', 'Created By', 'Created At'])
    for lead in leads:
        writer.writerow([lead.name, lead.description, lead.created_by, lead.created_at])
    return response