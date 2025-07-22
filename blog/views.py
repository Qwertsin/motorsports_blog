"""Views for the blog application."""

from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.generic import DetailView

from . import models

class HomeView(TemplateView):
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
    template_name = 'blog/about.html'


def terms_and_conditions(request):
   return render(request, 'blog/terms_and_conditions.html')

class PostListView(ListView):
    model = models.Post
    context_object_name = 'posts'
    queryset = models.Post.objects.published().order_by('-published')

class PostDetailView(DetailView):
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
    model = models.Topic
    context_object_name = 'topics'

class TopicDetailView(DetailView):
    model = models.Topic
    context_object_name = 'topic'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic = self.get_object()

        posts = topic.blog_posts.filter(
            status=models.Post.PUBLISHED
        ).order_by('-published')

        context['posts'] = posts
        return context