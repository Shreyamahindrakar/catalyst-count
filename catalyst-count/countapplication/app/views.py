# app/views.py

from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.generics import CreateAPIView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db import transaction
from rest_framework.response import Response
import csv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.models import Company
from app.serializers import CompanyFileSerializer, CompanySerializer
from app.utils import CookieJWTAuthentication, generate_token
from .forms import EmailLoginForm,RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from rest_framework.parsers import MultiPartParser, FormParser

from .forms import RegisterForm


def email_login(request):
    if request.method == 'POST':
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)

                if user is not None:
                    # Generate JWT token for the logged-in user
                    token = generate_token({"email": user.email})

                    # Log the user in and set the token as an HTTP-only cookie
                    login(request, user)
                    response = redirect('dashboard')  # Redirect to the dashboard view
                    response.set_cookie('jwt_token', token, httponly=True, secure=True)  # Use `secure=True` in production
                    return response
                else:
                    messages.error(request, "Invalid email or password.")
                    return redirect('login')  # Redirect back to login page

            except User.DoesNotExist:
                messages.error(request, "Email not found.")
                return redirect('login')  # Redirect back to login page
    else:
        form = EmailLoginForm()

    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            
            # Generate JWT token for the user if it does not exist in session
            if 'jwt_token' not in request.session:
                token = generate_token({"email": user.email})
                request.session['jwt_token'] = token  # Store token in session

            # Redirect to the login page or dashboard after successful registration
            messages.success(request, "Registration successful. Please log in.")
            return HttpResponseRedirect(reverse('email_login'))

        else:
            # If form is invalid, you can set error messages
            messages.error(request, "Registration failed. Please check the form for errors.")
            return render(request, 'register.html', {'form': form})

    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

class CompanyUploadView1(CreateAPIView):
    serializer_class = CompanyFileSerializer
    permission_classes = [CookieJWTAuthentication]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get('file')
       

        if not uploaded_file:
            return Response({
                "message": "No file provided",
                "status": 400
            })

        if not self.is_valid_csv(uploaded_file):
            return Response({
                'message': 'Input file should be CSV',
                'status': 422
            })

        company_file_serializer = self.create_company_file_serializer(uploaded_file, request.user.pk)
        
        print(company_file_serializer)
        if not company_file_serializer:
            return Response({
                "message": "Unable to upload file",
                "status": 422
            })

        try:
            with transaction.atomic():
                csv_file_data = self.extract_csv_data(company_file_serializer)
                print(csv_file_data)
                if not csv_file_data:
                    return self.handle_transaction_failure("Error extracting CSV data")

                errors = self.process_and_generate_errors(csv_file_data)
                if errors:
                    transaction.set_rollback(True)
                    return Response({
                        "message": "Errors occurred during validation.",
                        "error": errors,
                        "status": 422
                    })
                self.save_companies(csv_file_data)
                company_file_serializer.instance.save()
                return Response({
                    "message": "File added successfully",
                    "data": company_file_serializer.data,
                    "status": 201
                })

        except Exception as e:
            return self.handle_transaction_failure(str(e))

    def is_valid_csv(self, uploaded_file):
        return uploaded_file.name.split('.')[-1].lower() == 'csv'

    def create_company_file_serializer(self, uploaded_file, user_id):
        upload_file = {
            "uploaded_file": uploaded_file, 
            "company": user_id  
        }
        company_file_serializer = self.serializer_class(data=upload_file)
        
        if company_file_serializer.is_valid():
            company_file_serializer.save()
            return company_file_serializer
        print(company_file_serializer.errors)
        return None


    def extract_csv_data(self, company_file_serializer):
        csv_file_data = self.csv_file_extract(company_file_serializer)
        if csv_file_data[0] == "error":
            print(csv_file_data[1])
            return None
        return csv_file_data

    def process_and_generate_errors(self, csv_file_data):
        company_data = csv_file_data[0]
        errors = []
        for idx, row in enumerate(company_data):
            row_errors = {}

            # Check for missing or malformed fields as needed
            if not row.get("name"):
                row_errors["name"] = "Name is required."
            if not row.get('domain'):
                row_errors["domain"] = "domain is required."

            if not row.get('year_founded'):
                row_errors["year_founded"] = "year_founded is required."

            if not row.get('size_range'):
                 row_errors["size_range"] = "size_range is required."

            if not row.get("industry"):
                row_errors["industry"] = "Industry is required."

            if not row.get("linkedin_url"):
                row_errors["linkedin_url"] = "linkedin_url is required."

            if not row.get("current_employee_estimate"):
                row_errors["current_employee_estimate"] = "current_employee_estimate is required."

            if not row.get("country"):
                row_errors["country"] = "Country is required."

            if not row.get("total_employee_estimate"):
                row_errors["total_employee_estimate"] = "total_employee_estimate is required."

            if row_errors:
                errors.append({
                    "row": idx + 1,
                    "errors": row_errors
                })

        # Generate error CSV if there are errors
        if errors:
            
            return errors

        # Return empty errors if all data is valid
        return errors
    
    def save_companies(self, csv_file_data):
        # Loop over the CSV data and create Company instances
        company_data = csv_file_data[0]
        for data in company_data:
            company_serializer = CompanySerializer(data=data)
            if company_serializer.is_valid():
                company_serializer.save()  # Save Company instance to the database
            else:
                print(company_serializer.errors)

    def handle_transaction_failure(self, error_message):
        return Response({
            "message": "File upload failed",
            "error": error_message,
            "status": 400
        })

    def csv_file_extract(self, company_file_instance):
        try:
            file_path = company_file_instance.instance.uploaded_file
            decoded_file = file_path.read().decode('utf-8').splitlines()
            csv_reader = csv.DictReader(decoded_file)

            company_data = []

            # Helper functions
            def format_year(date_str):
                if date_str and date_str.isdigit():
                    return int(date_str)
                return None  # Return None if not a valid year

            def to_lower(val):
                return val.lower() if val else val

            def get_common_fields(row):
                return {
                    "company_id": row.get('company_id'),
                    "f_company": company_file_instance.instance.id,
                    "name": to_lower(row.get("name")),
                    "domain": to_lower(row.get("domain")),
                    "year_founded": format_year(row.get("year_founded")),
                    "industry": row.get("industry"),
                    "size_range": row.get("size_range"),
                    "locality": row.get("locality"),
                    "country": to_lower(row.get("country")),
                    "linkedin_url": row.get("linkedin_url"),
                    "current_employee_estimate": row.get("current_employee_estimate"),
                    "total_employee_estimate": row.get("total_employee_estimate")
                }

            for row in csv_reader:
                company_data.append(get_common_fields(row))

            return [company_data]
        except Exception as e:
            return ["error", {1: str(e)}]

class CompanySearchView(APIView):
    permission_classes = [CookieJWTAuthentication]
    def get(self, request):
        # Get query parameters from the request
        name = request.GET.get('name', None)
        domain = request.GET.get('domain', None)
        industry = request.GET.get('industry', None)
        year_founded = request.GET.get('year_founded', None)
        city = request.GET.get('city', None)
        state = request.GET.get('state', None)
        country = request.GET.get('country', None)

        # Filter the Company model based on the query parameters
        queryset = Company.objects.all()

        if name:
            queryset = queryset.filter(name__icontains=name)
        if domain:
            queryset = queryset.filter(domain__icontains=domain)
        if industry:
            queryset = queryset.filter(industry__icontains=industry)
        if year_founded:
            queryset = queryset.filter(year_founded=year_founded)
        if city:
            queryset = queryset.filter(locality__icontains=city)
        if state:
            queryset = queryset.filter(locality__icontains=state)
        if country:
            queryset = queryset.filter(country__icontains=country)

        # Serialize the data
        serializer = CompanySerializer(queryset, many=True)
        
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

@login_required  
def query_builder(request):
    return render(request, 'querybuilder.html')



class RegisteredUsersView(APIView):
    permission_classes = [CookieJWTAuthentication]
    def get(self, request):
        # Get all registered users
        users = User.objects.all() 
        
        username = request.GET.get('username', None)
        email = request.GET.get('email', None)
        
        if username:
            users = users.filter(username__icontains=username)
        if email:
            users = users.filter(email__icontains=email)

        user_data = [{"id": user.id, "username": user.username, "email": user.email} for user in users]
        
        return Response({
            "status": "success",
            "data": user_data
        }, status=status.HTTP_200_OK)

@login_required  
def register_user(request):
    return render(request, 'registeruser.html')


class DeleteUserView(APIView):
    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return Response({"status": "success", "message": "User deleted successfully"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"status": "error", "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
