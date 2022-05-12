from django.db import models
from django.urls import reverse
# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('author-detail', kwargs={'pk': self.pk})


class Article(models.Model):
    headline = models.CharField(max_length=250)
    content = models.TextField()
    reporter = models.ManyToManyField(Author, related_name='author')
    pub_date = models.DateTimeField()

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return self.headline

    def get_absolute_url(self):
        return reverse('article-detail', kwargs={'pk': self.pk})