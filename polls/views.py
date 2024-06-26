from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse,Http404, HttpResponseRedirect
from .models import Question, Choice
from django.shortcuts import render,get_object_or_404
from django.db.models import F
from django.urls import reverse
from django.views import generic

class Indexview(generic.ListView):
    template_name = "index.html"
    context_object_name = "latest_question_list"
    
    def get_queryset(self) -> QuerySet[Any]:
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")
    
    
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")
    context = {
        "latest_question_list" : latest_question_list
    }
    return render(request,"index.html",context=context)

class DetailView(generic.DetailView):
    model = Question
    template_name = "detail.html"


def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "detail.html", {"question": question})


class ResultView(generic.DetailView):
    model = Question
    template_name = "results.html"
    
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "results.html", {"question": question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
        
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes")+1
        selected_choice.save()
    
    ## Use of reverse() requires a view name and args in tuple 
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))