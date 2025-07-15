"""Views for the blog application."""

from django.shortcuts import render
from django.db.models import Count

from . import models


def home(request):
    """
    Homepage view showing recent posts and a sidebar of top topics.
    """
    latest_posts = models.Post.objects.published().order_by('-published')

    # Get top 10 topics by number of related posts
    top_topics = models.Topic.objects.annotate(
        post_count=Count('blog_posts')
    ).order_by('-post_count')[:10]

    context = {
        'latest_posts': latest_posts,
        'top_topics': top_topics
    }

    return render(request, 'blog/home.html', context)