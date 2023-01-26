from django.urls import path
from .views import QuizListView, QuizDetailView

urlpatterns = [
    path('', QuizListView.as_view()),
    path('<int:pk>/', QuizDetailView.as_view())
]
