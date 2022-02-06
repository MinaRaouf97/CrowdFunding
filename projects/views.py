from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import datetime
import math
from django import template
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Q, Sum
from django.db.models.query import prefetch_related_objects
from django.http import HttpResponse
from django.shortcuts import redirect, render

from django.http import HttpResponseRedirect
from .models import Donation, Project, ProjectImage, Category 
from .forms import ProjectForm, ProjectImageForm
from users.models import UserProfileInfo


from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin




register = template.Library()

@login_required
def index(request):
    topRatedProjects = Project.objects.annotate(
        comment_rate=Avg('comment__rate')).order_by('-comment_rate')[:5]
    latestProjects = Project.objects.order_by('start_date')[:5]
    featuredProjects = Project.objects.filter(
        featured=True).order_by('start_date')[:5]

    # preparing Top Rated Projects in One List
    topRatedProjectsList = []
    for project in topRatedProjects:
        topRatedProjectsList.append({
            'id': project.id,
            'title': project.title,
            'rate': project.comment_rate,
            'target': project.target,
            'img': (project.projectimage_set.first().img.url if ( project.projectimage_set.count() > 0 ) else "/media/project_images/NotFound.png")
        })

    # preparing Latest Projects in One List
    latestProjectsList = []
    for project in latestProjects:
      
        latestProjectsList.append({
            'id': project.id,
            'title': project.title,
            'details': project.details,
            'target': project.target,
            'start_date': project.start_date,
            'img': (project.projectimage_set.first().img.url if ( project.projectimage_set.count() > 0 ) else "/media/project_images/NotFound.png")
        })

    # preparing Featured Projects in One List
    featuredProjectsList = []
    for project in featuredProjects:
    
        featuredProjectsList.append({
            'id': project.id,
            'title': project.title,
            'details': project.details,
            'target': project.target,
            'start_date': project.start_date,
            'img': (project.projectimage_set.first().img.url if ( project.projectimage_set.count() > 0 ) else "/media/project_images/NotFound.png")
            
        })
    # imgSrc = topRatedProjects[0].projectimage_set.first().img.url
    context = {
        'topRatedProjectsList': topRatedProjectsList,
        'latestProjectsList': latestProjectsList,
        'featuredProjectsList': featuredProjectsList,
    }
    return render(request, "projects/index.html", context)

@login_required
def project_search(request):
    query = request.GET.get('q')
    result = []
    # get the query result
    if query:
        result = Project.objects.filter(
            Q(title__icontains=query) |
            Q(title__icontains=query)
        ).distinct().annotate(comment_rate=Avg('comment__rate'))
    resultList = []

    # preparing the result to the tempalte
    for project in result:
        print(project)
        resultList.append({
            'id':project.id,
            'title': project.title,
            'rate': project.comment_rate,
            'target': project.target,
            'details': project.details,
            'start_date':project.start_date,
            'img': (project.projectimage_set.first().img.url if ( project.projectimage_set.count() > 0 ) else "/media/project_images/NotFound.png")
        })
    return render(request, 'projects/search_result.html', {'result': resultList})

    Project.objects.filter(Q(title__icontains="project") | Q(
        details__icontains="project")).distinct().annotate

def myProjects(request):
    current_user = request.user.id

    myProjects = Project.objects.filter(user_id=current_user).order_by('start_date')
# preparing User Projects in One List
    myProjectsList = []
    for project in myProjects:
        print ("my projects : ",myProjectsList)
        myProjectsList.append({
                'id': project.id,
                'title': project.title,
                'details': project.details,
                'target': project.target,
                'start_date': project.start_date,
                'img': (project.projectimage_set.first().img.url if ( project.projectimage_set.count() > 0 ) else "/media/project_images/NotFound.png")
    })    
    return render(request, 'projects/myprojects.html', {'myProjects': myProjectsList})
      
def myDonations(request):
    current_user = request.user.id

    
    myDonations = Donation.objects.select_related().filter(user_id=current_user)

    allData=[]
    for donate in myDonations:
        selectedProject = Project.objects.get(id=donate.project_id)
        allData.append({
                'amount':donate.amount,
                'id': selectedProject.id,
                'title': selectedProject.title,
                'details': selectedProject.details,
                'target': selectedProject.target,
                'start_date': selectedProject.start_date,
                'img': (selectedProject.projectimage_set.first().img.url if ( selectedProject.projectimage_set.count() > 0 ) else "/media/project_images/NotFound.png")
    })    
    # print(selectedProject)
        
    return render(request, 'projects/myDonations.html', {'myProjects': allData})
            
             

# create new project function
@login_required
def create_project(request):
    if request.method == 'GET' :
        form = ProjectForm()
    else:
        form = ProjectForm(request.POST)
        files = request.FILES.getlist('images')
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user_id = request.user.id
            obj.save()
            last_id =Project.objects.latest('id')
            return redirect('/projects/project_images/'+ str(last_id.id))
    return render(request,'projects/add.html', {'form': form})

#  upload images form and function
@login_required
def project_images(request, project_id):
    if request.method == 'GET' :
        form = ProjectImageForm()
    else:
        form = ProjectImageForm(request.POST)
        files = request.FILES.getlist('images')
        if request.FILES['images']:
            for f in files:
                ProjectImage.objects.create(project_id=project_id,img=f)
           
            return redirect('/projects')
    return render(request,'projects/upload_images.html', {'form': form})

@login_required
def list_projects_with_categories(request):
    all_projects = Project.objects.all()
    projects = []
    for project in all_projects:
        projects.append({
            'id': project.id,
            'title': project.title,
            'img': (project.projectimage_set.first().img.url if ( project.projectimage_set.count() > 0 ) else "/media/project_images/NotFound.png")
        })
     
    categories = Category.objects.all()
    return render(request,'projects/app.html', {'projects': projects, 'categories': categories})


@login_required
def user_profile(request):
    current_user = request.user
    usrInfo = UserProfileInfo.objects.select_related().get(user_id=current_user.id)
    username = current_user.username 
    first_name = current_user.first_name 
    last_name = current_user.last_name 
    password = current_user.password
    phone =  usrInfo.phone
    profile_image = usrInfo.profile_pic
    email = current_user.email
    
    
    context= {}

    usrData ={
        'username':username,
        'first_name':first_name,
        'last_name':last_name,
        'phone':phone,
        'profile_image':profile_image,
        'email':email,
    }
    
    context['userData'] = usrData
    
 


    return render(request,'projects/profile.html', context)


@login_required
def edit_profile(request):
    current_user = request.user
    usrInfo = UserProfileInfo.objects.select_related().get(user_id=current_user.id)

    if request.method == 'GET':
  
        username = current_user.username 
        first_name = current_user.first_name 
        last_name = current_user.last_name 
        phone =  usrInfo.phone
        profile_image = usrInfo.profile_pic
        
        context= {}

        usrData ={
            'username':username,
            'first_name':first_name,
            'last_name':last_name,
            'phone':phone,
            'profile_image':profile_image,
            
        }
        
        context['userData'] = usrData
        
        return render(request,'projects/edit_profile.html', context)

    elif request.method == 'POST' and 'updateuser' in request.POST:
        try:
            # print(request.FILES['profile_image'])
            print(request.POST['first_name'])
            print(current_user.first_name)
            current_user.username=request.POST['username']
            current_user.first_name=request.POST['first_name']
            current_user.last_name=request.POST['last_name']
            
            # usrInfo.phone=request.POST['phone']
            # usrInfo.profile_pic = request.FILES['profile_image']

            current_user.save()
            usrInfo.save()
        except:
            print("error in saving update")
        
        return redirect('profile')
    
    elif request.method == 'POST' and 'deleteAccount' in request.POST:
        
        # u = User.objects.get(id=current_user.id)
        # print(u)

        try:
            print("111111111111111111111111")
            User.objects.filter(id=current_user.id).delete()
            # u = User.objects.get(id=current_user.id)
           
            
            # u.delete()
            messages.success(request, "The user is deleted")
            return HttpResponseRedirect('/users/user_login')


        except Exception as e: 
            return render(request, 'projects/edit_profile.html',{'err':e.message})




# @login_required
# def change_password(request):
    
class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'projects/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('profile')