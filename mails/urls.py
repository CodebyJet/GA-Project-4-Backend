from django.urls import path
from .views import MailListView, MailDetailView

urlpatterns = [
    path('', MailListView.as_view()),
    path('<int:pk>/', MailDetailView.as_view())
]
