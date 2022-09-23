"""This module contains a views of the application."""

from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Choice, Question, Votes


class IndexView(generic.ListView):
    """A display of index views."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(
            pub_date__lte=timezone.localtime()
        ).order_by('-pub_date')[:5]


class DetailView(LoginRequiredMixin, generic.DetailView):
    """A display of detail views."""

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.localtime())

    def get(self, request, pk):
        """Show the detail if can_vote is True,if not redirect to the index."""
        question = get_object_or_404(Question, pk=pk)
        user = request.user
        if not question.is_published():
            messages.error(request, 'This question is not available yet.')
            return HttpResponseRedirect(reverse('polls:index'))
        elif not question.can_vote():
            messages.error(request, 'This question is already over')
            return HttpResponseRedirect(reverse('polls:index'))
        selected = ""
        if not user.is_anonymous:
            try:
                q = question.choice_set.all()
                votes = Votes.objects.get(user=user, choice__in=q)
                selected = votes.choice.choice_text
            except Votes.DoesNotExist:
                selected = ""
            return render(request, 'polls/detail.html', {'question': question,
                                                         'selected': selected})


class ResultsView(generic.DetailView):
    """A display of the results pages."""

    model = Question
    template_name = 'polls/results.html'

    def get(self, request, pk):
        """Show the results if method is True, if not redirect to the index."""
        question = get_object_or_404(Question, pk=pk)

        if not question.is_published():
            messages.error(request, 'This question is not available.')
            return HttpResponseRedirect(reverse('polls:index'))
        return render(request, 'polls/results.html', {'question': question, })


@login_required
def vote(request, question_id):
    """Save a Voting choice from a question objects that user voted."""
    user = request.user
    # If a user is not authenticated, a user must login first
    if not user.is_authenticated:
        return redirect('login')
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        try:
            q = question.choice_set.all()
            vote = Votes.objects.get(user=user, choice__in=q)
        # Create a new vote if it does not exists.
        except Votes.DoesNotExist:
            selected = Votes.objects.create(user=user, choice=selected_choice)
            selected.save()
        # Replace a choice with a new choice.
        else:
            vote.choice = selected_choice
            vote.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
