import operator

from django.db.models import Sum
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from submission.models import Submission
from submission.utils import _get_total_points_of_user


class Home(TemplateView):
    template_name = 'submission/home.html'
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')

        return super().get(request, *args, **kwargs)


class Dashboard(LoginRequiredMixin, ListView):
    template_name = 'submission/dashboard.html'
    http_method_names = ['get']

    def get_queryset(self):
        qs = Submission.objects.filter(user=self.request.user).order_by('merged_at')
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['total_points'] = _get_total_points_of_user(self.request.user.username)
        return context


class Leaderboard(ListView):
    template_name = 'submission/leaderboard.html'
    http_method_names = ['get']

    def get_queryset(self):
        data = []
        all_users = (
            User.objects
            .filter(is_superuser=False)
            .order_by('date_joined')
            .values_list('username', flat=True)
        )

        for username in all_users:
            points = _get_total_points_of_user(username)
            github_link = f'https://github.com/{username}'
            data.append({
                'username': username,
                'github_link': github_link,
                'total_points': points,
            })

            data = sorted(data, key=operator.itemgetter('total_points'), reverse=True)

        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = Submission.objects.all().order_by('-created_at').first()
        if obj:
            context['last_updated'] = obj.created_at

        return context
