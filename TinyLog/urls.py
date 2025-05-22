from django.urls import path
from . import views
from .views import Generate_Immunization_PDF, Generate_Medical_PDF

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),  # No pk required
    # path('dashboard/<int:pk>/', views.dashboard_with_pk, name='dashboard_with_pk'),  # With pk
    path('add_patient/', views.add_patient, name='add_patient'),
    path('edit-patient/<int:pk>/', views.edit_patient, name='edit_patient'),
    path('patient_data_record/', views.patient_data_record, name='patient_data_record'),
    path('immunization_record/<int:pk>/', views.immunization_record, name='immunization_record'),
    path('immunization-data/<int:pk>/', views.immunization_data, name='immunization_data'),
    path('submission-success/', views.submission_success, name='submission_success'),
    path('search-patient/', views.search_patient, name='search_patient'),
    path('medical-record/<int:pk>/', views.medical_record, name='medical_record'),
    path('medical-data/<int:pk>/', views.medical_data, name='medical_data'),
    path('view-data/', views.view_data, name='view_data'),
    path('view-medical-data/<int:pk>/', views.view_medical_data, name='view_medical_data'),
    path('view-immunization-data/<int:pk>/', views.view_immunization_data, name='view_immunization_data'),
    path('logout/', views.logout_view, name='logout'),
    path('pdf/Immunization/<int:patient_id>/', Generate_Immunization_PDF.as_view(), name='patient_pdf'),
    path('pdf/Medical/<int:patient_id>/', Generate_Medical_PDF.as_view(), name='medical_pdf'),
    path('pdf1/', views.pdf1_view, name='pdf1_view'),
    path('pdf2/', views.pdf2_view, name='pdf2_view'),
]