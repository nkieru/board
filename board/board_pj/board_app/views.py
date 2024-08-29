from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .forms import *
from .filters import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail


class NoticeList(ListView):
    model = Notice
    ordering = '-date_nc'
    template_name = 'notices.html'
    context_object_name = 'notices'
    paginate_by = 10


class MyNoticeList(LoginRequiredMixin, ListView):
    model = Notice
    ordering = '-date_nc'
    template_name = 'my_notices.html'
    context_object_name = 'my_notices'
    paginate_by = 10

    def get_queryset(self):
        queryset = Notice.objects.filter(author_nc=self.request.user.id)
        return queryset


class NoticeDetail(LoginRequiredMixin, DetailView):
    model = Notice
    template_name = 'notice.html'
    context_object_name = 'notice'


class NoticeCreate(LoginRequiredMixin, CreateView):
    form_class = NoticeForm
    model = Notice
    template_name = 'notice_create.html'

    def form_valid(self, form):
        notice = form.save(commit=False)
        notice.author_nc = User.objects.get(id=self.request.user.id)
        return super().form_valid(form)


class NoticeUpdate(LoginRequiredMixin, UpdateView):
    form_class = NoticeForm
    model = Notice
    template_name = 'notice_update.html'

    def dispatch(self, request, *args, **kwargs):
        author = Notice.objects.get(pk=self.kwargs.get('pk')).author_nc.username
        if self.request.user.username == 'board_admin' or self.request.user.username == author:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponse('You do not have permission to')


class FeedbackList(LoginRequiredMixin, ListView):
    model = Feedback
    ordering = '-date_fb'
    template_name = 'my_notice_feedbacks.html'
    context_object_name = 'feedbacks'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Feedback.objects.filter(notice_fb__author_nc_id=self.request.user.id)
        context['filterset'] = NoticeFilter(self.request.GET, queryset, request=self.request.user.id)
        return context


class FeedbackDetail(LoginRequiredMixin, DetailView):
    form_class = FeedbackForm
    model = Feedback
    template_name = 'feedback.html'
    context_object_name = 'feedback'


class FeedbackCreate(LoginRequiredMixin, CreateView):
    form_class = FeedbackForm
    model = Feedback
    template_name = 'feedback_create.html'

    def form_valid(self, form):
        feedback = form.save(commit=False)
        feedback.author_fb = self.request.user
        feedback.notice_id = self.kwargs
        feedback.save()
        feedback.author_nc = User.objects.get(pk=feedback.notice_fb.author_nc.id)
        send_mail(
            subject='Feedback has been added',
            message=f'On your notice {feedback.notice_fb.title} \
            has been added feedback by user {feedback.author_fb.username}.\n'
                    f'\nhttp://127.0.0.1:8000/notices/feedbacks/feedback/{feedback.id}',
            from_email='example-sf@yandex.ru',
            recipient_list=[feedback.author_nc.email],
        )
        return super().form_valid(form)


class FeedbackDelete(LoginRequiredMixin, DeleteView):
    model = Feedback
    template_name = 'feedback_delete.html'
    success_url = '/notices/feedbacks'


@login_required
def accept_feedback(request, **kwargs):
    if request.user.is_authenticated:
        feedback = Feedback.objects.get(id=kwargs.get('pk'))
        feedback.accept = True
        send_mail(
            subject=f'Feedback was accepted',
            message=f'Hello {feedback.author_fb}! Feedback on notice {feedback.notice_fb.title} was accepted.\n',
            from_email='example-sf@yandex.ru',
            recipient_list=[feedback.author_fb.email],
        )
        feedback.save()
        return HttpResponseRedirect('/notices/feedbacks')
    else:
        return HttpResponseRedirect('/')
