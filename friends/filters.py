from .models import Friends, FriendshipRequest


class FriendsFilter:
	def get(self, data, request, *args, **kwargs):
		method = data.action
		user = request.query_params.get('user', None)
		if user and method == 'list':
			user_friends = Friends.objects.filter(user1_id=user, is_active=True) | \
							Friends.objects.filter(user2_id=user, is_active=True)
			print(user_friends)
			return user_friends


class FriendshipRequestsFilter:
	def get(self, data, request, *args, **kwargs):
		method = data.action
		user = request.query_params.get('user', None)
		action = request.query_params.get('action', None)
		if user and method == 'list' and not action:
			friendship_requests_all = FriendshipRequest.objects.filter(sender=user, is_active=True) | \
										FriendshipRequest.objects.filter(receiver=user, is_active=True)
			print(friendship_requests_all)
			return friendship_requests_all
		if user and method == 'list' and action:
			if action == 's':
				friendship_requests_sender = FriendshipRequest.objects.filter(sender=user, is_active=True)
				return friendship_requests_sender
			if action == 'r':
				friendship_requests_receiver = FriendshipRequest.objects.filter(receiver=user, is_active=True)
				return friendship_requests_receiver

