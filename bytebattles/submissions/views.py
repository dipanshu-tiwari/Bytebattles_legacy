from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Submission, Language, Verdict
from django.contrib.auth.models import User
from problems.models import Problem
from judge.submission_worker import enqueueTask

from .utils import checkExtension

@login_required
def submit(request, pid=None):
    
    if request.method == 'POST':
        problem = request.POST.get('problem')
        language = request.POST.get('language')
        code = request.POST.get('code').strip()
        file = request.FILES.get('file')

        if not Problem.objects.filter(pid=problem).exists():
            messages.info(request, 'Invalid problem ID')
        elif (file == None and code != "") or (file != None and code == ""):
            if file:
                extension = file.name.split('.')[-1]
                if not checkExtension(extension):
                    messages.info(request, 'Uploaded file\'s extension was invalid')
                else:
                    code = file.read().decode('utf-8').strip()
                    if code == "":
                        messages.info(request, 'File is empty')
            
            if code != "":
                submission = Submission.objects.create(language=language, code=code, problem=Problem.objects.get(pid=problem), user=request.user)
                submission.save()
                enqueueTask(submission.pk)
                messages.info(request, 'Submitted successfully')
                return redirect('result', submission.pk)
        else:
            messages.info(request, 'Either write source code or select a file, only one of those')

    languages = Language.choices
    context = {
        'languages': languages
    }

    if pid:
        context['pid'] = pid
    return render(request, 'submit.html', context)

def result(request, pk):
    submission  = get_object_or_404(Submission, pk=pk)

    context = {
        'submission': submission,
        'verdict': Verdict
    }

    if submission.output != None and submission.incorrect_testcase != None:
        context['output'] = submission.output
        with open(f"test_case_data/{submission.problem.pid}/output/{submission.incorrect_testcase}.out", "r") as file:
            context['expected'] = file.read()
            if len(context['expected']) > 500:
                context['expected'] = context['expected'][:497] + "..."
    print(context)
    return render(request, 'result.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def run_all(request):
    submissions = Submission.objects.all()
    for sub in submissions:
        enqueueTask(sub.pk)

    return HttpResponse('Done')