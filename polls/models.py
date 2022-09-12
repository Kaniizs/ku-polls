import datetime

from django.contrib import admin
from django.db import models
from django.utils import timezone


class Question(models.Model):
    """A model class for Question"""
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('date ended', null=True, blank=True)

    @admin.display(
        boolean=True,
        ordering=['pub_date','end_date'],
        description='Published recently?',
    )
    def was_published_recently(self):
        """Return a boolean whether the question was published recently less than 1 day or not."""
        return timezone.localtime() - datetime.timedelta(days=1) <= self.pub_date <= timezone.localtime()

    def is_published(self):
        """Return a boolean whether the question was published"""
        return self.pub_date <= timezone.localtime()

    def can_vote(self):
        """Return a boolean whether the question is not exceed the ending date"""
        if self.end_date is None:
            return timezone.localtime() >= self.pub_date
        return self.end_date >= timezone.localtime() >= self.pub_date

    def __str__(self):
        """Return a Question text"""
        return self.question_text


class Choice(models.Model):
    """A model class for Choice"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Return a choice text"""
        return self.choice_text
