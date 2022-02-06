from django.db import models
from django.contrib.auth.models import User
from projects.models import Project
class Comment(models.Model):
    rate = models.IntegerField()
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    reports = models.IntegerField(default = 0)

    def __str__(self):
        return self.project.title


class ReportedProject(models.Model) : 
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 

class ReportedComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 