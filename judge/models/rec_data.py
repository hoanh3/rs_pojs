import hashlib
import hmac

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from reversion import revisions

from judge.judgeapi import abort_submission, judge_submission
from judge.models.problem import Problem, SubmissionSourceAccess
from judge.models.profile import Profile
from judge.models.runtime import Language
from judge.utils.unicode import utf8bytes

__all__ = ['RecommendationData']

SUBMISSION_RESULT = (
    ('AC', _('Accepted')),
    ('WA', _('Wrong Answer')),
    ('TLE', _('Time Limit Exceeded')),
    ('MLE', _('Memory Limit Exceeded')),
    ('OLE', _('Output Limit Exceeded')),
    ('IR', _('Invalid Return')),
    ('RTE', _('Runtime Error')),
    ('CE', _('Compile Error')),
    ('IE', _('Internal Error')),
    ('SC', _('Short Circuited')),
    ('AB', _('Aborted')),
)

@revisions.register(follow=['test_cases'])
class RecommendationData(models.Model):
    user = models.ForeignKey(Profile, verbose_name=_('user'), on_delete=models.CASCADE, db_index=False)
    problem = models.ForeignKey(Problem, verbose_name=_('problem'), on_delete=models.CASCADE, db_index=False)
    number_of_attempt = models.IntegerField(default=0)
    final_result = models.CharField(verbose_name=_('result'), max_length=3, choices=SUBMISSION_RESULT,
                              default=None, null=True, blank=True)