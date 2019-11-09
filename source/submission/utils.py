from django.db.models import Sum
from submission.models import Submission


def _get_total_points_of_user(username):
        qs = Submission.objects.filter(user__username=username)
        total_points = qs.aggregate(Sum('points'))
        sum_ = total_points.get('points__sum')

        if not sum_:
            sum_ = 0

        return sum_
