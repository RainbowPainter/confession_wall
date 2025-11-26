from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Confession, Comment, Like, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class CustomUserAdmin(UserAdmin):
    inlines = [UserProfileInline]
    list_display = ['username', 'email', 'is_staff', 'get_is_banned']

    def get_is_banned(self, obj):
        return obj.userprofile.is_banned

    get_is_banned.short_description = '是否禁言'


class ConfessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'content_preview', 'status', 'likes_count', 'is_pinned', 'created_at']
    list_filter = ['status', 'is_pinned', 'created_at']
    list_editable = ['status', 'is_pinned']
    search_fields = ['content', 'user__username']
    actions = ['approve_confessions', 'reject_confessions']

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content

    content_preview.short_description = '内容预览'

    def approve_confessions(self, request, queryset):
        queryset.update(status='approved')

    approve_confessions.short_description = "审核通过选中的表白"

    def reject_confessions(self, request, queryset):
        queryset.update(status='rejected')

    reject_confessions.short_description = "审核拒绝选中的表白"


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'confession_preview', 'content_preview', 'created_at']
    search_fields = ['content', 'user__username']

    def confession_preview(self, obj):
        return obj.confession.content[:30] + '...' if len(obj.confession.content) > 30 else obj.confession.content

    confession_preview.short_description = '所属表白'

    def content_preview(self, obj):
        return obj.content[:30] + '...' if len(obj.content) > 30 else obj.content

    content_preview.short_description = '评论内容'


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Confession, ConfessionAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like)