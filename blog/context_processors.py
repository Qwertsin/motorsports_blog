from django.db.models import Count
from . import models


def base_context(request):
    authors = models.Post.objects.published() \
        .get_authors() \
        .order_by('first_name')

    top_topics = models.Topic.objects.annotate(
        post_count=Count('blog_posts')
    ).order_by('-post_count')[:10]

    return {
        'authors': authors,
        'top_topics': top_topics
    }