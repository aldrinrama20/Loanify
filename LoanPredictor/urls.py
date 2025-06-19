from django.contrib import admin
from django.urls import path, include
from predictor.views import CustomLoginView, CustomLogoutView, reports_view, CustomSignupView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('predictor.urls')),
    path('login/', CustomLoginView.as_view(), name='login_user'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('signupforuser/', CustomSignupView.as_view(), name='signupforuser'),
    path('reports/', reports_view, name='reports'),
]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)