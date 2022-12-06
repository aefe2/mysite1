from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView

from .forms import RegisterUserForm, EditProfile
from .models import Question, Choice, User
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'вы не сделали выбор'
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


@login_required
def profile(request):
    return render(request, 'main/profile.html')


# class EditP(request):
#     template_name = 'main/profile_edit.html'
#     form_class = EditProfile
#
#     def get_success_url(self):
#         return reverse('polls:login')


class RegisterView(CreateView):
    template_name = 'main/register.html'
    form_class = RegisterUserForm

    def get_success_url(self):
        return reverse('polls:login')


class LoginView(LoginView):
    template_name = 'main/login.html'
