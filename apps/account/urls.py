from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    path('accounts/login/', views.AccountsLoginView.as_view(), name='login'),
    path('accounts/access/', views.AccountsAccessView.as_view(), name='access'),
    path('accounts/refresh/', views.AccountsRefreshView.as_view(), name='refresh'),
    path('accounts/register/', views.AccountsRegisterView.as_view(), name='register'),
    path('accounts/verify/email/', views.AccountsVerifyEmailView.as_view(), name='verify-email'),

    path('accounts/profile/', views.AccountsProfileView.as_view(), name='profile'),
    path('accounts/profile/update/', views.AccountsProfileUpdateView.as_view(), name='profile-update'),
    path('accounts/profile/config/', views.AccountsProfileConfigView.as_view(), name='profile-config'),
    path('accounts/profile/photo/upload/', views.AccountsProfilePhotoUploadView.as_view(), name='profile-photo-upload'),
    path('accounts/profile/photo/remove/', views.AccountsProfilePhotoRemoveView.as_view(), name='profile-photo-remove'),

    path('accounts/password/change/', views.AccountsPasswordChangeView.as_view(), name='password-change'),
    path('accounts/password/forgot/', views.AccountsPasswordForgotView.as_view(), name='password-forgot'),
    # path('accounts/password/forgot/confirm/', views.AccountsPasswordForgotConfirmView.as_view(), name='password-forgot-confirm'),

    path('accounts/profile/follow/', views.AccountsProfileFollowView.as_view(), name='profile-follow'),
    path('accounts/profile/unfollow/', views.AccountsProfileUnfollowView.as_view(), name='profile-unfollow'),

    path('accounts/profile/search/', views.AccountsProfileSearchView.as_view(), name='profile-search'),
    path('accounts/profile/follower/<str:slug>/', views.AccountsProfileFollowerView.as_view(), name='profile-follower'),
    path('accounts/profile/following/<str:slug>/', views.AccountsProfileFollowingView.as_view(), name='profile-following'),

    path('accounts/organizers/', views.AccountsOrganizerView.as_view(), name='organizer'),
    path('accounts/organizers/verify/', views.AccountsOrganizerVerifyView.as_view(), name='organizer-verify'),
    path('accounts/organizer/documents/', views.AccountsOrganizerDocumentsView.as_view(), name='organizer-documents'),
    path('accounts/organizer/document/add/', views.AccountsOrganizerDocumentAddView.as_view(), name='organizer-document-add'),
    path('accounts/organizer/document/remove/', views.AccountsOrganizerDocumentRemoveView.as_view(), name='organizer-document-remove'),


    # connection/add
    path('accounts/connection/request/', views.AccountsConnectionRequestView.as_view(), name='connection-request'),
    path('accounts/connection/remove/', views.AccountsConnectionRemoveView.as_view(), name='connection-remove'),
    # connection/block # connection/remove  connection/status/
    path('accounts/connection/status/', views.AccountsConnectionStatusView.as_view(), name='connection-status'),
    # connection/accept - same as deny maybe just status choices # connection/deny
    # connection/{user}
    path('accounts/connections/pending/', views.AccountsConnectionsPendingView.as_view(), name='connections-pending'),
    path('accounts/connections/requests/', views.AccountsConnectionsRequestsView.as_view(), name='connections-requests'),
    path('accounts/connections/request/deny/', views.AccountsConnectionsRequestDenyView.as_view(), name='connections-request-deny'),
    path('accounts/connections/accepted/<str:slug>/', views.AccountsConnectionsAcceptedView.as_view(), name='connections-accepted'),

    path('accounts/profile/report/', views.AccountsProfileReportView.as_view(), name='profile-report'),

    path('static/document/type/', views.StaticDocumentTypeView.as_view(), name='static-document-type'),

    # message
    path('chat/rooms/', views.ChatRoomsView.as_view(), name='chat-rooms'),
    path('chat/room/get/', views.ChatRoomGetView.as_view(), name='chat-room-get'),

    path('chat/messages/', views.ChatMessagesView.as_view(), name='chat-messages'),
    path('chat/message/add/', views.ChatMessageAddView.as_view(), name='chat-message-add'),
    path('chat/message/remove/', views.ChatMessageRemoveView.as_view(), name='chat-message-remove'),

    path('chat/messages/unread/update/', views.ChatMessagesUnreadUpdateView.as_view(), name='chat-messages-unread-update'),

    # notif
    path('notifications/', views.NotificationsView().as_view(), name='notifications'),
    path('notifications/update/', views.NotificationsUpdateView().as_view(), name='notifications-update'),

    path('top/tags/', views.TopTagsView.as_view(), name='top-tags'),
    path('recommend/services/', views.RecommendServicesView.as_view(), name='recommend-services'),

    path('recommend/services/empty/', views.RecommendEmptyView.as_view(), name='recommend-empty'),

    # chat/urls.py
    path('chatroom/index/', views.index, name='index'),
    path('chatroom/<str:room_name>/', views.room, name='room'),
]