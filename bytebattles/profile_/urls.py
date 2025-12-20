from django.urls import path
from .views import profile, submissions, solved_problems

urlpatterns = [
    path('<str:username>/', profile, name='profile'),
    path('submissions/<str:username>/', submissions, name='submissions'),
    path('solved-problems/<str:username>/', solved_problems, name='solved_problems'),
]