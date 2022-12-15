from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, UpdateView
from .forms import RegisterUserForm, EditProfileForm
from .models import Question, Choice, User, Vote
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic import UpdateView, CreateView, DeleteView
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView


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


@login_required
def vote(request, question_id):
    question_vote = get_object_or_404(Question, pk=question_id)
    vote, created = Vote.objects.get_or_create(voter=request.user, question_vote=question_vote)
    if not created:
        return render(request, 'polls/detail.html', {
            'question': question_vote,
            'error_message': 'Голосовать можно только один раз'
        })
    try:
        selected_choice = question_vote.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question_vote,
            'error_message': 'Вы не сделали выбор'
        })

    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question_vote.id,)))


@login_required
def profile(request):
    return render(request, 'main/profile.html')


class EditProfileView(SuccessMessageMixin, LoginRequiredMixin,
                      UpdateView):
    model = User
    template_name = 'main/profile_edit.html'
    form_class = EditProfileForm
    success_url = reverse_lazy('polls:profile')
    success_message = 'Личные данные пользователя изменены'

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class UserPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin,
                             PasswordChangeView):
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('polls:profile')
    success_message = 'Пароль пользователя изменен'


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'main/profile_delete.html'
    success_url = reverse_lazy('polls:index')

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удален')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class RegisterView(CreateView):
    template_name = 'main/register.html'
    form_class = RegisterUserForm

    def get_success_url(self):
        return reverse('polls:login')


class LoginView(LoginView):
    template_name = 'main/login.html'
