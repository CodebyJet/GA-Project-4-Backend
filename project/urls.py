from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('jwt_auth.urls')),
    path('api/description/', include('descriptions.urls')),
    path('api/mail/', include('mails.urls')),
    path('api/quiz/', include('quizs.urls')),
]
