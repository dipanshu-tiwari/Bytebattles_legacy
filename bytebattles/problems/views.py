import json

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator
from django.db.models import FloatField, ExpressionWrapper, Value, Case, When, F, Q

from .models import Problem
from app.models import Category

def problems(request):
    page = request.GET.get('page')
    order = request.GET.get('order', '')

    problem_set = Problem.objects.filter(visibility=True)

    if order in ['ACR_ASC', 'ACR_DSC']:
        problem_set = problem_set.annotate(
            acr_value=Case(
                When(total_submissions=0, then=Value(0.0)),
                default=ExpressionWrapper(
                    100.0 * F('accepted_submissions') / F('total_submissions'),
                    output_field=FloatField()
                ),
                output_field=FloatField()
            )
        )

    ordering_options = {
        'RATING_ASC': 'rating',
        'RATING_DSC': '-rating',
        'ACR_ASC': 'acr_value',
        'ACR_DSC': '-acr_value',
    }
    ordering = ordering_options.get(order, '-time_created')
    problem_set = problem_set.order_by(ordering)

    min_rating = request.GET.get('min-rating', '0')
    max_rating = request.GET.get('max-rating', '3500')
    query = request.GET.get('query', '')

    try:
        min_rating = int(min_rating)
    except:
        min_rating = 0
    try:
        max_rating = int(max_rating)
    except:
        max_rating = 3500
    try:
        categories = json.loads(request.GET.get('categories', '[]'))
    except:
        categories = []

    problem_set = problem_set.filter(name__icontains=query)
    problem_set = problem_set.filter(Q(rating__gte=min_rating) & Q(rating__lte=max_rating))
    for category in categories:
        problem_set = problem_set.filter(categories__slug=category).distinct()

    paginator = Paginator(problem_set, 8)
    problems = paginator.get_page(page)

    context = {
        'problems': problems,
        'categories': Category.objects.all()
    }

    return render(request, 'problems.html', context)

def details(request, pid):
    problem = get_object_or_404(Problem, pid=pid)
    if problem.visibility == False:
        raise Http404()

    context = {
        'problem': problem
    }
    return render(request, 'details.html', context)