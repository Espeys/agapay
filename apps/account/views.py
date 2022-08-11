import logging
from base.views import GenericView
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.permissions import IsAuthenticated

from .permissions import (
    IsModerator,
    IsOrganizer,
    IsCandidate
)
from . import errors, forms


logger = logging.getLogger(__name__)


class AccountsLoginView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.AccountsLoginForm

    # post method
    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class AccountsAccessView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.AccountsAccessForm
    permission_classes = [IsAuthenticated,]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class AccountsRefreshView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.AccountsRefreshForm
    permission_classes = [IsAuthenticated,]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class AccountsRegisterView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.AccountsRegisterForm

    def process_base_form(self, base_form, params, request, *args, **kwargs):
        return base_form(
            params,
            request.FILES, group=request.data.get('user_type', None))

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class AccountsProfileView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.AccountsProfileForm
    permission_classes = [IsAuthenticated,]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class AccountsProfileUpdateView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.AccountsProfileUpdateForm
    permission_classes = [IsAuthenticated,]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class AccountsProfileConfigView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.AccountsProfileConfigForm
    permission_classes = [IsAuthenticated,]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class AccountsProfilePhotoUploadView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.AccountsProfilePhotoUploadForm
    permission_classes = [IsAuthenticated, IsOrganizer|IsModerator]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class AccountsProfilePhotoRemoveView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.AccountsProfilePhotoRemoveForm
    permission_classes = [IsAuthenticated, IsOrganizer|IsModerator]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class AccountsPasswordChangeView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.AccountsPasswordChangeForm
    permission_classes = [IsAuthenticated,]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class AccountsPasswordForgotView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.AccountsPasswordForgotForm

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class AccountsPasswordForgotConfirmView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.AccountsPasswordForgotConfirmForm

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class AccountsProfileFollowView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.AccountsProfileFollowForm
    permission_classes = [IsAuthenticated,]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class AccountsProfileUnfollowView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.AccountsProfileUnfollowForm
    permission_classes = [IsAuthenticated,]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class AccountsProfileFollowerView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.AccountsProfileFollowerForm
    permission_classes = [IsAuthenticated,]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class AccountsProfileFollowingView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.AccountsProfileFollowingForm
    permission_classes = [IsAuthenticated,]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class AccountsProfileSearchView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.AccountsProfileSearchForm
    permission_classes = []

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class AccountsOrganizerView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.AccountsOrganizerForm
    permission_classes = [IsAuthenticated, IsModerator]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class AccountsOrganizerVerifyView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.AccountsOrganizerVerifyForm
    permission_classes = [IsAuthenticated, IsModerator]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class AccountsVerifyEmailView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.AccountsVerifyEmailForm

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class AccountsConnectionRequestView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.AccountsConnectionRequestForm
    permission_classes = [IsAuthenticated,]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class AccountsConnectionRemoveView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.AccountsConnectionRemoveForm
    permission_classes = [IsAuthenticated,]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)



class AccountsConnectionStatusView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.AccountsConnectionStatusForm
    permission_classes = [IsAuthenticated,]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class AccountsConnectionsAcceptedView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.AccountsConnectionsAcceptedForm
    permission_classes = [IsAuthenticated,]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class AccountsConnectionsPendingView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.AccountsConnectionsPendingForm
    permission_classes = [IsAuthenticated,]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class AccountsConnectionsRequestsView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.AccountsConnectionsRequestsForm
    permission_classes = [IsAuthenticated,]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class AccountsConnectionsRequestDenyView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.AccountsConnectionsRequestDenyForm
    permission_classes = [IsAuthenticated,]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class AccountsProfileReportView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.AccountsProfileReportForm
    permission_classes = [IsAuthenticated,]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class AccountsOrganizerDocumentAddView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.AccountsOrganizerDocumentAddForm
    permission_classes = [IsAuthenticated,]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class AccountsOrganizerDocumentRemoveView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.AccountsOrganizerDocumentRemoveForm
    permission_classes = [IsAuthenticated,]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)



class AccountsOrganizerDocumentsView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.AccountsOrganizerDocumentsForm
    permission_classes = [IsAuthenticated,]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class StaticDocumentTypeView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.StaticDocumentTypeForm
    permission_classes = [IsAuthenticated,]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class ChatRoomsView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.ChatRoomsForm
    permission_classes = [IsAuthenticated,]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)

class ChatRoomGetView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.ChatRoomGetForm
    permission_classes = [IsAuthenticated,]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class ChatMessagesView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.ChatMessagesForm
    permission_classes = [IsAuthenticated,]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class ChatMessageAddView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.ChatMessageAddForm
    permission_classes = [IsAuthenticated,]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class ChatMessageRemoveView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.ChatMessageRemoveForm
    permission_classes = [IsAuthenticated,]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class ChatMessagesUnreadUpdateView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.ChatMessagesUnreadUpdateForm
    permission_classes = [IsAuthenticated,]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class NotificationsView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.NotificationsForm
    permission_classes = [IsAuthenticated,]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class NotificationsUpdateView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.NotificationsUpdateForm
    permission_classes = [IsAuthenticated,]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class TopTagsView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.TopTagsForm
    # permission_classes = [IsAuthenticated,]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class RecommendServicesView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.RecommendServicesForm

    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class RecommendEmptyView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.RecommendEmptyForm

    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


from django.shortcuts import render

def index(request, version):
    return render(request, 'chatroom/index.html', {})

def room(request, version, room_name):
    return render(request, 'chatroom/room.html', {
        'room_name': room_name
    })