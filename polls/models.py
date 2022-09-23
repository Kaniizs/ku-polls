"""This module contains a model for Question, Choice and Votes."""
import datetime

from django.contrib import admin
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    """A model class for Question."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('date ended', null=True, blank=True)

    @admin.display(
        boolean=True,
        ordering=['pub_date', 'end_date'],
        description='Published recently?'
    )
    def was_published_recently(self):
        """Return a boolean whether the question was published recently."""
        lct = timezone.localtime()
        return lct - datetime.timedelta(days=1) <= self.pub_date <= lct

    def is_published(self):
        """Return a boolean whether the question was published."""
        return self.pub_date <= timezone.localtime()

    def can_vote(self):
        """Return a boolean whether the question is within the date."""
        if self.end_date is None:
            return timezone.localtime() >= self.pub_date
        return self.end_date >= timezone.localtime() >= self.pub_date

    def __str__(self):
        """Return a Question text."""
        return self.question_text


class Choice(models.Model):
    """A model class for Choice."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    @property
    def votes(self):
        """Count the numbers of the votes for each choice."""
        return Votes.objects.filter(choice_id=self.id).count()

    def __str__(self):
        """Return a choice text."""
        return self.choice_text


class Votes(models.Model):
    """A vote by user for a question."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    @property
    def question(self):
        """Get the question from the selected choice."""
        return self.choice.question
