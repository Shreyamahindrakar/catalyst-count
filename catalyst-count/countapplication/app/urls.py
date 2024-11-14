# app/urls.py
from django.urls import path
from django.conf.urls.static import static
from countapplication import settings
from .views import  CompanyUploadView1, DeleteUserView, RegisteredUsersView, dashboard, email_login, query_builder, register,CompanySearchView, register_user

urlpatterns = [
    path('',email_login, name='email_login'),
    path('login/', email_login, name='email_login'),
    path('register/', register, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('file-upload/',CompanyUploadView1.as_view(),name='file-upload'),
    path('data-search/',CompanySearchView.as_view(), name='company-query'),
    path('querybuilder/', query_builder, name='querybuilder'),
    path('registered-users/', RegisteredUsersView.as_view(), name='registered-users'),
    path('register_user/',register_user,name='register_user'),
    path('delete-user/<int:user_id>/', DeleteUserView.as_view(), name='delete-user')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)