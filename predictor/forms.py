from django import forms
from django.core.exceptions import ValidationError



ID_TYPE_CHOICES = [
    ('', 'Select ID Type'),
    ('passport', 'Passport'),
    ('driver_license', "Driver's License"),
    ('national_id', 'National ID'),
]

class LoanForm(forms.Form):
    GENDER_CHOICES = [('2', 'Please Choose'), ('0', 'Male'), ('1', 'Female')]
    DEPENDENTS_CHOICES = [('0', 'No'), ('1', 'Yes')]
    MARRIED_CHOICES = [('1', 'Married'), ('0', 'Single')]
    EDUCATION_CHOICES = [('0', 'Graduate'), ('1', 'Not Graduate')]
    SELF_EMPLOYED_CHOICES = [('0', 'No'), ('1', 'Yes')]
    PROPERTY_AREA_CHOICES = [('2', 'Urban'), ('1', 'Semiurban'), ('0', 'Rural')]

    Name = forms.CharField(
        label="Full Name",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your full name'
        })
    )

    Gender = forms.ChoiceField(label="Gender", choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    Dependents = forms.ChoiceField(label="Dependents", choices=DEPENDENTS_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    Married = forms.ChoiceField(label="Marital Status", choices=MARRIED_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    Education = forms.ChoiceField(label="Education", choices=EDUCATION_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    
    ApplicantIncome = forms.FloatField(
        label="Applicant Income",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter applicant income'
        })
    )
    CoapplicantIncome = forms.FloatField(
        label="Coapplicant Income",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter co-applicant income'
        })
    )
    LoanAmount = forms.FloatField(
        label="Loan Amount",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter loan amount'
        })
    )
    Loan_Amount_Term = forms.FloatField(
        label="Loan Amount Term",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter loan term in days'
        })
    )
    
    Credit_History = forms.FloatField(
        label="Credit History",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter credit history (e.g., 1.0 or 0.0)'
        })
    )

    LOAN_TYPE_CHOICES = [
        ('', 'Select Loan Type'),
        ('home', 'Home Loan'),
        ('personal', 'Personal Loan'),
        ('education', 'Education Loan'),
        ('car', 'Car Loan'),
    ]

    Loan_Type = forms.ChoiceField(
        label="Loan Type",
        choices=LOAN_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    Self_Employed = forms.ChoiceField(label="Self Employed", choices=SELF_EMPLOYED_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    Property_Area = forms.ChoiceField(label="Property Area", choices=PROPERTY_AREA_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))





    id_type = forms.ChoiceField(
            choices=ID_TYPE_CHOICES,
            label='Government ID Type',
            required=False,
            widget=forms.Select(attrs={'class': 'form-select'})
        )

    id_upload = forms.FileField(
            label='Upload ID',
            required=False,
            widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
        )