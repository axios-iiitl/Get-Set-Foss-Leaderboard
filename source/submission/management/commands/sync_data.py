import logging
import requests

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings

from submission.models import Repository, Submission

log = logging.getLogger(__file__)


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        log.info('Data sync started')

        # delete all previous submissions before syncing data
        Submission.objects.all().delete()

        all_usernames = User.objects.filter(is_superuser=False).values_list('username', flat=True)
        all_repos = Repository.objects.all()

        for repo in all_repos:
            merged_prs = self._get_all_merged_prs(repo)

            for pr in merged_prs:
                try:
                    link = pr['html_url']
                    all_labels = self._get_prs_labels(pr, link)

                    if settings.MAIN_LABEL in all_labels:
                        pr_user = pr['user']['login']

                        if pr_user in all_usernames:
                            points_list = [
                                settings.POINTS_DATA.get(category)
                                for category in settings.POINTS_DATA.keys()
                                if category in all_labels
                            ]

                            if points_list:
                                points = sum(points_list)
                            else:
                                points = 0

                            user = User.objects.get(username=pr_user)
                            merged_at_utc = timezone.datetime.strptime(
                                pr['merged_at'],
                                '%Y-%m-%dT%H:%M:%SZ',
                            )
                            merged_at_ist = merged_at_utc + timezone.timedelta(hours=5, minutes=30)
                            merged_at_ist = timezone.make_aware(merged_at_ist)

                            Submission.objects.create(
                                user=user,
                                merged_at=merged_at_ist,
                                points=points,
                                link=link,
                            )

                except Exception:
                    log.exception('Error while syncing data for %s', link)

    def _get_all_merged_prs(self, repo):
        """Returns all merged PRs for a giver repository."""

        link_template = 'https://api.github.com/repos/{owner}/{repo}/pulls?state=closed&page={page_no}'
        final_data = []
        headers = {
            'Authorization': f'token {settings.GITHUB_PERSONAL_ACCESS_TOKEN}',
        }

        try:
            for page_no in range(1000):
                link = link_template.format(
                    owner=repo.owner,
                    repo=repo.repo,
                    page_no=page_no+1,
                )

                log.info('Getting data for %s', link)

                response = requests.get(link, headers=headers)
                if response.status_code == 200:
                    data = response.json()

                    if not data:
                        break

                    for pr in data:
                        if pr['merged_at'] != None:
                            final_data.append(pr)
                else:
                    log.info('%s response for %s:' % (response.status_code, link))

        except Exception:
            log.exception('Error while getting all merged PRs for repo %s', repo)
            return []

        return final_data

    def _get_prs_labels(self, pr_data, pr_link):
        """Returns all labels for a PR."""

        labels = []

        try:
            for label in pr_data['labels']:
                labels.append(label['name'].lower())
        except Exception:
            log.exception('Error while getting labels for %s', pr_link)

        return labels
