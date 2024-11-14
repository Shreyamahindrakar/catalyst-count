from rest_framework import serializers
import datetime
import os

from app.models import Company, CompanyFile

class CompanyFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyFile
        fields = "__all__"

    def create(self, validated_data):
        # Prepend a timestamp to the uploaded file name
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        validated_data['uploaded_file'].name = f"{timestamp}_{validated_data['uploaded_file'].name}"
        return super().create(validated_data)

    def to_representation(self, instance):
        # Customize the representation for the file name and created_at fields
        representation = super().to_representation(instance)
        representation['uploaded_file'] = os.path.basename(instance.uploaded_file.name)
        representation['created_at'] = instance.created_at.strftime('%Y-%m-%d %H:%M:%S')
        return representation

class CompanySerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Company
        fields = ['company_id', 'name', 'domain', 'year_founded', 'industry', 'size_range', 'locality', 'country', 'linkedin_url', 'current_employee_estimate', 'total_employee_estimate', 'f_company']
