import logging

from apps.account.permissions import (
    IsCandidate,
    IsOrganizer,
    IsOrganizerAndVerified,
    IsModerator,
)
from base.views import GenericView
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.permissions import IsAuthenticated
from . import errors, forms


# Create your views here.


class PostsNewsFeedView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.PostsNewsFeedForm
    permission_classes = []

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class PostsAddView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.PostsAddForm
    permission_classes = [IsAuthenticated, IsCandidate|IsOrganizer]

    def process_base_form(self, base_form, params, request, *args, **kwargs):
        item_type = params.get('item_type', '')

        return base_form(
            params,
            request.FILES, item_type=item_type)

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)

class PostsEditView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.PostsEditForm
    permission_classes = [IsAuthenticated, IsCandidate|IsOrganizer]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class PostsDeleteView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.PostsDeleteForm
    permission_classes = [IsAuthenticated,]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class PostsBookmarkView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.PostsBookmarkForm
    permission_classes = [IsAuthenticated,]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class PostsUnbookmarkView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.PostsUnbookmarkForm
    permission_classes = [IsAuthenticated,]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class PostsLikeView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.PostsLikeForm
    permission_classes = [IsAuthenticated,]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class PostsUnlikeView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.PostsUnlikeForm
    permission_classes = [IsAuthenticated,]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class PostsReportView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.PostsReportForm
    permission_classes = [IsAuthenticated,]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class PostsHistoryView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.PostsHistoryForm
    permission_classes = [IsAuthenticated,]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class PostsReportedView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.PostsReportedForm

    permission_classes = [IsAuthenticated, IsModerator]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class PostsCensorView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.PostsCensorForm

    permission_classes = [IsAuthenticated, IsModerator]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class PostsDiscardView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.PostsDiscardForm

    permission_classes = [IsAuthenticated, IsModerator]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class PostsVerifyView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.PostsVerifyForm

    permission_classes = [IsAuthenticated, IsModerator]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class PostsLikersView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.PostsLikersForm

    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class PostsShareView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.PostsShareForm

    permission_classes = [IsAuthenticated]

    def process_base_form(self, base_form, params, request, *args, **kwargs):
        item_type = params.get('item_type', '')

        return base_form(
            params,
            request.FILES, item_type=item_type)

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class PostsCommentAddView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.PostCommentAddForm

    permission_classes = [IsAuthenticated]


    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class PostsCommentEditView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.PostCommentEditForm

    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class PostsCommentDeleteView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.PostCommentDeleteForm

    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)

class PostsCommentReportView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.PostCommentReportForm

    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)

class PostsCommentsView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.PostCommentsForm

    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class PostsTagSaveView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.PostTagSaveForm

    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class AccountsMoodContentView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.AccountsMoodContentForm

    permission_classes = [IsAuthenticated, IsCandidate]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class AccountsMoodAddView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.AccountsMoodAddForm

    permission_classes = [IsAuthenticated, IsCandidate]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class AccountsMoodEditView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.AccountsMoodEditForm

    permission_classes = [IsAuthenticated, IsCandidate]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)



class AccountsDiaryAggregateView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.AccountsDiaryAggregateForm

    permission_classes = [IsAuthenticated, IsCandidate]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class PostsSupportSendView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.PostsSupportSendForm

    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class PostsSupportDeclineView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.PostsSupportDeclineForm

    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class PostsSupportAcceptView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.PostsSupportAcceptForm

    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class PostsSupportsView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.PostsSupportsForm

    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class RecommendPromotionsView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.RecommendPromotionsForm

    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


class RecommendEmptyView(GenericView):
    errors_dict = errors.ERRORS_DICT
    form_class = forms.RecommendEmptyForm

    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)