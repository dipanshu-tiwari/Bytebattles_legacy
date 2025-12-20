from django.urls import path
from .views import details, problems

urlpatterns = [
    path('', problems, name='problems'),
    path('<str:pid>/', details, name='details')
]