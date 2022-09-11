from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseRedirect,HttpResponse,Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.localtime()
        ).order_by('-pub_date')[:5] 
    



class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.localtime())
    
    def get(self, request, pk):
        """
        Show the detail of the polls page if can_vote method is True,if not redirect to the results pages.
        """
        question = get_object_or_404(Question, pk=pk)

        # if a question is available to vote then redirect into details page.
        
        if question.can_vote() and question.is_published():
             return render(request, 'polls/detail.html', {'question': question,})
        # Else show an error message and redirect to index pages
        elif not question.is_published():
            messages.error(request, 'This question is not available for voting right now.')
            return redirect('polls:index')
        elif not question.can_vote():
            messages.error(request, 'This question is already ended.')
            return redirect('polls:results')

        
        
        
        
        


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    """Return a response after a user has voted a choices"""
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
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def showtime(request) -> HttpResponse:
    """Return the local time and date."""
    thaitime = timezone.localtime()
    msg = f"<p>The time is {thaitime}.</p>"
    # return the msg in an HTTP response
    return HttpResponse(msg)

