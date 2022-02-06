from django.urls import path, include,re_path
from users import views
from django.contrib.auth import views as auth_views

# Be careful setting the name to just /login use userlogin instead!
# SET THE NAMESPACE!
app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),
    re_path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
         views.activate, name='activate'),
    

    # path('password_reset/',
    #      auth_views.PasswordResetView.as_view(),
    #      {
    #          'post_reset_redirect': '/user/password_reset/done/'
    #      },
    #      name='password_reset'),
    #
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    #
    # path('reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
    #      auth_views.PasswordResetConfirmView.as_view(),
    #      {
    #          'post_reset_redirect': '/user/reset/done/'
    #      },
    #      name='password_reset_confirm'),
    #
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
