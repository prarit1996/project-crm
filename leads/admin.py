from django.contrib import admin
from .models import Lead, Comments, LeadFiles

# Register your models here.
admin.site.register(Lead)
admin.site.register(Comments)
admin.site.register(LeadFiles)