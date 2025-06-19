from django.db import models
from django.utils import timezone

class LoanPrediction(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    dependents = models.CharField(max_length=10)
    married = models.CharField(max_length=10)
    education = models.CharField(max_length=20)
    applicant_income = models.FloatField()
    coapplicant_income = models.FloatField()
    loan_amount = models.FloatField()
    loan_amount_term = models.FloatField()
    credit_history = models.FloatField()
    self_employed = models.CharField(max_length=10)
    property_area = models.CharField(max_length=20)
    prediction_result = models.CharField(max_length=20)
    loan_type = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    is_admin_approved = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)
    id_type = models.CharField(max_length=100, blank=True, null=True)
    id_upload = models.FileField(upload_to='uploaded_ids/', blank=True, null=True)
