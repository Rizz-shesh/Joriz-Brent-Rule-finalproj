from django.shortcuts import render, redirect, get_object_or_404
from wkhtmltopdf.views import PDFTemplateResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from TinyLog.models import Patient
from .models import User,UserProfile, ImmunizationRecord, MedicalHospitalizationRecord
from .forms import PatientForm, ImmunizationRecordForm, SignUpForm, MedicalHospitalizationRecordForm
from django.http import HttpResponse, Http404
from django.template.loader import render_to_string
from django.views import View
from wkhtmltopdf.views import PDFTemplateResponse
import pdfkit

def home(request):
    return render(request, 'home.html')

def pdf1_view(request):
    return render(request, 'pdf_immunization_data.html')

def pdf2_view(request):
    return render(request, 'pdf_medical_data.html')

def view_medical_data(request,pk):
    # Fetch the patient by primary key (pk)
    patient = get_object_or_404(Patient, pk=pk)
    # Fetch the latest medical record for the patient
    try:
        medical_record = MedicalHospitalizationRecord.objects.filter(patient=patient).latest('date_of_visit')
    except MedicalHospitalizationRecord.DoesNotExist:
        medical_record = None

    return render(request, 'view_medical_data.html', {
        'patient': patient,
        'medical_record': medical_record,
    })

def view_immunization_data(request,pk):
    # Fetch the patient by primary key (pk)
    patient = get_object_or_404(Patient, pk=pk)
    # Fetch the latest medical record for the patient
    immunization_record = ImmunizationRecord.objects.filter(patient=patient)

    return render(request, 'view_immunization_data.html', {
        'patient': patient,
        'immunization_record': immunization_record,
    })

def view_data(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        birthdate = request.POST.get('birthdate')
        try:
            # Search for the patient by name and birthdate
            patient = Patient.objects.get(name=name, date_of_birth=birthdate)
            # Redirect to the view_immunization_data view with the patient's pk
            return redirect('view_immunization_data', pk=patient.id)
        except Patient.DoesNotExist:
            # Display an error message if the patient is not found
            messages.error(request, "Patient not found. Please check the name and birthdate.")
    else:
        # Fetch all patients to display in the view
        patients = Patient.objects.all()
    return render(request, 'view_data.html', {'patients': patients})


@login_required
def search_patient(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        birthdate = request.POST.get('birthdate')

        try:
            # Search for the patient by name and birthdate
            patient = Patient.objects.get(name=name, date_of_birth=birthdate)
            # Redirect to the edit_patient view with the patient's pk
            return redirect('edit_patient', pk=patient.id)
        except Patient.DoesNotExist:
            # Display an error message if the patient is not found
            messages.error(request, "Patient not found. Please check the name and birthdate.")
    
    return render(request, 'search_patient.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Log the user in
            login(request, user)
            
            # Fetch the associated UserProfile and store its ID in the session
            try:
                provider = UserProfile.objects.get(user=user)
                request.session['provider_id'] = provider.id
                print("Provider ID stored in session:", provider.id)  # Debugging statement
                return redirect('dashboard')  # Redirect to the dashboard
            except UserProfile.DoesNotExist:
                messages.error(request, "User profile not found")
                return redirect('login')
        else:
            # Display an error message
            messages.error(request, "Invalid credentials")
    
    return render(request, 'login.html')

def logout_view(request):
    if request.method == 'POST' or request.method == 'GET':
        logout(request)  # Log the user out
        return redirect('home')  # Redirect to the login page
    return redirect('dashboard')  # Fallback redirection

@login_required
def dashboard(request):
    provider_id = request.session.get('provider_id')
    if not provider_id:
        print("User invalid")
        return redirect('login')
    provider = UserProfile.objects.get(id=provider_id)
    print("User valid")
    return render(request, 'dashboard.html', {'provider': provider})

@login_required
def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        print("Form submitted")  # Debugging statement
        if form.is_valid():
            print("Form is valid")  # Debugging statement
            patient = form.save()
            print(f"Patient saved with ID: {patient.pk}")  # Debugging statement
            return redirect('immunization_record', pk=patient.pk)
        else:
            print("Form is invalid")  # Debugging statement
            print(form.errors)  # Print form errors for debugging
            messages.error(request, "Invalid form data. Please check your input.")
    else:
        form = PatientForm()

    return render(request, 'add_patient.html', {'form': form})

@login_required
def patient_data_record(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            return redirect('immunization_record', pk=patient.pk)
    else:
        form = PatientForm()
    return render(request, 'immunization_record.html', {'form': form})

@login_required
def immunization_record(request, pk):
    # Fetch the patient by primary key (pk)
    patient = get_object_or_404(Patient, pk=pk)
    # Fetch all immunization records for the patient
    immunization_records = ImmunizationRecord.objects.filter(patient=patient)

    if request.method == 'POST':
        # Handle new immunization record submission
        form = ImmunizationRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.patient = patient
            record.save()
            return redirect('immunization_data', pk=patient.pk)  # Redirect with pk
    else:
        # Display an empty form for adding a new record
        form = ImmunizationRecordForm()

    return render(request, 'immunization_record.html', {
        'form': form,
        'patient': patient,
        'immunization_records': immunization_records,
    })

@login_required
def edit_patient(request, pk):
    # Fetch the patient by primary key (pk)
    patient = get_object_or_404(Patient, pk=pk)

    if request.method == 'POST':
        # Populate the form with the submitted data and the patient instance
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            # Redirect to the immunization_data view with the patient's pk
            return redirect('immunization_data', pk=patient.id)
    else:
        # Populate the form with the patient's existing data
        form = PatientForm(instance=patient)
    
    return render(request, 'edit_patient.html', {'form': form, 'patient': patient})

def immunization_data(request, pk):
    # Fetch the patient by ID
    patient = get_object_or_404(Patient, pk=pk)
    # Fetch all immunization records for the patient
    immunization_datas = ImmunizationRecord.objects.filter(patient=patient)

    if request.method == 'POST':
        # Handle new immunization record submission
        form = ImmunizationRecord(request.POST, patient=patient)
        if form.is_valid():
            record = form.save(commit=False)
            record.patient = patient
            record.save()
            return redirect('immunization_data', pk=patient.id)
    else:
        # Display an empty form for adding a new record
        form = ImmunizationRecord(patient=patient)

    return render(request, 'immunization_data.html', {
        'form': form,
        'patient': patient,
        'immunization_datas': immunization_datas,
    })

def medical_data(request, pk):
    # Fetch the patient by primary key (pk)
    patient = get_object_or_404(Patient, pk=pk)
    # Fetch the latest medical record for the patient
    try:
        medical_record = MedicalHospitalizationRecord.objects.filter(patient=patient).latest('date_of_visit')
    except MedicalHospitalizationRecord.DoesNotExist:
        medical_record = None

    return render(request, 'medical_data.html', {
        'patient': patient,
        'medical_record': medical_record,
    })


@login_required
def medical_record(request, pk):
    patient = get_object_or_404(Patient, id=pk)  # Fetch the patient by ID
    if request.method == 'POST':
        form = MedicalHospitalizationRecordForm(request.POST)
        print("Form submitted")  # Debugging statement
        if form.is_valid():
            print("Form is valid")  # Debugging statement
            record = form.save(commit=False)
            record.patient = patient
            record.save()
            print(f"Medical record saved with ID: {patient.pk}")
            return redirect('submission_success')  # Redirect to dashboard after submission
    else:
        form = MedicalHospitalizationRecordForm()
        print("Form is invalid")  # Debugging statement
        print(form.errors)  # Print form errors for debugging
    return render(request, 'medical_record.html', {'form': form, 'patient': patient})

def submission_success(request):
    return render(request, 'submission_success.html')

class Generate_Immunization_PDF(View):
    def get(self, request, patient_id):
        try:
            # 1. Fetch patient and related immunization records
            patient = Patient.objects.get(id=patient_id)
            immunization_record = ImmunizationRecord.objects.filter(patient=patient)
        except Patient.DoesNotExist:
            raise Http404("Patient record not found")

        html_string = render_to_string('pdf_immunization_data.html', {
            'patient': patient,
            'immunization_record': immunization_record
        })

        # Configure path to wkhtmltopdf executable
        config = pdfkit.configuration(
            wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        )

        # Convert HTML string to PDF binary
        pdf = pdfkit.from_string(html_string, False, configuration=config, options={
            'margin-bottom': '0',  # This removes footer margin
            'quiet': ''            # To suppress CLI output
        })

        # Return the PDF in a downloadable response
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="patient_{patient_id}_immunization_data.pdf"'
        return response
    
class Generate_Medical_PDF(View):
    def get(self, request, patient_id):
        try:
            # 1. Fetch patient and related medical records
            patient = Patient.objects.get(id=patient_id)
            medical_record = MedicalHospitalizationRecord.objects.filter(patient=patient)
        except Patient.DoesNotExist:
            raise Http404("Patient record not found")

        html_string = render_to_string('pdf_medical_data.html', {
            'patient': patient,
            'medical_record': medical_record
        })

        # Configure path to wkhtmltopdf executable
        config = pdfkit.configuration(
            wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        )

        # Convert HTML string to PDF binary
        pdf = pdfkit.from_string(html_string, False, configuration=config, options={
            'margin-bottom': '0',  # This removes footer margin
            'quiet': ''            # To suppress CLI output
        })

        # Return the PDF in a downloadable response
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="patient_{patient_id}_medical_data.pdf"'
        return response