from django.urls import path
from .views import submit, result, run_all

urlpatterns = [
    path('new/', submit, name='submit'),
    path('new/<str:pid>/', submit, name='submitpid'),
    path('<int:pk>/', result, name='result'),
    path('run_all/', run_all, name=None)
]