from django.contrib import admin
from .models import Project,ProjectImage, Category , Donation

# Register your models here.
admin.site.register(Project)
admin.site.register(Category)
admin.site.register(ProjectImage)
admin.site.register(Donation)
