from django.contrib import admin
from . import models

# Register your models here.

# tabular chosen due to models being short and compact
class CommentInLine(admin.TabularInline):
    model = models.Comment
    extra = 0  # Do not show blank rows
    fields = ('name', 'email', 'text', 'approved')  # Show only these
    readonly_fields = ('name', 'email', 'text')  # These fields are read-only

@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'status',
        'created',
        'updated',
    )

    search_fields = (
        'title',
        'author__username',
        'author__first_name',
        'author__last_name',
    )

    list_filter = (
        'status',
        'topics',
    )

    prepopulated_fields = {'slug': ('title',)}
    inlines = [CommentInLine]   # Connects CommentInLine to PostAdmin

@admin.register(models.Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    prepopulated_fields = {'slug': ('name',)}


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'approved',
        'created',
        'post',
    )

    search_fields = (
        'name',
        'email',
        'text',
    )

    list_filter = (
        'approved',
    )

