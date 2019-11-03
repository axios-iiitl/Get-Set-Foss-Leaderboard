from django.db import models
from django.contrib.auth.models import User


class Repository(models.Model):
    owner = models.CharField(max_length=30)
    repo = models.CharField(max_length=100)

    def get_full_link(self):
        return f'https://github.com/{self.owner}/{self.repo}/'

    def get_short_link(self):
        return f'{self.owner}/{self.repo}'

    def __str__(self):
        return self.get_short_link()

    class Meta:
        verbose_name_plural = 'Repositories'


class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    merged_at = models.DateTimeField('Submitted At')
    points = models.IntegerField(choices=(
        (10, 10),
        (15, 15),
        (25, 25),
        (30, 30),
        (50, 50),
    ))
    link = models.URLField('GitHub link')

    def __str__(self):
        return f'Submission by {self.user}'
