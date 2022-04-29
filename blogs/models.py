from django.db import models


# Create your models here.
class Blogs(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=200)
    date_created = models.DateTimeField('date_created')
    date_updated = models.DateTimeField('date_updated', blank=True)

    def __str__(self):
        return self.title + " -- by " + self.author

    class Meta:
        ordering = ['title']
        verbose_name = "Blog"


class Comments(models.Model):
    blog = models.ForeignKey(Blogs, on_delete=models.CASCADE, related_name="related_blog")
    commented_by = models.CharField(max_length=200)
    comment_desc = models.CharField(max_length=2000)
    commented_at = models.DateTimeField('created_at')

    def __str__(self):
        return self.comment_desc[:30] + " -- by " + self.commented_by + " -- on " + str(self.commented_at)[:11]

    class Meta:
        verbose_name = "Comment"