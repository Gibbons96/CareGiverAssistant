from django import forms
from .models import EmployeeApplication

class EmployeeApplication_Form(forms.ModelForm):
    class Meta:
        model = EmployeeApplication
        fields = '__all__'
        widgets = {
            'title': forms.Select(attrs={'class': 'form-control'}),
            'forenames': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'eircode': forms.TextInput(attrs={'class': 'form-control'}),
            'pps_number': forms.TextInput(attrs={'class': 'form-control'}),
            'occupation': forms.TextInput(attrs={'class': 'form-control'}),
            'language': forms.TextInput(attrs={'class': 'form-control'}),
            'eu_passport_or_gnib': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'emergency_name': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_relationship': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'iban': forms.TextInput(attrs={'class': 'form-control'}),
            'bic': forms.TextInput(attrs={'class': 'form-control'}),
            # Boolean fields as checkboxes
            'student_nurse_id': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'nmbi_cert': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'fetac_level_5': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'social_care_cert': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'cpr_cert': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'patient_moving': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'elder_abuse': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'ppe_training': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'infection_control': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'safeguarding_adults': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hand_hygiene': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'fire_safety': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'children_first': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'gdpr': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hep_b': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'mmr_immunity': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'varicella_immunity': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
