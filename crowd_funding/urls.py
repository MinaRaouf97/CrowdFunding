from django.contrib import admin
from django.urls import path, include
# those imports are for the static files
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import settings
from projects.views import index
from single_project.views import view_project
from users import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('projects/', include('projects.urls')),
    path('', index),
    path('users/', include('users.urls')),
    path('logout/', views.user_logout, name='logout'),
    path('special/', views.special, name='special'),
    path('social-auth/', include('social_django.urls', namespace="social")),

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
