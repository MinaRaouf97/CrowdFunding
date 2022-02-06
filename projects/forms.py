from django import forms
from projects.models import Project, ProjectImage

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'category', 'details', 'target', 'tags', 'reports', 'featured', 'end_date']

class ProjectImageForm(forms.Form):
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = ProjectImage
        fields = '__all__'
