from rest_framework import serializers
from .models import Friends, FriendshipRequest


class FriendsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Friends
		fields = '__all__'


class FriendshipRequestSerializer(serializers.ModelSerializer):
	class Meta:
		model = FriendshipRequest
		fields = '__all__'
