from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from .views import donate, cancel_project, report_project , delete_comment , report_comment, view_project, add_comment

urlpatterns = [
    path('', view_project, name="project_details"),
    path('cancel_project', cancel_project),
    path('report_project', report_project),
    path('addcomment', add_comment),
    path('delete_comment', delete_comment),
    path('report_comment', report_comment),
    path('donate', donate),
 

]
