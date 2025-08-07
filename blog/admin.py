"""
Django admin configuration for the blog app.
Registers Post, Topic, and Comment models with custom admin settings.
"""

from django.contrib import admin
from . import models


# tabular chosen due to models being short and compact
class CommentInLine(admin.TabularInline):
    """Inline admin configuration for Comment model on the Post detail page."""
    model = models.Comment
    extra = 0  # Do not show blank rows
    fields = ('name', 'email', 'text', 'approved')  # Show only these
    readonly_fields = ('name', 'email', 'text')  # These fields are read-only


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    """Admin configuration for the Post model."""
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
    inlines = [CommentInLine]  # Connects CommentInLine to PostAdmin


@admin.register(models.Topic)
class TopicAdmin(admin.ModelAdmin):
    """Admin configuration for the Topic model."""
    list_display = (
        'name',
        'slug',
    )
    prepopulated_fields = {'slug': ('name',)}


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin configuration for the Comment model."""
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

@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'last_name',
        'first_name',
        'submitted'
    )
    # Make these fields read-only in the admin
    readonly_fields = (
        'first_name',
        'last_name',
        'email',
        'message',
        'submitted'
    )
