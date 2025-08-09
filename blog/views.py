"""Views for the blog application."""

from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import DetailView,CreateView, FormView, ListView
from django.urls import reverse_lazy
from django.contrib import messages

from . import forms, models

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

def form_example(request):
    # Handle the POST
    if request.method == 'POST':
        # Pass the POST data into a new form instance for validation
        form = forms.ExampleSignupForm(request.POST)

        # If the form is valid, return a different template.
        if form.is_valid():
            # form.cleaned_data is a dict with valid form data
            cleaned_data = form.cleaned_data

            return render(
                request,
                'blog/form_example_success.html',
                context={'data': cleaned_data}
            )
    # If not a POST, return a blank form
    else:
        form = forms.ExampleSignupForm()

    # Return if either an invalid POST or a GET
    return render(request, 'blog/form_example.html', context={'form': form})


class FormViewExample(FormView):
    template_name = 'blog/form_example.html'
    form_class = forms.ExampleSignupForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # Create a "success" message
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Thank you for signing up!'
        )
        # Continue with default behaviour
        return super().form_valid(form)

class ContactFormView(CreateView):
    model = models.Contact
    success_url = reverse_lazy('home')
    fields = [
        'first_name',
        'last_name',
        'email',
        'message',
    ]

    def form_valid(self, form):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Thank you! Your message has been sent.'
        )
        return super().form_valid(form)


class PhotoContestView(CreateView):
    """
    Handles photo contest submissions using a model-backed form.
    """
    model = models.PhotoSubmission
    form_class = forms.PhotoSubmissionForm
    template_name = 'blog/photo_contest.html'
    success_url = reverse_lazy('photo-contest')

    def form_valid(self, form):
        """
        Show a success message after saving the submission.
        """
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Thank you! Your photo submission has been received.'
        )
        return super().form_valid(form)