from django.forms import model_to_dict
from rest_framework.response import Response
from users.models import CustomUser
from .models import Friends, FriendshipRequest


def check_user_friend_params(params):
	""" Check User Friend query_params """
	try:
		user = int(params.get('user', None))
		friend = int(params.get('friend', None))
		status = 'OK'
		return user, friend, status
	except:
		return None, None, Response({'Wrong data entry': ['Send correct User_ID and Friend_ID']})


def check_friendschip_status(data, request, user, friend):
	""" Check Friendship Status """
	sent_request = FriendshipRequest.objects.filter(sender=user, receiver=friend, is_active=True).count()
	received_request = FriendshipRequest.objects.filter(sender=friend, receiver=user, is_active=True).count()
	is_friended = (Friends.objects.filter(user1_id=friend, user2_id=user, is_active=True) |\
					Friends.objects.filter(user1_id=user, user2_id=friend, is_active=True)).count()
	if is_friended > 0:
		return Response({'Friendship Status': ['is friended']})
	elif sent_request > 0:
		return Response({'Friendship Status': ['sent request']})
	elif received_request > 0:
		return Response({'Friendship Status': ['received request']})
	else:
		return Response({'Friendship Status': ['no data']})


def send_friendship_request(data, request, user, friend):
	""" Create Friendship Request in DB """
	user = user
	friend = friend
	method = data.action
	# Добавть проверку для авторизованного пользователя(request.user.id == user)
	try:
		check_request = FriendshipRequest.objects.filter(sender=friend,
														receiver=user,
														friendship_status='SENT',
														is_active=True)
		if len(check_request) > 0 and method == 'create':
			checked_request_to_save = check_request.get()
			checked_request_to_save.is_active = False
			checked_request_to_save.save()
			new_friend = Friends.objects.create(user1=CustomUser.objects.get(id=user),
												user2=CustomUser.objects.get(id=friend),
												is_active=True)
			new_friend.save()
			return Response({'Request SENT': {'Friendship Status': 'is friended'}})
		elif method == 'create':
			check_request_is_already_exist = FriendshipRequest.objects.filter(sender=user,
																			receiver=friend,
																			friendship_status='SENT',
																			is_active=True)
			check_request_is_already_declined = FriendshipRequest.objects.filter(sender=user,
																				receiver=friend,
																				friendship_status='DECLINED',
																				is_active=True)
			if len(check_request_is_already_exist) > 0:
				return Response({'Request SENT': f'request is already exist'})
			elif len(check_request_is_already_declined) > 0:
				return Response({'Request SENT': f'request was declined'})
			else:
				new_request = FriendshipRequest.objects.create(sender=CustomUser.objects.get(id=user),
																receiver=CustomUser.objects.get(id=friend),
																friendship_status='SENT')
				new_request.save()
				return Response({'Request SENT': model_to_dict(new_request)})
		else:
			return Response({'error': [f' method: {method} is not permitted']})
	except:
		return Response({'error': ['no valid data']})


def update_friendship_request(data, request, user, friend, pk):
	""" CONFIRMED or DECLINED actions on Friendship Ruquest """
	user = user
	friend = friend
	method = data.action
	action = request.query_params.get('action', None).upper()
	actions = ['DECLINED', 'CONFIRMED']
	# Добавть проверку для авторизованного пользователя(request.user.id == user)
	try:
		get_request_to_update = FriendshipRequest.objects.get(pk=pk)
		if get_request_to_update and action in actions and method == 'update':
			if action == 'DECLINED':
				get_request_to_update.friendship_status = action
				get_request_to_update.save()
				return Response({'Request SENT': model_to_dict(get_request_to_update)})
			elif action.upper() == 'CONFIRMED':
				new_friend = Friends.objects.create(user1=get_request_to_update.receiver,
													user2=get_request_to_update.sender,
													is_active=True)
				new_friend.save()
				get_request_to_update.friendship_status = action
				get_request_to_update.is_active = False
				get_request_to_update.save()
				return Response({'Request CONFIRMED': {'Friendship Status': 'is friended'}})
	except:
		return Response({'error': ['no valid data']})

