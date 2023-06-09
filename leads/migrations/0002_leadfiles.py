# Generated by Django 4.1.7 on 2023-03-20 18:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teams', '0001_initial'),
        ('leads', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeadFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='leadfiles')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lead_files', to=settings.AUTH_USER_MODEL)),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='leads.lead')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lead_files', to='teams.team')),
            ],
        ),
    ]
