from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q, Count
from datetime import datetime, timedelta
from .models import Confession, Comment, Like, UserProfile
from .forms import CustomUserCreationForm, ConfessionForm, CommentForm


def home(request):
    """广场页面 - 显示最新已审核内容"""
    confessions = Confession.objects.filter(status='approved').order_by('-created_at')
    return render(request, 'confession/home.html', {
        'confessions': confessions,
        'active_tab': 'square'
    })


def hot(request):
    """热度榜页面"""
    period = request.GET.get('period', 'today')

    # 时间范围筛选
    today = timezone.now().date()
    if period == 'today':
        start_date = today
    elif period == 'week':
        start_date = today - timedelta(days=7)
    elif period == 'month':
        start_date = today - timedelta(days=30)
    else:
        start_date = None

    confessions = Confession.objects.filter(status='approved')
    if start_date:
        confessions = confessions.filter(created_at__gte=start_date)

    confessions = confessions.order_by('-likes_count', '-created_at')

    return render(request, 'confession/hot.html', {
        'confessions': confessions,
        'active_tab': 'hot',
        'current_period': period
    })


@login_required
def my_confessions(request):
    """我的表白页面"""
    confessions = Confession.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'confession/my_confessions.html', {
        'confessions': confessions,
        'active_tab': 'my'
    })


def register(request):
    """用户注册"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 信号处理器会自动创建 UserProfile，所以这里不需要手动创建
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'confession/register.html', {'form': form})


def login_view(request):
    """用户登录"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'confession/login.html', {'error': '用户名或密码错误'})
    return render(request, 'confession/login.html')


def logout_view(request):
    """用户登出"""
    logout(request)
    return redirect('home')


@login_required
def create_confession(request):
    """发布表白"""
    if request.user.userprofile.is_banned:
        return render(request, 'confession/error.html', {
            'error': '您的账号已被禁言，无法发布内容'
        })

    if request.method == 'POST':
        form = ConfessionForm(request.POST, request.FILES)
        if form.is_valid():
            confession = form.save(commit=False)
            confession.user = request.user
            confession.save()
            return redirect('my_confessions')
    else:
        form = ConfessionForm()
    return render(request, 'confession/create_confession.html', {'form': form})


@login_required
def delete_confession(request, confession_id):
    """删除表白"""
    confession = get_object_or_404(Confession, id=confession_id)

    # 只能删除自己的表白或管理员
    if confession.user == request.user or request.user.is_staff:
        confession.delete()

    if request.user.is_staff:
        return redirect('admin_confessions')
    return redirect('my_confessions')


@login_required
def like_confession(request, confession_id):
    """点赞/取消点赞"""
    if request.method == 'POST':
        confession = get_object_or_404(Confession, id=confession_id)

        # 检查用户是否已点赞
        like, created = Like.objects.get_or_create(
            user=request.user,
            confession=confession
        )

        if not created:
            # 如果已经点赞，则取消点赞
            like.delete()
            confession.likes_count -= 1
        else:
            # 新点赞
            confession.likes_count += 1

        confession.save()

        return JsonResponse({
            'likes_count': confession.likes_count,
            'is_liked': created
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def add_comment(request, confession_id):
    """添加评论"""
    if request.user.userprofile.is_banned:
        return JsonResponse({'error': '您的账号已被禁言，无法评论'}, status=403)

    if request.method == 'POST':
        confession = get_object_or_404(Confession, id=confession_id, status='approved')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.confession = confession
            comment.save()
            return redirect('home')

    return redirect('home')


@login_required
def delete_comment(request, comment_id):
    """删除评论"""
    comment = get_object_or_404(Comment, id=comment_id)

    # 只能删除自己的评论或管理员
    if comment.user == request.user or request.user.is_staff:
        comment.delete()

    return redirect('home')


def is_staff(user):
    return user.is_staff


@user_passes_test(is_staff)
def admin_confessions(request):
    """管理员审核页面"""
    status_filter = request.GET.get('status', 'pending')

    if status_filter == 'all':
        confessions = Confession.objects.all()
    else:
        confessions = Confession.objects.filter(status=status_filter)

    confessions = confessions.order_by('-created_at')

    return render(request, 'confession/admin_confessions.html', {
        'confessions': confessions,
        'status_filter': status_filter
    })


@user_passes_test(is_staff)
def approve_confession(request, confession_id):
    """审核通过表白"""
    confession = get_object_or_404(Confession, id=confession_id)
    confession.status = 'approved'
    confession.save()
    return redirect('admin_confessions')


@user_passes_test(is_staff)
def reject_confession(request, confession_id):
    """审核拒绝表白"""
    confession = get_object_or_404(Confession, id=confession_id)
    confession.status = 'rejected'
    confession.save()
    return redirect('admin_confessions')


@user_passes_test(is_staff)
def ban_user(request, user_id):
    """禁言用户"""
    user = get_object_or_404(User, id=user_id)
    user.userprofile.is_banned = True
    user.userprofile.save()
    return redirect('admin_confessions')


@user_passes_test(is_staff)
def unban_user(request, user_id):
    """解除禁言"""
    user = get_object_or_404(User, id=user_id)
    user.userprofile.is_banned = False
    user.userprofile.save()
    return redirect('admin_confessions')