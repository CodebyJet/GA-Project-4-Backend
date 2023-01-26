from django.urls import path
from .views import RegisterView, LoginView, UserViews, UserSpecificView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', UserViews.as_view()),
    path('user/<int:pk>/', UserSpecificView.as_view()),
]
