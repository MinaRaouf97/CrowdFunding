from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from .views import index,ChangePasswordView, project_search,myProjects,myDonations,create_project,project_images,list_projects_with_categories,user_profile,edit_profile
urlpatterns = [
    path('/', index, name="projects_index"),
    path('project_search', project_search, name="project_search"),
    path('<int:id>/', include('single_project.urls')),
    path('myProjects', myProjects, name="myProjects"),
    path('myDonations', myDonations, name="myDonations"),
    path('add_project',create_project , name="create_project"),
    path('project_images/<int:project_id>/',project_images , name="project_images"),
    path('app',list_projects_with_categories, name="all_projects" ),
    path('profile',user_profile,name='profile'),
    path('profile/edit',edit_profile,name='edit_profile'),
    # path('profile/changepassword',change_password,name='change_password'),
    path('password-change/', ChangePasswordView.as_view(), name='change_password'),

    
    



]
