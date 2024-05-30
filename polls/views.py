from django.http import HttpResponse,Http404, HttpResponseRedirect
from .models import Question, Choice
from django.shortcuts import render,get_object_or_404
from django.db.models import F
from django.urls import reverse

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {
        "latest_question_list" : latest_question_list
    }
    return render(request,"index.html",context=context)

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "detail.html", {"question": question})


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
            "polls/detail.html",
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