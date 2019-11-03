from django.contrib import admin
from submission.models import Submission, Repository


class RepositoryAdmin(admin.ModelAdmin):
    list_display = ['__str__']


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'merged_at', 'points', 'link']


admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Repository, RepositoryAdmin)
