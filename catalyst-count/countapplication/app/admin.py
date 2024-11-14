from django.contrib import admin

from app.models import Company, CompanyFile

# Register your models here.
admin.site.register(CompanyFile)
admin.site.register(Company)