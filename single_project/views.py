from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import datetime
import math
from django import template
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Q, Sum
from django.db.models.query import prefetch_related_objects
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import AddCommentForm
from .models import Comment, ReportedComment , ReportedProject
from projects.models import Donation, Project, ProjectImage

register = template.Library()

def get_users_info (p_id,comments,user_names,current_user) :
    if len(user_names) == 0 :
        return []
    users_info=[]
    for i, user in enumerate(user_names):
        amount = Donation.objects.filter(user_id=user[1], project_id=p_id).aggregate(Sum('amount'))
        if amount['amount__sum'] == None:
            amount['amount__sum'] = "0"
        # check user's privelges over the comment
        can_delete_comment = (current_user == user[1])
        can_report_comment = not can_delete_comment
        reported_before = bool(ReportedComment.objects.filter(comment_id = comments[i]['id'] , user_id = current_user))
        user_info = {
            "user_name": user_names[i][0],
            "amount": int(amount['amount__sum']),
            "comment": comments[i]['comment'],
            "comment_id": comments[i]['id'],
            "rate": comments[i]['rate'],
            "can_delete" : can_delete_comment,
            "can_report" : can_report_comment,
            "reported_before" : reported_before,
        }
        users_info.append(dict(user_info))
    return users_info

def get_donators_info(p_id):
    # get donation info
    all_donations = Donation.objects.filter(
        project_id=p_id).prefetch_related('user')
    donation_info = list(all_donations.values('user_id').annotate(sum=Sum('amount')).order_by('-sum'))
    donators = []
    donator_id = []
    for entry in donation_info:
        for data in all_donations:
            if data.user.id == entry['user_id'] and data.user.id not in donator_id:
                donators.append(
                    {"user_name": data.user.username, "sum": entry['sum']})
                # to make sure that the name won't be repeated
                donator_id.append(data.user.id)
    return donators
def check_reported_before (p_id,u_id) : 
    report = ReportedProject.objects.filter(project_id = p_id , user_id = u_id)
    return bool(len(report))

@login_required
def view_project(request, id):
    current_user = request.user.id
    project = Project.objects.get(id=id)
    featured_img = project.projectimage_set.first()
    if featured_img != None : 
        featured_img = featured_img.img.url
        imgs_objects = project.projectimage_set.all()
        imgs = []
        for img in imgs_objects:
            imgs.append(img.img.url)
    else : 
        featured_img = 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/450px-No_image_available.svg.png'
        imgs = []
    comments = list(project.comment_set.values())
    # get user name by populating comments
    populated_comments = project.comment_set.all()
    user_names = [(entry.user.username, entry.user.id)
                  for entry in populated_comments]
        # Get the progress of project
    total_amount = Donation.objects.filter(
        project_id=id).aggregate(Sum('amount'))['amount__sum']
    target = project.target
    if not total_amount:
        total_amount = 0
    percentage = math.floor(total_amount*100/target)
    target_reached = False
    if percentage > 100:
        target_reached = True

    # check if the userprevielges
    can_cancel = True if percentage < 25 and project.user_id == current_user else False
    can_report = True if project.user_id != current_user else False
    user_comments_count = populated_comments.filter(
        user_id=current_user, project_id=id).count()
    can_comment = not bool(user_comments_count)
    reported_before = check_reported_before(id,current_user)
    avg_rate = Comment.objects.filter(project_id=id).aggregate(Avg('rate'))
    if avg_rate['rate__avg'] == None:
        avg_rate['rate__avg'] = "0"

    # ِAdd comment form
    form = AddCommentForm()
    # get donation amount for everyh person
    users_info = get_users_info(id,comments, user_names,current_user)
    donators = get_donators_info(id)
    context = {
        "project": project,
        "featured_img": featured_img,
        "form": form,
        "imgs": imgs,
        'comments': comments,
        "donators": donators,
        "users_info": users_info,
        "avg_rate": range(int(avg_rate['rate__avg'])),
        "rest_of_stars": range((5-int(avg_rate['rate__avg']))),
        "total_amount": total_amount,
        "target": target,
        "target_reached":target_reached,
        "percentage": percentage,
        "can_comment": can_comment,
        "can_cancel" : can_cancel,
        "can_report" : can_report,
        "reported_before" : reported_before,
    }
    return render(request, 'single_project/project_page.html/', context)
@login_required
def add_comment(request,id):
    if request.method == 'POST':
        project_id = int(request.POST['project_id'])
        current_user = request.user.id
        form = AddCommentForm(request.POST)
        if form.is_valid():
            comment = Comment()
            comment.rate = int(form['rate'].value())
            comment.comment = form['comment'].value()
            comment.project_id = project_id
            comment.user_id = current_user
            comment.save()
            return redirect('/projects/'+str(project_id))
        return redirect('/projects/'+str(project_id))
    else : 
         return redirect('/projects/')
@login_required
def donate(request,id):
    current_user = request.user.id
    donation = Donation()
    donation.amount = request.POST['amount']
    donation.project_id = request.POST['project_id']
    donation.user_id = current_user
    donation.save()
    return redirect('/projects/'+str(donation.project_id))

def cancel_project(request,id):
    current_user = request.user.id
    p_id = request.POST['project_id']
    project = Project.objects.get(id=p_id)
    # check if the deleter is the project owner
    if current_user == project.user_id:
        project.delete()
        return redirect('/')
    return redirect('/projects/'+str(p_id))
@login_required    
def report_project(request,id) :
    current_user = request.user.id
    p_id = request.POST['project_id']
    project = Project.objects.get(id=p_id)
    reported_before = check_reported_before(p_id,current_user)
    # check if the deleter is the project owner
    if current_user != project.user_id and not reported_before:
        project.reports+=1
        project.save()
        report = ReportedProject()
        report.user_id = current_user
        report.project_id = p_id
        report.save()
        return redirect('/projects/'+str(p_id))
    return redirect('/projects/'+str(p_id))
@login_required    
def delete_comment(request,id):
    current_user = request.user.id
    c_id = request.POST['comment_id']
    p_id = request.POST['project_id']
    # we won't use get because it will return error if it's not exist
    comment = Comment.objects.get(id=c_id,user_id=current_user)
    # check if the deleter is the project owner
    if current_user == comment.user_id and comment:
        comment.delete()
        return redirect('/projects/'+str(p_id))
    return redirect('/projects/'+str(p_id))
@login_required    
def report_comment(request,id) :
    current_user = request.user.id
    c_id = request.POST['comment_id']
    p_id = request.POST['project_id']
    comment = Comment.objects.get(id=c_id)
    # check if the deleter is the project owner
    if current_user != comment.user_id:
        comment.reports+=1
        comment.save()
        report = ReportedComment()
        report.user_id = current_user
        report.comment_id = c_id
        report.save()
        return redirect('/projects/'+str(p_id))
    return redirect('/projects/'+str(p_id))
