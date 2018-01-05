from datetime import timedelta
from typing import Optional

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest
from django.utils import timezone

from swiss.models.user import User


def register(provider: str, user_id: str, access_token: str, expires_in: int) -> User:
    social_id = '%s:%s' % (provider, user_id)

    try:
        user = User.objects.get(social_id=social_id)
    except ObjectDoesNotExist:
        user = User()
        user.social_id = social_id

    user.access_token = access_token
    user.expire_dt = timezone.now() + timedelta(seconds=expires_in)
    user.save()

    return user


def get_user(request: HttpRequest) -> Optional[User]:
    if 'HTTP_AUTHORIZATION' not in request.META:
        return None

    authorization = request.META['HTTP_AUTHORIZATION'].split(' ')
    if len(authorization) != 2:
        return None

    access_token = authorization[1]
    try:
        return User.objects.get(access_token=access_token)
    except ObjectDoesNotExist:
        return None
