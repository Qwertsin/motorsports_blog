"""Views for the blog application."""

from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.generic import DetailView

from . import models

class HomeView(TemplateView):
    """Render the home page with the latest published posts."""
    template_name = 'blog/home.html'

    def get_context_data(self, **kwargs):
        # Get the parent context
        context = super().get_context_data(**kwargs)

        latest_posts = models.Post.objects.published() \
            .order_by('-published')[:3]

        context.update({
            'latest_posts': latest_posts
        })

        return context

class AboutView(TemplateView):
    """Render the about page."""
    template_name = 'blog/about.html'


def terms_and_conditions(request):
    """Render the terms and conditions static page."""
    return render(request, 'blog/terms_and_conditions.html')

class PostListView(ListView):
    """List all published posts in reverse chronological order."""
    model = models.Post
    context_object_name = 'posts'
    queryset = models.Post.objects.published().order_by('-published')

class PostDetailView(DetailView):
    """Render the detailed view of a single post."""
    model = models.Post

    def get_queryset(self):
        queryset = super().get_queryset().published()

        # If this is a `pk` lookup, use default queryset
        if 'pk' in self.kwargs:
            return queryset

        # Otherwise, filter on the published date
        return queryset.filter(
            published__year=self.kwargs['year'],
            published__month=self.kwargs['month'],
            published__day=self.kwargs['day'],
        )

class TopicListView(ListView):
    """Render a list of all topics in alphabetical order."""
    model = models.Topic
    context_object_name = 'topics'
    queryset = models.Topic.objects.order_by('name')  # Topics listed alphabetically

class TopicDetailView(DetailView):
    """Render a detail view of a single topic with its related posts."""
    model = models.Topic
    context_object_name = 'topic'


    # Overriding the get_context_data() method allows the customization of the context variables to the template
    def get_context_data(self, **kwargs):
        """Add related published posts to the context, ordered by date."""
        context = super().get_context_data(**kwargs)
        # To access the topic object from the DetailView, use the self.get_object() method.
        topic = self.get_object() # Get the topic instance

        # Only published posts should appear
        # Posts should be ordered by latest to earliest published date
        posts = topic.blog_posts.filter(
            status=models.Post.PUBLISHED
        ).order_by('-published')

        context['posts'] = posts
        return context