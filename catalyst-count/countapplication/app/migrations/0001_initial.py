# Generated by Django 5.1.3 on 2024-11-13 19:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded_file', models.FileField(upload_to='company_files/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('company_id', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('domain', models.CharField(blank=True, max_length=255, null=True)),
                ('year_founded', models.IntegerField(blank=True, null=True)),
                ('industry', models.CharField(blank=True, max_length=255, null=True)),
                ('size_range', models.CharField(blank=True, max_length=50, null=True)),
                ('locality', models.CharField(blank=True, max_length=255, null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('linkedin_url', models.CharField(blank=True, max_length=255, null=True)),
                ('current_employee_estimate', models.IntegerField(blank=True, null=True)),
                ('total_employee_estimate', models.IntegerField(blank=True, null=True)),
                ('f_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='app.companyfile')),
            ],
        ),
    ]