from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView, CustomSignupView, CustomLogoutView

urlpatterns = [
    path('', views.loan_entry_page, name='loan_entry_page'),  # root URL
    path('loan/', views.loan_application, name='loan_application'),
    path('form/', views.loan_form, name='loan_form'),
    path('status',views.my_loan_status, name='my_loan_status'), 
    path('reports/', views.reports, name='reports'),
    path('download/', views.download_excel, name='download_excel'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('download/gender-report/', views.download_gender_report, name='download_gender_report'),
    path('signupforuser/', CustomSignupView.as_view(), name='signupforuser'),
    path('records/', views.view_records, name='view_records'),
    path('records/delete/<int:record_id>/', views.delete_record, name='delete_record'),
    path('records/approve/<int:record_id>/', views.approve_record, name='approve_record'),
    path('records/disapprove/<int:record_id>/', views.disapprove_record, name='disapprove_record'),
    path('status/', views.status_view, name='status'),
]
    
#path('signup/', CustomSignupView.as_view(), name='signup'),
#path('', views.loan_entry_page, name='loan_entry_page'),  # root URL