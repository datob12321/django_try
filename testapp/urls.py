from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('settings', views.settings, name='settings'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html',),
         name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"), name='password_reset_confirm'),
    path('reset_done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_complete.html'), name='password_reset_complete'),
    path('like_content/', views.like_content, name='like_content'),
    path('reset_done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_complete.html'), name='password_reset_complete'),
    path('upload_post/', views.upload_post, name='upload_post'),
    path('like_comment/<str:comment_id>/', views.like_comment, name='like_comment'),
    path('profile/<str:pk>/', views.profile, name='profile'),
    path('follow/', views.follow_user, name='follow'),
]

