"""
Provides global context variables for templates.

Includes:
- List of authors (ordered by first name) who have published posts.
- Top 10 topics based on number of related posts.
"""

from django.db.models import Count
from . import models


def base_context(request):
    authors = (
        models.Post.objects.published()
        .get_authors()
        .order_by('first_name')
    )

    # Move global queries to context_processors
    top_topics = models.Topic.objects.annotate(
        post_count=Count('blog_posts')
    ).order_by('-post_count')[:10]

    return {
        'authors': authors,
        'top_topics': top_topics
    }