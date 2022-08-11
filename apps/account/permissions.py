from django.db.models import Q
from rest_framework import permissions

from .models import Profile


class IsOrganizer(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user \
            and request.user.groups.filter(name__in=[Profile.GROUP_ORGANIZER, Profile.GROUP_INDIVIDUAL]).exists():
            return True
        return False


class IsOrganizerAndVerified(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user \
            and request.user.groups.filter(name__in=[Profile.GROUP_ORGANIZER, Profile.GROUP_INDIVIDUAL]).exists() \
            and request.user.profile.is_certified:
            return True
        return False

class IsCandidate(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user \
            and request.user.groups.filter(name=Profile.GROUP_CANDIDATE).exists():
            return True
        return False


class IsModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user \
            and request.user.groups.filter(name=Profile.GROUP_MODERATOR).exists():
            return True
        return False
