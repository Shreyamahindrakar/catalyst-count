from django.db import models


class CompanyFile(models.Model):
    
    uploaded_file = models.FileField(upload_to="company_files/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.uploaded_file.name}"
    
class Company(models.Model):
    id = models.AutoField(primary_key=True)
    f_company = models.ForeignKey(CompanyFile, on_delete=models.CASCADE, related_name="files")
    company_id = models.IntegerField(blank=True,null=True)
    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255, null=True, blank=True)
    year_founded = models.IntegerField(null=True, blank=True)
    industry = models.CharField(max_length=255, null=True, blank=True)
    size_range = models.CharField(max_length=50, null=True, blank=True)
    locality = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    linkedin_url = models.CharField(max_length=255,null=True, blank=True)
    current_employee_estimate = models.IntegerField(null=True, blank=True)
    total_employee_estimate = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name
