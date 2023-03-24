import csv
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView, View
from .forms import AddLeadForm, AddCommentForm, AddFileForm
from .models import Lead, LeadFiles
from django.contrib import messages
from client.models import client, Comments as ClientComment
from teams.models import Team
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from .function_based_views import leadlist, leaddetails, edit_lead, addlead, converToClient, delete_lead, leadsExport
from django.http import HttpResponse
# Create your views here.

class LeadListView(LoginRequiredMixin,ListView):
    model = Lead
    template_name = 'leads/leadlist.html'

    def get_queryset(self):
        queryset = super(LeadListView, self).get_queryset()
        return queryset.filter(created_by = self.request.user, converted_to_client=False)



#class based view for leads details
class LeadDetailView(LoginRequiredMixin,DetailView):
    model = Lead
    template_name = "leads/leaddetails.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddCommentForm()
        context['fileform'] = AddFileForm()
        return context
    def get_queryset(self):
        queryset=super(LeadDetailView, self).get_queryset()
        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))

class LeadDeleteView(LoginRequiredMixin,DeleteView):
    model = Lead

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    def get_success_url(self):
        return reverse('leads:list')
    def delete(self, request, *args, **kwargs):
        super(LeadDeleteView,self).delete(self.request,created_by=self.request.user, pk=self.kwargs.get('pk'))
        messages.success(self.request, "Lead deleted successfully")
        return redirect(self.get_success_url())


class LeadUpdateView(LoginRequiredMixin,UpdateView):
    model = Lead
    fields = ['name','email', 'description', 'priority', 'status']
    template_name = 'leads/editLead.html'
    def get_queryset(self):
        queryset = super(LeadUpdateView, self).get_queryset()
        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))
    def get_success_url(self):
        messages.success(self.request, "Lead details updated successfully")
        return reverse_lazy('leads:list')

class AddFileView(LoginRequiredMixin,View):
    def post(self,request, *args, **kwargs):
        pk = kwargs.get('pk')
        form = AddFileForm(request.POST, request.FILES)
        if form.is_valid():
            team = Team.objects.filter(created_by=self.request.user)[0]
            file = form.save(commit=False)
            file.created_by = request.user
            file.lead_id = pk
            file.team= team
            file.save()
        return redirect('leads:details',pk=pk)



class LeadCreateView(LoginRequiredMixin,CreateView):
    model = Lead
    fields = ['name', 'email', 'description', 'priority', 'status']
    template_name = 'leads/add_lead.html'
    def get_context_data(self, **kwargs):
        team = Team.objects.filter(created_by=self.request.user)[0]
        context = super().get_context_data(**kwargs)
        context['team']=team
        return context
    def get_success_url(self):
        return reverse('leads:list')
    def form_valid(self, form):
        team= Team.objects.filter(created_by=self.request.user)[0]
        self.object= form.save(commit=False)
        self.object.created_by= self.request.user
        self.object.team = team
        self.object.save()
        messages.success(self.request, "Lead created successfully")
        return redirect(self.get_success_url())

class AddCommentView(LoginRequiredMixin,View):
    def post(self,request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        form = AddCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            team = Team.objects.filter(created_by=request.user)[0]
            comment.team = team
            comment.created_by = request.user
            comment.lead_id = pk
            comment.save()
        return redirect('leads:details', pk=pk)


class ConvertToClientView(LoginRequiredMixin, View):
    def get(self,request, *args, **kwargs):
        pk=self.kwargs.get('pk')
        lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
        team = Team.objects.filter(created_by=request.user)[0]
        Client = client.objects.create(
            name=lead.name,
            email=lead.email,
            description=lead.description,
            created_by=request.user,
            team=team
        )


       # convert lead comments to client comments
        for comment in lead.comments.all:
            ClientComment.objects.create(
                content = comment.comtent,
                created_by= comment.created_by,
                team = team,
                client = Client
            )
        lead.converted_to_client = True
        lead.save()
        messages.success(request, "Lead converted to client successfully")
        return redirect('leads:list')


