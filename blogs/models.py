from django.db import models
from django.utils import timezone


# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=200)
    date_created = models.DateTimeField('date_created', default=timezone.now())
    date_updated = models.DateTimeField('date_updated', blank=True, null=True)
    date_published = models.DateTimeField('date_published', blank=True, null=True)

    def __str__(self):
        return self.title + " -- by " + self.author

    # class Meta:
    #     ordering = ['title']
    #     # verbose_name = "Blog"
    def publish(self):
        self.date_published = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(is_approved=True)


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")
    commented_by = models.CharField(max_length=200)
    comment_desc = models.TextField()
    commented_at = models.DateTimeField('created_at', default=timezone.now())
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.comment_desc[:30] + " -- by " + self.commented_by + " -- on " + str(self.commented_at)[:11]

    class Meta:
        # verbose_name = "Comment"
        ordering = ['commented_at']

    def approve(self):
        self.is_approved = True
        self.save()