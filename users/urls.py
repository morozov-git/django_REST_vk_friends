from django.urls import path
from .views import UserListCreateView, UserDetailView


urlpatterns = [
    path('', UserListCreateView.as_view(), name='all-users'),
    path('user/', UserDetailView.as_view(), name='user'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user'),
]
