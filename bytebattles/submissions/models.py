from django.db import models
from problems.models import Problem
from django.contrib.auth.models import User

class Verdict(models.TextChoices):
    AC = 'AC', 'Accepted'
    WA = 'WA', 'Wrong Answer'
    TLE = 'TLE', 'Time Limit Exceeded'
    MLE = 'MLE', 'Memory Limit Exceeded'
    CA = 'CA', 'Compilation Error'
    RE = 'RE', 'Runtime Error'
    SKP = 'SKP', 'Skipped'
    PD = 'PD', 'Pending'

colorMap = {
    Verdict.AC.name: 'green-700',
    Verdict.WA.name: 'red-700',
    Verdict.TLE.name: 'red-700',
    Verdict.MLE.name: 'red-700',
    Verdict.CA.name: 'black',
    Verdict.RE.name: 'black',
    Verdict.SKP.name: 'gray-700',
    Verdict.PD.name: 'gray-700'
}

class Language(models.TextChoices):
    C = 'C', 'C'
    CPP = 'CPP', 'C++'
    PY = 'PY', 'Python'
    # JV = 'JV', 'Java'
    # JS = 'JS', 'Javascript'

class Submission(models.Model):
    language = models.CharField(
        max_length=3,
        choices=Language.choices
    )
    code = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='submissions')
    verdict = models.CharField(
        max_length=3,
        choices=Verdict.choices,
        default=Verdict.PD
    )
    incorrect_testcase = models.IntegerField(blank=True, null=True)
    output = models.TextField(blank=True, null=True)

    walltime = models.IntegerField(blank=True, null=True)
    memory = models.IntegerField(blank=True, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')

    def __str__(self):
        return str(self.pk)
    
    def color(self):
        return colorMap[self.verdict]