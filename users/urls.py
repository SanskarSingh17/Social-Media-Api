from django.urls import path
from .views import UserSignupView, UserLoginView, UserSearchView, FriendRequestView, AcceptRejectFriendRequestView,ListFriendsView,PendingFriendRequestsView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('search/', UserSearchView.as_view(), name='user-search'),
    path('friend-requests/', FriendRequestView.as_view(), name='friend-requests'),
    path('friend-requests/<int:pk>/', AcceptRejectFriendRequestView.as_view(), name='accept-reject-friend-request'),
    path('friends/', ListFriendsView.as_view(), name='list-friends'),
    path('pending-requests/', PendingFriendRequestsView.as_view(), name='pending-requests'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
