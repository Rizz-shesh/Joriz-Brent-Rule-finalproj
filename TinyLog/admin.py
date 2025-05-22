from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Patient, ImmunizationRecord, MedicalHospitalizationRecord

# Inline UserProfile with User in the admin
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profiles'

# Extend the default UserAdmin
class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

# Unregister the default UserAdmin and register the custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Patient)
admin.site.register(ImmunizationRecord)
admin.site.register(MedicalHospitalizationRecord)
admin.site.register(UserProfile)
