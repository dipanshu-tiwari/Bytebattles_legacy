from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from submissions.models import Submission, Verdict
from problems.models import Problem
from django.core.paginator import Paginator
from .models import Profile

from django.db.models import Max

def profile(request, username):
    profile = get_object_or_404(Profile, user=User.objects.get(username=username))

    submissions = Submission.objects.filter(user=profile.user)

    total_submissions = submissions.count()
    accepted_submissions = submissions.filter(verdict=Verdict.AC.name).count()
    wa_submissions = submissions.filter(verdict=Verdict.WA.name).count()
    tle_submissions = submissions.filter(verdict=Verdict.TLE.name).count()
    mle_submissions = submissions.filter(verdict=Verdict.MLE.name).count()

    problem_solved = submissions.filter(verdict=Verdict.AC.name).distinct('problem').count()
    total_attempted = submissions.distinct('problem').count()
    total_problems = Problem.objects.all().count()

    profile.rating = round(problem_solved * 3000 / total_problems if total_problems > 0 else 0, 1)
    profile.save()

    context = {
        'profile': profile,

        'problem_solved': problem_solved,
        'total_attempted': total_attempted,
        'total_problems': total_problems,
        'percent_solved': round(problem_solved * 100 / total_problems if total_problems > 0 else 0, 1),

        'accepted_submissions': accepted_submissions,
        'wa_submissions': wa_submissions,
        'tle_submissions': tle_submissions,
        'mle_submissions': mle_submissions,
        'total_submissions': total_submissions,
        'percent_accepted': round(accepted_submissions * 100 / total_submissions if total_submissions > 0 else 0, 1),
    }
    return render(request, 'profile.html', context)

def submissions(request, username):
    profile = get_object_or_404(Profile, user=User.objects.get(username=username))

    p = Paginator(Submission.objects.filter(user=profile.user).order_by('-time'), 8)

    page = request.GET.get('page')
    submissions = p.get_page(page)

    context = {
        'profile': profile,
        'submissions': submissions
    }
    return render(request, 'submissions.html', context)

def solved_problems(request, username):
    profile = get_object_or_404(Profile, user=User.objects.get(username=username))

    solved = Problem.objects.filter(
        submissions__user=request.user,
        submissions__verdict=Verdict.AC.name
    ).annotate(latest_ac=Max('submissions__time')).order_by('-latest_ac')


    p = Paginator(solved, 8)

    page = request.GET.get('page')
    solved = p.get_page(page)

    context = {
        'profile': profile,
        'solved': solved
    }
    return render(request, 'solved_problems.html', context)