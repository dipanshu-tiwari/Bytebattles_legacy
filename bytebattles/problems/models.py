from django.db import models
from app.models import Category

class Problem(models.Model):
    pid = models.CharField(max_length=6, primary_key=True, unique=True, db_index=True)
    name = models.CharField()
    level = models.CharField(max_length=1, blank=True, null=True)
    statement = models.TextField()
    constraints = models.JSONField(default=list, null=True, blank=True)
    input = models.TextField()
    output = models.TextField()
    note = models.TextField(blank=True, null=True)
    sample_io = models.JSONField()

    time_created = models.DateTimeField(auto_now_add=True)

    memory_limit = models.IntegerField()
    time_limit = models.IntegerField()
    test_count = models.IntegerField()

    rating = models.IntegerField()
    categories = models.ManyToManyField(to=Category, related_name='problems')

    visibility = models.BooleanField(default=False)
    source = models.CharField(blank=True, null=True)

    accepted_submissions = models.IntegerField(default=0)
    total_submissions = models.IntegerField(default=0)

    def __str__(self):
        return self.pid
    
    def acr(self):
        if self.total_submissions == 0:
            return "-"
        else:
            return round(100 * self.accepted_submissions / self.total_submissions, 2)
    
    def isCSES(self):
        return self.pid.__contains__("CSES")