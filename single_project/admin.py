from django.contrib import admin
from .models import Comment , ReportedComment,ReportedProject

# Register your models here.
admin.site.register(ReportedComment)
admin.site.register(ReportedProject)
admin.site.register(Comment)