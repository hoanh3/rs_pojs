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
from judge.models.choices import LANGUAGE_CHOICES, EXPERIENCE_CHOICES, PURPOSE_CHOICES, LEVEL_CHOICES, ALGORITHM_CHOICES, CONTEST_CHOICES, HOBBY_CHOICES

__all__ = ['Survey']

class Survey(models.Model):
    user = models.ForeignKey(Profile, verbose_name=_('user'), on_delete=models.CASCADE, db_index=False)
    language = models.IntegerField(choices=LANGUAGE_CHOICES, null=True, default=None)
    experience = models.IntegerField(choices=EXPERIENCE_CHOICES, null=True, default=None)
    purpose = models.IntegerField(choices=PURPOSE_CHOICES, null=True, default=None)
    skill_level = models.IntegerField(choices=LEVEL_CHOICES, null=True, default=None)
    algorithm = models.IntegerField(choices=ALGORITHM_CHOICES, null=True, default=None)
    contest = models.IntegerField(choices=CONTEST_CHOICES, null=True, default=None)
    hobby = models.IntegerField(choices=HOBBY_CHOICES, null=True, default=None)
    submitted_at = models.DateTimeField(auto_now_add=True)