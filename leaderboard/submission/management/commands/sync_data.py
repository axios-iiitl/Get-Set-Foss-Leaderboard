import logging
import requests

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from submission.models import Repository, Submission

log = logging.getLogger(__file__)


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        log.info('Data sync started')

        Submission.objects.all().delete()

        all_usernames = User.objects.filter(is_superuser=False).values_list('username', flat=True)
        all_repos = Repository.objects.all()

        for repo in all_repos:
            merged_prs = self.get_all_merged_prs(repo)

            for pr in merged_prs:
                try:
                    link = pr['html_url']
                    all_labels = self._get_prs_labels(pr, link)

                    if 'getsetfoss2019' in all_labels:
                        pr_user = pr['user']['login']

                        if pr_user in all_usernames:
                            if 'very easy' in all_labels:
                                points = 10
                            elif 'easy' in all_labels:
                                points = 15
                            elif 'medium' in all_labels:
                                points = 25
                            elif 'hard' in all_labels:
                                points = 30
                            elif 'pro' in all_labels:
                                points = 50
                            else:
                                points = 0

                            user = User.objects.get(username=pr_user)
                            merged_at_utc = timezone.datetime.strptime(
                                pr['merged_at'],
                                '%Y-%m-%dT%H:%M:%SZ',
                            )
                            merged_at_ist = merged_at_utc + timezone.timedelta(hours=5, minutes=30)
                            Submission.objects.create(
                                user=user,
                                merged_at=merged_at_ist,
                                points=points,
                                link=link,
                            )
                except Exception:
                    log.exception('Error while syncing data for %s', link)

    def get_all_merged_prs(self, repo):
        link_template = 'https://api.github.com/repos/{owner}/{repo}/pulls?state=closed&page={page_no}'
        final_data = []

        try:
            for page_no in range(1000):
                link = link_template.format(
                    owner=repo.owner,
                    repo=repo.repo,
                    page_no=page_no+1,
                )

                response = requests.get(link)
                if response.status_code == 200:
                    data = response.json()

                    if not data:
                        break

                    for pr in data:
                        if pr['merged_at'] != 'null':
                            final_data.append(pr)

        except Exception:
            log.exception('Error while getting all merged PRs for repo %s', repo)
            return []

        return final_data

    def _get_prs_labels(self, pr_data, pr_link):
        labels = []

        try:
            for label in pr_data['labels']:
                labels.append(label['name'].lower())
        except Exception:
            log.exception('Error while getting labels for %s', pr_link)

        return labels
