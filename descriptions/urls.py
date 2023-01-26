from django.urls import path
from .views import DescriptionListView, DescriptionDetailView

urlpatterns = [
    path('', DescriptionListView.as_view()),
    path('<int:pk>/', DescriptionDetailView.as_view())
]
