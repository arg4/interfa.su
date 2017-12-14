from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class ArticleBase(models.Model):
    """
    Defines an Article, will link to a disparate html page or
    to a premade 'link page'
    """
    article_name = models.CharField(max_length=140)
    article_external_url = models.CharField(blank=True, max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True)
    name_author = models.ManyToManyField(User, blank=True)
    article_description = models.TextField(null=True, blank=True)
    article_body_text = models.TextField(null=True, blank=True)
    article_caption_styles = models.TextField(null=True,blank=True)
    LINK = 'LI'
    EDITORIAL = 'ED'
    TUTORIAL = 'TU'
    ARTICLE_TYPES = (
        (LINK, 'link'),
        (EDITORIAL, 'editorial'),
        (TUTORIAL, 'tutorial'),
    )
    article_type = models.CharField(
        max_length=2,
        choices = ARTICLE_TYPES,
        default = LINK,
    )
    class Meta:
        abstract = True


class Article(ArticleBase):

    def __str__(self):
        """Return a string with the articles name"""
        return self.article_name[:50] + '...'


class Draft(ArticleBase):

    draft_vote = models.IntegerField(default=0)
    make_public = models.BooleanField(default=False)
    voters = models.ManyToManyField(User, related_name='voters', blank=True)

    def __str__(self):
        """Return a string desribing a draft """
        return self.article_name[:50] + '...'


class Comment(models.Model):
    comment_text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    comment_on = models.ForeignKey(Article, null=True)
    comment_owner = models.ForeignKey(User, null=True)
    commented_anonymously = models.BooleanField(default=False)
    comment_flag = models.IntegerField(default=0) # incremement based on ban.
    comment_ban_text = models.CharField(max_length=140, null=True)

    def __str__(self):
        """Return a string with an abridged comment"""
        return self.comment_text + str(self.id)


# Discussion of articles belongs in IRC but there could be critque comments too...
