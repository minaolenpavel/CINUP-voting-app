# voteApp/authentication.py

from django.contrib.auth.backends import ModelBackend
from voteApp.models import ProxyVote
from django.contrib.auth import get_user_model
import datetime

class ProxyVoteAuthBackend(ModelBackend):
    def authenticate(self, request, key=None):
        try:
            proxy_vote = ProxyVote.objects.get(key=key, used_at__isnull=True)
            if proxy_vote.expires_at < datetime.datetime.now():
                return None
            proxy_vote.used_by = request.user
            proxy_vote.used_at = datetime.datetime.now()
            proxy_vote.save()
            return proxy_vote.generated_by
        except ProxyVote.DoesNotExist:
            return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
