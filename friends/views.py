from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from .models import Friends, FriendshipRequest
from .serializers import FriendsSerializer, FriendshipRequestSerializer
from .filters import FriendsFilter, FriendshipRequestsFilter
from .servises import check_friendschip_status, check_user_friend_params,\
	send_friendship_request, update_friendship_request

# Create your views here.


class AllFriendsAPIView(mixins.CreateModelMixin,
						mixins.RetrieveModelMixin,
						mixins.UpdateModelMixin,
						mixins.ListModelMixin,
						mixins.DestroyModelMixin,
						GenericViewSet):

	""" All Friends List for Admins """

	queryset = Friends.objects.all()
	serializer_class = FriendsSerializer
	# permission_classes = [IsAdminUser, IsAuthenticated]


class AllFriendshipRequestsAPIView(mixins.CreateModelMixin,
									mixins.RetrieveModelMixin,
									mixins.UpdateModelMixin,
									mixins.ListModelMixin,
									mixins.DestroyModelMixin,
									GenericViewSet):

	""" All Friendship Requests List for Admins """

	queryset = FriendshipRequest.objects.all()
	serializer_class = FriendshipRequestSerializer
	# permission_classes = [IsAdminUser, IsAuthenticated]


class UserFriendsAPIView(mixins.CreateModelMixin,
							mixins.RetrieveModelMixin,
							mixins.UpdateModelMixin,
							mixins.ListModelMixin,
							mixins.DestroyModelMixin,
							GenericViewSet):

	# generics.ListAPIView

	""" User's Friends API View Class """

	queryset = Friends.objects.all()
	serializer_class = FriendsSerializer

	def get_queryset(self, *args, **kwargs):
		params = self.request.query_params
		if len(params) == 0:
			return Friends.objects.all()
		friends_filter = FriendsFilter()
		queryset = friends_filter.get(data=self, request=self.request, *args, **kwargs)
		return queryset


class UserFriendsDestroyAPIView(generics.DestroyAPIView):

	""" User's Friends Destroy Class """

	queryset = Friends.objects.all()
	serializer_class = FriendsSerializer

	def destroy(self, request, *args, **kwargs):
		user, friend, status = check_user_friend_params(self.request.query_params)
		try:
			if status == 'OK':
				user_friend_destroy = (Friends.objects.filter(user1=user, user2=friend, is_active=True) | \
									   Friends.objects.filter(user1=friend, user2=user, is_active=True)).get()
				user_friend_destroy.is_active = False
				user_friend_destroy.save()
				serializer = self.get_serializer(user_friend_destroy)
				return Response(serializer.data)
			else:
				return status
		except:
			return Response({'error': 'no valid data'})


class FriendshipRequestsAPIView(mixins.CreateModelMixin,
								mixins.RetrieveModelMixin,
								mixins.UpdateModelMixin,
								mixins.ListModelMixin,
								mixins.DestroyModelMixin,
								GenericViewSet):
	""" User's Requests to Friends API View Class """

	queryset = FriendshipRequest.objects.all()
	serializer_class = FriendshipRequestSerializer

	def get_queryset(self, *args, **kwargs):
		params = self.request.query_params
		if len(params) == 0:
			return FriendshipRequest.objects.all()
		friendship_requests_filter = FriendshipRequestsFilter()
		queryset = friendship_requests_filter.get(data=self, request=self.request, *args, **kwargs)
		return queryset

	def create(self, request):
		user, friend, status = check_user_friend_params(self.request.query_params)
		if status == 'OK':
			return send_friendship_request(data=self, request=request, user=user, friend=friend)
		else:
			return status

	def update(self, request, pk):
		user, friend, status = check_user_friend_params(self.request.query_params)
		if status == 'OK':
			return update_friendship_request(data=self, request=request, user=user, friend=friend, pk=pk)
		else:
			return status


class GetFriendStatusAPIView(APIView):

	""" Check Friendship Status """

	def get(self, request):
		user, friend, status = check_user_friend_params(self.request.query_params)
		if status == 'OK':
			return check_friendschip_status(data=self, request=request, user=user, friend=friend)
		else:
			return status
