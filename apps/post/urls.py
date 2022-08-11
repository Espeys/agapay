from django.urls import path
from . import views

urlpatterns = [
    path('posts/newsfeed/', views.PostsNewsFeedView.as_view(), name='post-newsfeed'),
    path('posts/add/', views.PostsAddView.as_view(), name='post-add'),
    path('posts/update/', views.PostsEditView.as_view(), name='post-edit'),
    path('posts/delete/', views.PostsDeleteView.as_view(), name='post-delete'),
    path('posts/bookmark/', views.PostsBookmarkView.as_view(), name='post-bookmark'),
    path('posts/unbookmark/', views.PostsUnbookmarkView.as_view(), name='post-unbookmark'),
    path('posts/like/', views.PostsLikeView.as_view(), name='post-like'),
    path('posts/unlike/', views.PostsUnlikeView.as_view(), name='post-unlike'),

    path('posts/report/', views.PostsReportView.as_view(), name='post-report'),
    # path('posts/history/<str:slug>/', views.PostsHistoryView.as_view(), name='post-history'),
    # path('posts/reported/', views.PostsReportedView.as_view(), name='post-reported'),
    # path('posts/censor/', views.PostsCensorView.as_view(), name='post-censor'),
    # path('posts/verify/', views.PostsVerifyView.as_view(), name='post-verify'),
    # path('posts/discard/', views.PostsDiscardView.as_view(), name='post-discard'),

    path('posts/likers/<str:slug>/', views.PostsLikersView.as_view(), name='post-likers'),

    path('posts/share/', views.PostsShareView.as_view(), name='post-share'),

    # Comments
    path('posts/comment/add/', views.PostsCommentAddView.as_view(), name='post-comment-add'),
    path('posts/comment/edit/', views.PostsCommentEditView.as_view(), name='post-comment-edit'),
    path('posts/comment/delete/', views.PostsCommentDeleteView.as_view(), name='post-comment-delete'),
    path('posts/comment/report/', views.PostsCommentReportView.as_view(), name='post-comment-report'),
    path('posts/comments/<str:slug>/', views.PostsCommentsView.as_view(), name='post-comments'),

    # path('accounts/mood/content/', views.AccountsMoodContentView.as_view(), name='mood-content'),
    # path('accounts/mood/add/', views.AccountsMoodAddView.as_view(), name='mood-add'),
    # path('accounts/mood/edit/', views.AccountsMoodEditView.as_view(), name='mood-edit'),


    # path('posts/tag/save/', views.PostsTagSaveView.as_view(), name='post-tag-save'),

    path('accounts/diary/aggregate/', views.AccountsDiaryAggregateView.as_view(), name='diary-aggregate'),


    path('posts/support/send/', views.PostsSupportSendView.as_view(), name='posts-support-send'),
    path('posts/support/accept/', views.PostsSupportAcceptView.as_view(), name='posts-support-accept'),
    path('posts/support/decline/', views.PostsSupportDeclineView.as_view(), name='posts-support-decline'),
    path('posts/supports/', views.PostsSupportsView.as_view(), name='posts-supports'),

    path('recommend/promotions/', views.RecommendPromotionsView.as_view(), name='recommend-promotions'),
    path('recommend/promotions/empty/', views.RecommendEmptyView.as_view(), name='recommend-empty'),
]
