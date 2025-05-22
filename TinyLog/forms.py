from django import forms
from .models import Patient, ImmunizationRecord, MedicalHospitalizationRecord
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'name', 'religion', 'place_of_birth', 'pediatrician',
            'date_of_birth', 'sex', 'birth_weight', 'mother_maiden_name',
            'birth_height', 'father_name', 'address'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'autocomplete': 'name',
                'placeholder': 'Enter the patient\'s full name',
                'style': 'width: 90%; padding: 10px; font-size: 25px; border-radius: 10px; border: none; background-color: #d1d0d0;'
            }),
            'address': forms.TextInput(attrs={
                'autocomplete': 'street-address',
                'placeholder': 'Enter the patient\'s address',
                'style': 'width: 90%; padding: 10px; font-size: 25px; border-radius: 10px; border: none; background-color: #d1d0d0;'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date',
                'autocomplete': 'bday',
                'placeholder': 'MM/DD/YYYY',
                'style': 'width: 90%; padding: 10px; font-size: 25px; border-radius: 10px; border: none; background-color: #d1d0d0;'
            }),
            'sex': forms.Select(attrs={
                'autocomplete': 'sex',
                'style': 'width: 90%; padding: 10px; font-size: 25px; border-radius: 10px; border: none; background-color: #d1d0d0;'
            }),
            'religion': forms.TextInput(attrs={
                'autocomplete': 'off',
                'placeholder': 'Enter the patient\'s religion',
                'style': 'width: 90%; padding: 10px; font-size: 25px; border-radius: 10px; border: none; background-color: #d1d0d0;'
            }),
            'place_of_birth': forms.TextInput(attrs={
                'autocomplete': 'off',
                'placeholder': 'Enter the place of birth',
                'style': 'width: 90%; padding: 10px; font-size: 25px; border-radius: 10px; border: none; background-color: #d1d0d0;'
            }),
            'pediatrician': forms.TextInput(attrs={
                'autocomplete': 'off',
                'placeholder': 'Enter the pediatrician\'s name',
                'style': 'width: 90%; padding: 10px; font-size: 25px; border-radius: 10px; border: none; background-color: #d1d0d0;'
            }),
            'birth_weight': forms.NumberInput(attrs={
                'autocomplete': 'off',
                'placeholder': 'Enter the birth weight (g)',
                'style': 'width: 90%; padding: 10px; font-size: 25px; border-radius: 10px; border: none; background-color: #d1d0d0;'
            }),
            'mother_maiden_name': forms.TextInput(attrs={
                'autocomplete': 'name',
                'placeholder': 'Enter the mother\'s maiden name',
                'style': 'width: 90%; padding: 10px; font-size: 25px; border-radius: 10px; border: none; background-color: #d1d0d0;'
            }),
            'birth_height': forms.NumberInput(attrs={
                'autocomplete': 'off',
                'placeholder': 'Enter the birth height (cm)',
                'style': 'width: 90%; padding: 10px; font-size: 25px; border-radius: 10px; border: none; background-color: #d1d0d0;'
            }),
            'father_name': forms.TextInput(attrs={
                'autocomplete': 'name',
                'placeholder': 'Enter the father\'s name',
                'style': 'width: 90%; padding: 10px; font-size: 25px; border-radius: 10px; border: none; background-color: #d1d0d0;'
            }),
        }

class ImmunizationRecordForm(forms.ModelForm):
    class Meta:
        model = ImmunizationRecord
        fields = ['vaccine', 'dose', 'vaccine_batch_number', 'date_of_administration', 'facility_name', 'administering_provider', 'remarks']

        widgets = {
            'date_of_administration': forms.DateInput(attrs={
                'type': 'date',
                'autocomplete': 'date_of_administration',
                'placeholder': 'MM/DD/YYYY',
                'style': 'width: 90%; padding: 10px; font-size: 25px; border-radius: 10px; border: none; background-color: #d1d0d0;'
            }),
        }

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.CharField(max_length=100, required=False, initial="Healthcare Provider")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create a UserProfile instance for the new user
            UserProfile.objects.create(user=user, role=self.cleaned_data.get('role'))
        return user
    
class MedicalHospitalizationRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalHospitalizationRecord
        fields = [
            'type', 'name_of_facility', 'date_of_visit',
            'name_of_physician', 'chief_complaint', 'nurses_notes', 'medical_impression'
        ]
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'nurses_notes': forms.Textarea(attrs={'autocomplete': 'medical_impression',
                'style': 'height: 90%; margin: 0px 60px; font-size: 25px; border-radius: 20px; border: none; background-color: #d1d0d0;'}),
            'date_of_visit': forms.DateInput(attrs={
                'type': 'date',
                'autocomplete': 'date_of_visit',
                'placeholder': 'MM/DD/YYYY',
                'style': 'width: 90%; padding: 10px; font-size: 25px; border-radius: 10px; border: none; background-color: #d1d0d0;'
            }),
            'medical_impression': forms.Textarea(attrs={
                'autocomplete': 'medical_impression',
                'style': 'height: 85%; margin: 25px 10px 0px 0px; font-size: 25px; border-radius: 10px; border: none; background-color: #d1d0d0;'
            }),
        }