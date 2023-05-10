from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()
router.register(r'all_friends', AllFriendsAPIView, basename='all_friends')
router.register(r'all_friendship_requests', AllFriendshipRequestsAPIView, basename='all_friendship_request')
router.register(r'user_friends', UserFriendsAPIView, basename='user_friends')
router.register(r'friendship_requests', FriendshipRequestsAPIView, basename='friendship_request')
# print(router.urls)

urlpatterns = [
    path('', include(router.urls)),
    path('userfriends/<int:user>/<int:pk>/', UserFriendsDestroyAPIView.as_view()),
    path('get_friends_status/', GetFriendStatusAPIView.as_view(), name='get_friends_status'),

]
