from django.contrib import admin

from . import models, helper
from django.utils.safestring import mark_safe


def sync_tweets(modeladmin, request, queryset):
    for user in queryset.all():
        helper.update_or_create_user(user.screen_name)
        helper.sync_user_tweets(user)


sync_tweets.short_description = "爬取推文"


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('screen_name', 'name', 'description', 'is_active', 'created_at', 'create_time')
    raw_id_fields = ('user',)
    search_fields = ("name", 'screen_name')
    date_hierarchy = 'create_time'
    actions = [sync_tweets]


@admin.register(models.Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_text', 'url_link', 'favorite_count', 'retweet_count', 'created_at', 'create_time')
    raw_id_fields = ('user',)
    list_filter = ('user',)
    search_fields = ("full_text",)
    date_hierarchy = 'create_time'
    ordering = ('is_active', 'created_at', 'create_time', 'favorite_count', 'retweet_count')

    def url_link(self, obj):
        return mark_safe('<a href="%s" target="_blank">%s</a>' % (obj.url, obj.url))

    url_link.short_description = "网址"
