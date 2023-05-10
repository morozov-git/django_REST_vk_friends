from django.db import models
from users.models import CustomUser

# Create your models here.


class Friends(models.Model):
    user1 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user1_users')
    user2 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user2_users')
    # friendship_status = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(verbose_name='is_active', default=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f'User-1: {self.user1}, User-2: {self.user2}, is_active: {self.is_active}'


class FriendshipRequest(models.Model):
    STATUS_CHOICES = [('SENT', 'sent'), ('CONFIRMED', 'confirmed'), ('DECLINED', 'declined')]
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender_users')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='receiver_users')
    friendship_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='SENT')
    is_active = models.BooleanField(verbose_name='is_active', default=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f'ID:{self.id} ' \
               f'Status: {self.friendship_status}, ' \
               f'Sender: {self.sender.username}, ' \
               f'Receiver: {self.receiver.username}'
