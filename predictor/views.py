from .models import LoanPrediction
from django.shortcuts import render, redirect
from .forms import LoanForm
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from django.http import HttpResponse
from django.utils.timezone import is_aware
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.db.models.functions import TruncMonth, TruncYear
from django.db.models import Count
import calendar
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date
from django.contrib.auth import login, authenticate

class CustomSignupView(CreateView):
    form_class = UserCreationForm
    template_name = 'signupforuser.html'
    success_url = reverse_lazy('loan_form')

    def form_valid(self, form):
        self.object = form.save()  # ✅ Set self.object!
        raw_password = form.cleaned_data.get("password1")
        user = authenticate(username=self.object.username, password=raw_password)

        if user is not None:
            login(self.request, user)
            print("✅ Login successful.")
        else:
            print("❌ Login failed. Authentication returned None.")

        return redirect(self.get_success_url())

    def form_invalid(self, form):
        print("❌ Form invalid:", form.errors)
        return super().form_invalid(form)
    
class CustomLoginView(LoginView):
    template_name = 'login_user.html'

class CustomLogoutView(LogoutView):
    pass

def loan_entry_page(request):
    return render(request, 'landingpage.html')

@login_required
def view_records(request):
    records = LoanPrediction.objects.all().order_by('-id')
     # Filter by date range
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date:
        records = records.filter(timestamp__date__gte=parse_date(start_date))
    if end_date:
        records = records.filter(timestamp__date__lte=parse_date(end_date))

    return render(request, 'predictor/records.html', {'records': records})

@require_POST
@login_required
def delete_record(request, record_id):
    record = get_object_or_404(LoanPrediction, id=record_id)
    record.delete()
    return redirect('view_records')

@require_POST
@login_required
def approve_record(request, record_id):
    record = get_object_or_404(LoanPrediction, id=record_id)
    record.prediction_result = 'Approved'
    record.is_admin_approved = True  # <-- Mark as approved
    record.save()

    messages.success(request, f"Loan record for {record.name} has been approved.")
    return redirect('view_records')

@require_POST
@login_required
def disapprove_record(request, record_id):
    record = get_object_or_404(LoanPrediction, id=record_id)
    record.prediction_result = 'Rejected'
    record.is_admin_approved = True  # <-- Also mark as reviewed
    record.save()

    messages.success(request, f"Loan record for {record.name} has been disapproved.")
    return redirect('view_records')

# This view is for displaying the status of the user's loan applications
@login_required
def status_view(request):
    # Show only the loan records created by this logged-in user
    user_records = LoanPrediction.objects.filter(name=request.user.username).order_by('-id')
    return render(request, 'status.html', {'user_records': user_records})


@login_required
def reports_view(request):
    return render(request, 'reports.html')

model = joblib.load('loan_model.pkl')

@login_required
@csrf_exempt
def loan_application(request):
    if request.method == 'POST':
        form = LoanForm(request.POST, request.FILES)  # <-- handle files
        if form.is_valid():
            data = pd.DataFrame([form.cleaned_data])
            data = pd.get_dummies(data)

            expected_columns = model.get_booster().feature_names
            for col in expected_columns:
                if col not in data:
                    data[col] = 0
            data = data[expected_columns]

            prediction = model.predict(data)[0]
            result = 'Approved' if prediction == 1 else 'Rejected'

            # Save to DB
            LoanPrediction.objects.create(
                name=request.user.username,
                gender=form.cleaned_data['Gender'],
                dependents=form.cleaned_data['Dependents'],
                married=form.cleaned_data['Married'],
                education=form.cleaned_data['Education'],
                applicant_income=form.cleaned_data['ApplicantIncome'],
                coapplicant_income=form.cleaned_data['CoapplicantIncome'],
                loan_amount=form.cleaned_data['LoanAmount'],
                loan_amount_term=form.cleaned_data['Loan_Amount_Term'],
                credit_history=form.cleaned_data['Credit_History'],
                self_employed=form.cleaned_data['Self_Employed'],
                property_area=form.cleaned_data['Property_Area'],
                loan_type=form.cleaned_data['Loan_Type'],
                id_type=form.cleaned_data.get('id_type'),
                id_upload=request.FILES.get('id_upload'),
                prediction_result=result,
            )

            return render(request, 'predictor/result.html', {'result': result})
    else:
        form = LoanForm()
        loan_amount = request.GET.get('loanAmount')
        loan_term = request.GET.get('loanTerm')
        return render(request, 'predictor/form.html', {
            'form': form,
            'loan_amount': loan_amount,
            'loan_term': loan_term
        })

def reports(request):
    df = pd.read_csv('Loans_datasets.csv')

    # Loan Status Count
    status_counts = df['Loan_Status'].value_counts()
    status_data = {
        'labels': status_counts.index.tolist(),
        'values': status_counts.values.tolist()
    }

    # Loan Status by Property Area
    prop_area = df[df['Loan_Status'] == 'Y']['Property_Area'].value_counts()
    property_data = {
        'labels': prop_area.index.tolist(),
        'values': prop_area.values.tolist()
    }

    # Income vs Loan Amount
    scatter_data = df[['ApplicantIncome', 'LoanAmount']].dropna()
    income_loan_data = [
        {'x': row['ApplicantIncome'], 'y': row['LoanAmount']}
        for _, row in scatter_data.iterrows()
    ]

    context = {
        'status_data': json.dumps(status_data),
        'property_data': json.dumps(property_data),
        'income_loan_data': json.dumps(income_loan_data),
    }

    return render(request, 'predictor/reports.html', context)

def download_excel(request):
    data = LoanPrediction.objects.all()
    df = pd.DataFrame(list(data.values()))

    # Convert any timezone-aware datetimes to naive
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].apply(lambda x: x.replace(tzinfo=None) if is_aware(x) else x)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=loan_predictions.xlsx'
    df.to_excel(response, index=False)
    return response

def loan_form(request):
    return render(request, 'predictor/form.html')


# toggle section
def download_gender_report(request):
    data = {
        'Gender': ['Male', 'Female'],
        'Count': [120, 100],  # Replace with actual dynamic data
    }
    df = pd.DataFrame(data)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=gender_report.csv'
    df.to_csv(response, index=False)
    return response

def dashboard(request):
    df = pd.read_csv('Loans_datasets.csv')

    total_loans = len(df)
    total_predicted = df['Loan_Status'].count()

    approval_count = df[df['Loan_Status'] == 'Y'].shape[0]
    rejection_count = df[df['Loan_Status'] == 'N'].shape[0]

    approval_rate = (approval_count / total_predicted) * 100 if total_predicted else 0
    rejection_rate = (rejection_count / total_predicted) * 100 if total_predicted else 0

    total_applications = LoanPrediction.objects.count()

    gender_counts = df['Gender'].value_counts()
    gender_display = ', '.join([f"{gender}: {count}" for gender, count in gender_counts.items()])
    gender_data = {
        'labels': gender_counts.index.tolist(),
        'values': gender_counts.values.tolist()
    }

    education_counts = df['Education'].value_counts()
    education_data = {
        'labels': education_counts.index.tolist(),
        'values': education_counts.values.tolist()
    }

    # Ensure 'Date' column exists and is in datetime format
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')  # Handles invalid formats
        df = df.dropna(subset=['Date'])

        # Monthly trend
        df['Month'] = df['Date'].dt.month
        monthly_group = df.groupby('Month').size()
        monthly_labels = [calendar.month_abbr[m] for m in monthly_group.index]
        monthly_values = monthly_group.values.tolist()

        monthly_data = {
            'labels': monthly_labels,
            'values': monthly_values
        }

        # Yearly trend
        df['Year'] = df['Date'].dt.year
        yearly_group = df.groupby('Year').size()
        yearly_data = {
            'labels': yearly_group.index.tolist(),
            'values': yearly_group.values.tolist()
        }
    else:
        # If 'Date' is not present, return placeholders
        monthly_data = {'labels': [], 'values': []}
        yearly_data = {'labels': [], 'values': []}

    context = {
        'total_loans': total_loans,
        'total_predicted': total_predicted,
        'approval_rate': round(approval_rate, 2),
        'rejection_rate': round(rejection_rate, 2),
        'gender_display': gender_display,
        'gender_data': json.dumps(gender_data),
        'education_data': json.dumps(education_data),
        'monthly_data': json.dumps(monthly_data),
        'yearly_data': json.dumps(yearly_data),
        'total_applications': total_applications,
    }

    return render(request, 'predictor/dashboard.html', context)

def my_loan_status(request):
    return HttpResponse("Loan status")


