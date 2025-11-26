from django.urls import path
from . import views

urlpatterns = [
    # 公开页面
    path('', views.home, name='home'),
    path('hot/', views.hot, name='hot'),

    # 用户认证
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # 用户功能
    path('my/', views.my_confessions, name='my_confessions'),
    path('create/', views.create_confession, name='create_confession'),
    path('delete/<int:confession_id>/', views.delete_confession, name='delete_confession'),
    path('like/<int:confession_id>/', views.like_confession, name='like_confession'),
    path('comment/<int:confession_id>/', views.add_comment, name='add_comment'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),

    # 管理员功能 - 使用 manage/ 前缀避免与Django admin冲突
    path('manage/confessions/', views.admin_confessions, name='admin_confessions'),
    path('manage/approve/<int:confession_id>/', views.approve_confession, name='approve_confession'),
    path('manage/reject/<int:confession_id>/', views.reject_confession, name='reject_confession'),
    path('manage/ban/<int:user_id>/', views.ban_user, name='ban_user'),
    path('manage/unban/<int:user_id>/', views.unban_user, name='unban_user'),
]