from django.conf import settings
from django.db import models
from django.utils import timezone


class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status=self.model.PUBLISHED)

    def drafts(self):
        return self.filter(status=self.model.DRAFT)


class Topic(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True  # No duplicates!
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Post(models.Model):
    """
    Represents a blog post
    """
    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published')
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(
        null=False,
        unique_for_date='published',
    )

    topics = models.ManyToManyField(
        Topic,
        related_name='blog_posts'
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # The Django auth user model
        on_delete=models.PROTECT,  # Prevent posts from being deleted
        related_name='blog_posts',
        null=False,
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=DRAFT,
        help_text='Set to "published" to make this post publicly visible',
    )
    content = models.TextField()
    published = models.DateTimeField(
        null=True,
        blank=True,
        help_text='The date & time this article was published'
    )

    objects = PostQuerySet.as_manager()

    slug = models.SlugField(
        null=False,
        help_text='The date & time this article was published',
        unique_for_date='published',  # Slug is unique for publication date
    )

    created = models.DateTimeField(auto_now_add=True)  # Sets on create
    updated = models.DateTimeField(auto_now=True)  # Updates on each save

    class Meta:
        ordering = ['-created']

    def publish(self):
        self.status = self.PUBLISHED
        self.published = timezone.now()

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    Represents a comment left by a user on a blog post.
    """
    # Many comments to one unique post therefore ForeignKey

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,  # Cascade deletes all comments when related posted is deleted
        related_name='comments',    # As per part 2
        null=False,  # Makes sure that each comment is linked to a post
    )

    # The name of the person making the comment
    name = models.CharField(
        max_length=50,
        null=False  # required field
    )

    # The email address for the commenter
    email = models.EmailField(
        null=False  # required field
    )

    # Text containing the actual comment
    text = models.TextField(
        max_length=500,
        null=False  # required field
    )

    # A boolean field which is intended for comment moderation
    approved = models.BooleanField(
        default=False   # Comments are hidden by default until approved
    )

    # A timestamp which is automatically set only on create
    created = models.DateTimeField(auto_now_add=True)  # Sets on create

    # A timestamp which updates each time the object is saved
    updated = models.DateTimeField(auto_now=True)  # Updates on each save

    #Order Comments sorted by the created timestamp in reverse chronological order
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.name}: {self.text[:30]}'
